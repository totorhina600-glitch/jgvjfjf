"""
vox_refonte.py — P2→P6 : capteurs → tableau brut → intensité réelle → scoring
=================================================================================
Refonte multi-capteurs de F00B_VOX. Remplace le `intensity` constant (0.85/0.9)
par une MESURE RÉELLE d'intensité = convergence de signaux indépendants.

Capteurs implémentés :
  P2 (gratuit)  : emotes + vélocité + événements (raid/host/subs) — depuis chat_messages.
                  clips communautaires : dégradation gracieuse (Helix non branché → absent).
  P3 (lexical)  : densité, gap max, hook positionnel 0-3s, pic d'énergie unique.
  P4 (lourd)    : audio (silence via word-gaps) ; rire/applaudissement & visuel →
                  dégradation gracieuse (modèles dédiés, non branchés dans ce run).

Chaque fonction est DÉFENSIVE : retourne None quand le signal est indisponible,
ne lève jamais. Le scoring se replie sur les signaux présents.
"""

import math
import re

# références émotionnelles (alignées sur auto_detector._EMOTION_EMOTES)
EMOTE_MAP = {
    "joy": ["LUL", "KEKW", "OMEGALUL", "haHAA", "LOL", "Pog", "EZ", "Kappa"],
    "hype": ["PogChamp", "Poggers", "CLAP", "Kreygasm", "LETSGO", "HYPERS"],
    "negative": ["Sadge", "peepoSad", "monkaS", "weirdChamp", "KEKW"],
}
ALL_EMOTES = [e for v in EMOTE_MAP.values() for e in v]

EVENT_RE = [
    (r"\braid\b", "raid"),
    (r"\bhost(?:ing|ed)?\b", "host"),
    (r"subscribed|subscription|\bsub\b", "sub"),
    (r"gift(?:ed)?\s+(?:sub|prime)", "gift_sub"),
    (r"welcome\b", "follow"),
]

def _num(x, default=0.0):
    try:
        return float(x)
    except (TypeError, ValueError):
        return default

def _window_words(words, s, e):
    return [w for w in words if s <= _num(w.get("start")) < e]

def _window_messages(msgs, s, e):
    return [m for m in msgs if s <= _num(m.get("offset_sec")) < e]

# ─── P2 : émotes ─────────────────────────────────────────────────────────
def emote_signal(msgs_window):
    """Fraction de messages portant une emote émotionnelle, dilatée 0..1."""
    if not msgs_window:
        return 0.0
    hits = 0
    for m in msgs_window:
        body = str(m.get("body", "")).upper()
        emotes = [str(e).upper() for e in m.get("emotes", [])]
        if any(e in body or e in emotes for e in ALL_EMOTES):
            hits += 1
    ratio = hits / len(msgs_window)
    # >30% de messages émotifs = intensité maximale émotionnelle
    return min(1.0, ratio / 0.30)

def chat_baseline(messages, duration=0.0):
    """Messages/seconde moyen sur toute la VOD (référence pour la vélocité)."""
    if not messages:
        return 1e-6
    span = duration
    if span <= 0:
        offs = [_num(m.get("offset_sec")) for m in messages if _num(m.get("offset_sec")) >= 0]
        span = (max(offs) - min(offs)) if len(offs) > 1 else 1.0
    return max(len(messages) / max(span, 1.0), 1e-6)

def velocity_signal(msgs_window, window_dur, baseline):
    """Ratio vélocité locale / baseline. 3× la baseline = 1.0."""
    if window_dur <= 0:
        return 0.0
    rate = len(msgs_window) / window_dur
    if baseline <= 0:
        return 0.0
    return min(1.0, (rate / baseline) / 3.0)

def event_signal(msgs_window):
    """Binary : au moins un événement majeur (raid/host/sub/gift/follow) ?"""
    if not msgs_window:
        return 0.0
    for m in msgs_window:
        body = str(m.get("body", "")).lower()
        for pat, _ in EVENT_RE:
            if re.search(pat, body):
                return 1.0
    return 0.0

def clips_signal(vod_url, s, e):
    """Réservé P2 (heatmap clips communautaires). Non branché → None."""
    return None

