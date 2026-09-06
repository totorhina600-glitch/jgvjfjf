# F00B_LOG — Journal de déploiement F00B_VOX

## 2026-09-05 — Auto-Detect v1 (Option A)

**Statut** : ✅ Implémenté, prêt à tester
**Commit** : feat(F00B): auto_detect v1 — transcription word-level, chat replay, scoring premium

### Fichiers créés/modifiés
- `CODEBASE/libs/__init__.py` → nouveau dossier libs
- `CODEBASE/libs/auto_detector.py` → module auto-detect complet (~470 lignes)
- `CODEBASE/f00b_vox.py` → commande `auto_detect` ajoutée au CLI + flags `--keep-audio`, `--no-chat`, `--market`, `--platform`, `--nb-clips`
- `CODEBASE/requirements_f00b.txt` → documentation des dépendances
- `CONTRACTS/f00b_secrets.example.json` → config clé premium (pattern F04)

### Ce qui a changé
**Avant** : F00B était un constructeur de fenêtres qui exigeait des timestamps humains (signals.json). Le Warsmith devait scrubs la VOD manuellement.

**Après** : F00B détecte automatiquement :
1. **Audio seul** (yt-dlp -f ba, stream copy) → pas de MP4 complet
2. **Transcription** via clé premium (Whisper API OpenAI-compatible, chunks ffmpeg stream copy)
   - Mode **words** : timestamps mot par mot → analyse speech complète
   - Mode **segments** : timestamps par segments → conversion pseudo-mots
   - Mode **texte** : texte brut → fallback chat-only (analyse speech désactivée)
3. **Chat replay Twitch** (API v5 publique, pas d'auth) → pics d'engagement
4. **Speech analysis** (triggers, punchlines, densité) — si mode words/segments
5. **Fusion + scoring multicritère** → candidats.json
6. **Gate Warsmith** reste obligatoire → le Warsmith valide, il ne détecte plus

### Clé premium
- Config : `CONTRACTS/f00b_secrets.json` (même pattern que F04)
- Env vars : `CLIPPING_F00B_API_KEY` ou fallback `AI_GATEWAY_API_KEY`
- Endpoint : `{base_url}/audio/transcriptions` (OpenAI-compatible)

### Pipeline mis à jour
```
Ancien :  Warsmith fournit timestamps → F00B score → gate
Nouveau : F00B auto_detect → candidats.json → score → gate Warsmith
```

### Commande
```bash
python f00b_vox.py auto_detect --nb-clips 5 --market us_young_english --platform youtube_shorts
```


## 2026-09-06 — Transcription GPU Modal (moteur swappable)

**Statut** : ✅ Déployé et testé en production (run GH Actions vert + artefacts commités)

### Fichiers créés
- `MODAL/transcribe.py` → service endpoint `/audio/transcriptions` (faster-whisper GPU)
- `MODAL/requirements.txt` → dépendances (référence)
- `MODAL/DEPLOYER.md` → guide déploiement/rotation de compte

### Ce qui a changé
- **Aucun** changement dans `f00b_vox.py` / `auto_detector.py`.
- La transcription passe par un endpoint OpenAI-compatible sur GPU Modal au lieu du CPU local.
- La config se fait dans `f00b_secrets.json` (`base_url` = URL Modal), jamais dans le code.

### Décision clé
- Clé premium NVIDIA = **analyse/copywriting** (pas transcription).
- Transcription = **Modal (Whisper medium)** — modèle swappable via config.
- Rotation de compte Modal possible sans toucher au code (crédits gratuits).


## 2026-09-06 — Orchestration Oracle via GitHub Actions

**Statut** : ✅ Orchestration validée — premier test de production réel réussi

### Fichiers créés/modifiés
- `.github/workflows/perturabo_transcribe.yml` → pipeline deploy→transcribe→score→commit
- `GUIDE_UTILISATION/16_ORCHESTRATION_GITHUB_ACTIONS.md` → doctrine des rôles
- `MODAL/DEPLOYER.md` → corrigé (déploiement via GH Actions, plus machine opérateur)

### Décision clé
- L'opérateur ne code pas, ne déploie pas, ne clique pas : il valide les Portes.
- L'Oracle (Cody) déclenche le workflow via l'API et suit les runs.
- Secrets injectés en aveugle (chiffrés libsodium), jamais commités.


## 2026-09-06 — Premier test de production réel (VOD aishahsofey)

**Statut** : ✅ SUCCESS — run GitHub Actions vert, artefacts commités dans ARCHIVUM.

### Résultat
- VOD : `https://www.twitch.tv/videos/2864600351` (aishahsofey, GTA V REACTIONS, 3h29)
- Transcript : `ARCHIVUM/montage/transcripts/v2864600351_transcript.json` (15 118 mots word-level)
- Candidats : `ARCHIVUM/montage/transcripts/v2864600351_candidats.json` (9 acceptés / 1 rejeté)

### Correctifs apportés au service Modal (leçons)
1. `requests==2.32.3` manquant → 500 (faster-whisper importe `requests` dans utils.py)
2. Image de base : `debian_slim` → `nvidia/cuda:12.4.0-runtime-ubuntu22.04` (libcublas.so.12 manquant → 500)
3. Préchargement du modèle au build (`.run_function`) + fallback CPU si CUDA absente
4. Endpoint durci : renvoie le traceback dans le corps du 500 (plus jamais aveugle)
