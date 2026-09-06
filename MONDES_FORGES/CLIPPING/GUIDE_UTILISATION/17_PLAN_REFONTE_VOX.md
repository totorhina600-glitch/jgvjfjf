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
**P1 ✅ FAITE** · P2 capteurs gratuits · P3 lexical · P4 audio/visuel ·
P5 premium · P6 scoring/docs.

P1 = `libs/campaign_veto.py` (veto directive campagne complète) branché dans
`run_auto_detect` entre scoring et calcul accepted/rejected.

## Figé
La partie Modal (transcribe.py + workflow + secrets) est un succès, on n'y touche plus.