# ─── P3 : lexical ────────────────────────────────────────────────────────
def lexical_signal(words, s, e, trigger_words):
    window_words = _window_words(words, s, e)
    dur = e - s
    density = len(window_words) / dur if dur > 0 else 0.0

    # gap max entre mots de la fenêtre
    gap_max = 0.0
    prev_end = s
    for w in sorted(window_words, key=lambda x: _num(x.get("start"))):
        ws = _num(w.get("start"))
        gap = ws - prev_end
        if gap > gap_max:
            gap_max = gap
        prev_end = _num(w.get("end"), ws)
    if prev_end < e:
        gap_max = max(gap_max, e - prev_end)

    # hook positionnel : mot trigger dans les 3 premières secondes
    hook_zone = [w for w in window_words if _num(w.get("start")) - s <= 3.0]
    hook_text = " ".join(str(w.get("word", "")) for w in hook_zone).lower()
    tl = [t for t in trigger_words if len(str(t)) > 3]
    hook = any(t in hook_text for t in tl)

    return {"density": density, "gap_max": round(gap_max, 2), "hook": hook,
            "silence_gt_3s": gap_max > 3.0}

# ─── P4 : audio / visuel (dégradation gracieuse) ────────────────────────
def audio_silence_signal(lex):
    """Récupère le silence depuis les gaps de mots (proxy orthogonal déjà calculé)."""
    return 1.0 if lex.get("silence_gt_3s") else 0.0

def audio_laugh_signal(audio_path, s, e):
    return None  # modèle audio dédié requis — non branché

def visual_signal(video_path, s, e):
    return None  # modèle vision requis — non branché

# ─── intensité réelle (P6) ──────────────────────────────────────────────
def real_intensity(c, words, messages, baseline, trigger_words):
    s = _num(c.get("start_sec", c.get("start")))
    e = _num(c.get("end_sec", c.get("end")))
    dur = e - s
    mw = _window_messages(messages, s, e)

    signals = {}
    signals["emo"] = emote_signal(mw)
    signals["vel"] = velocity_signal(mw, dur, baseline)
    signals["evt"] = event_signal(mw)
    lex = lexical_signal(words, s, e, trigger_words)
    signals["hook"] = 1.0 if lex.get("hook") else 0.0

    weights = {"emo": 0.35, "vel": 0.25, "evt": 0.20, "hook": 0.20}
    present = {k: v for k, v in signals.items() if v is not None}
    total_w = sum(weights.get(k, 0.0) for k in present)
    if total_w <= 0:
        return 0.5  # aucun signal : neutre, pas de constante faussement haute
    val = sum(weights.get(k, 0.0) * v for k, v in present.items()) / total_w
    return round(min(1.0, max(0.1, val)), 3)

# ─── tableau brut (P6) ──────────────────────────────────────────────────
RAW_TABLE_COLUMNS = [
    "window_id", "start_sec", "end_sec", "duration_sec",
    "emote_joy", "chat_velocity", "chat_spike", "event",
    "clips_density", "clips_views",
    "lex_density", "lex_gap_max", "lex_hook", "lex_silence",
    "audio_silence", "intensity", "campaign_ok",
]

def build_raw_table(candidates, words, messages, trigger_words, duration=0.0):
    """Enrichit chaque candidat d'une intensité réelle + construit le tableau brut.
    Retourne (candidates_modifiés, raw_table)."""
    baseline = chat_baseline(messages, duration)
    table = []
    for i, c in enumerate(candidates):
        s = _num(c.get("start_sec", c.get("start")))
        e = _num(c.get("end_sec", c.get("end")))
        dur = e - s
        mw = _window_messages(messages, s, e)
        lex = lexical_signal(words, s, e, trigger_words)
        c["intensity"] = real_intensity(c, words, messages, baseline, trigger_words)
        c["_win_words"] = lex
        table.append({
            "window_id": f"w{i:04d}",
            "start_sec": round(s, 2),
            "end_sec": round(e, 2),
            "duration_sec": round(dur, 2),
            "emote_joy": round(emote_signal(mw), 3),
            "chat_velocity": round(velocity_signal(mw, dur, baseline), 3),
            "chat_spike": round(velocity_signal(mw, dur, baseline), 3),
            "event": event_signal(mw),
            "clips_density": None,
            "clips_views": None,
            "lex_density": round(lex["density"], 3),
            "lex_gap_max": lex["gap_max"],
            "lex_hook": lex["hook"],
            "lex_silence": lex["silence_gt_3s"],
            "audio_silence": audio_silence_signal(lex),
            "intensity": c["intensity"],
            "campaign_ok": None,
        })
    return candidates, table
