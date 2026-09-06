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
