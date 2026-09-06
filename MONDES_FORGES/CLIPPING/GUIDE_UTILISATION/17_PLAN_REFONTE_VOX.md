# 17 — Plan de refonte VOX (architecture multi-capteurs)

> Document d'architecture validé, PAS encore implémenté.
> Source complète : `F00_IRON_SENTINEL/F00B_VOX/PLAN_REFONTE_VOX.md`.

## En une phrase
VOX passe d'un scoré sur signal unique (d'où le `signal_intensity:0.9` constant) à un
**tableau brut multi-capteurs** (emotes, clips commu, événements, audio, visuel, lexical)
puis un arbitrage premium. Le but : éliminer le garbage AVANT l'aval (règle
« garbage in = garbage out »).

## Les 3 filtres
1. Émotion (réaction réelle)
2. Statistique lexicale (exploitable en texte)
3. Directive campagne COMPLÈTE (autorisé : source/plateforme/marché/cycle/exclusions)

## Entonnoir (le premium ne voit que le lot propre)
Étage 0 (capteurs gratuits, scan total) → Étage 1 (lexical + campagne) →
Étage 2 (audio + visuel ciblés) → Étage 3 (kimi-k3 arbitrage) → Gate Warsmith.

## Clé premium
Analyse sémantique (reframing hooks_pur) + arbitrage final. PAS l'extraction brute
visuel/audio (ffmpeg + modèles dédiés).

## Phases
**P1→P6 ✅ FAITES** — voir détails ci-dessous.

P1 = `libs/campaign_veto.py` (veto directive campagne complète) branché dans
`run_auto_detect` entre scoring et calcul accepted/rejected.

## Figé
La partie Modal (transcribe.py + workflow + secrets) est un succès, on n'y touche plus.


## État d'implémentation

- **P1** ✅ `libs/campaign_veto.py` — veto directive campagne complète dans `run_auto_detect`.
- **P2-P4** ✅ `libs/vox_refonte.py` — capteurs (emotes+vélocité+événements+lexical), dégradation gracieuse sur clips/audio/visuel.
- **P6** ✅ `vox_refonte.real_intensity()` + `build_raw_table()` — intensité RÉELLE (plus la constante 0.9), tableau brut `raw_table.json`.
- **P5** ✅ `libs/vox_premium.py` — arbitrage kimi-k3 (score reframing + verdict) sur les survivants.

### Fichiers
`libs/campaign_veto.py` · `libs/vox_refonte.py` · `libs/vox_premium.py` · patch `auto_detector.py` · workflow (injecte NVIDIA_NIM_API_KEY/MODEL).


## Capteurs audio + visuel (P4 — phase 2)
- **`libs/audio_sensor.py`** — rire/applaudissement (heuristique RMS+ZCR+burets) + silence, gratuit (numpy+ffmpeg), sur fenêtres survivantes uniquement.
- **`libs/visual_sensor.py`** — visage (OpenCV Haar) + cut (ffmpeg scene detect), gratuit, dégradation gracieuse.
- Branchés dans `vox_refonte.build_raw_table()` (colonnes `audio_laugh`, `audio_applause`, `visual_face`, `visual_cut`).
- ✅ **Capteur clips communautaires** — `libs/clips_heatmap.py` via GraphQL public Twitch (Client-ID web anonyme, ZÉRO clé). Heatmap densité × vues + moisson des titres. Dégradation gracieuse (endpoint interne fragile).


## Note test réel (2026-09-06)
- Chat replay Twitch : l'API v5 est morte ; remplacé par **GraphQL public** (Client-ID web anonyme,
  pagination par offset Int). C'est la même source que le capteur clips.
- Ordre impératif dans `run_auto_detect` : capteurs (8a) → scoring (8) → veto (8b) → premium (8c).
  Le scoring consomme l'intensité réelle, il doit donc être APRÈS build_raw_table.
