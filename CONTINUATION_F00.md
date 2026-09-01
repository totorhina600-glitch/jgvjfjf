# CONTINUATION — Reprise du siège (F00_CAPTEURS)

> **LIRE CE FICHIER EN PREMIER** si vous arrivez dans ce repo "à froid".
> Il dit EXACTEMENT où le travail s'est arrêté et quoi faire ensuite.

---

## 📅 DERNIÈRE MISE À JOUR

**Date** : 2026-09-01
**Ajout** : F06_DIRECTOR + Mode PUR

---

## 1. État au dernier push

### ✅ Ce qui existe

- **CLIPPING** est opérationnel avec les modes : informatif, humour, meme
- **3 sièges terminés** : NBA_WESTBROOK, STUDENT_DEBT, MARVEL_DOOMSDAY
- **6 frégates actives** : F00 → F05
- **ARCHIVUM** enrichi avec channels, campagnes, learnings

### 🆕 Ajouté aujourd'hui

- **F06_DIRECTOR** — Le Directeur de Montage
  - `F06_DIRECTOR/CODEBASE/director.py` — Génération instructions montage
  - `F06_DIRECTOR/CODEBASE/pattern_extractor.py` — Extraction patterns
  - `ARCHIVUM/montage/` — Bibliothèque de montage

- **Mode PUR** — Clipping pur (podcast → clip viral)
  - Workflow complet : F00 → F06
  - Le streamer Whop fournit le podcast + clip ref

---

## 2. Les Frégates (mise à jour)

| Code | Nom | Rôle | Statut |
|------|-----|------|--------|
| F00 | CAPTEURS | Scan viral + assimilation source streamer | ✅ Opérationnel |
| F01 | SCOUT | Transcription vidéo | ✅ Opérationnel |
| F02 | TYRANT_CAMP | Verdict GO/NO-GO + océan bleu | ✅ Opérationnel |
| F03 | SOURCE_HUNTER | Sélection segment parfait | ✅ Opérationnel |
| F04 | COPYWRITER | Forger texte viral (frégate lourde) | ✅ Opérationnel |
| F05 | PACKAGER | Emballer production pack | ✅ Opérationnel |
| **F06** | **DIRECTOR** | **Instructions de montage** | 🆕 **Nouveau** |

---

## 3. Le Mode PUR — Workflow détaillé

### Inputs du Warsmith
1. Podcast source (fourni par le streamer Whop)
2. Clip viral de référence (optionnel)
3. Plateforme cible (YouTube Shorts / TikTok / Instagram Reels)
4. Marché cible (ex : US / Anglais / Jeune)

### Workflow
```
F00_CAPTEURS → Assimile source streamer (podcast + clip ref)
    ↓
F01_SCOUT → Transcription complète du podcast
    ↓
F02_TYRANT_CAMP → Identifie règles viralité + consulte ARCHIVUM
    ↓
F03_SOURCE_HUNTER → Sélectionne le segment parfait (timestamp précis)
    ↓
F04_COPYWRITER → Forge hook visuel (titres, overlays) + métadonnées
    ↓
F05_PACKAGER → Emballe le production pack
    ↓
F06_DIRECTOR → Génère instructions de montage détaillées
    ↓
OMNIS_WATCH → Exécute le montage
    ↓
Opérateur → Poster + soumettre Whop < 1h
```

### Outputs
- `segment.json` — Segment précis (timestamp)
- `text_payload.json` — Titres, overlays, hashtags
- `production_pack.json` — Pack complet
- `montage_instructions.json` — Instructions de montage

---

## 4. F06_DIRECTOR — Détails techniques

### Architecture
```
F06_DIRECTOR/
├── CODEBASE/
│   ├── director.py          ← Script principal
│   ├── pattern_extractor.py ← Extraction patterns
│   └── requirements_f06.txt ← Dépendances
├── IN/                      ← Reçoit de F03/F04
├── OUT/                     ← Produit montage_instructions.json
└── TRACKING/
    └── F06_LOG.md           ← Journal
```

### ARCHIVUM/montage/
```
ARCHIVUM/montage/
├── transcripts/     ← Vidéos tutos montage YouTube
├── patterns/        ← Patterns extraits (hooks, zooms, cuts)
├── rules/           ← Règles par plateforme
│   ├── youtube_shorts.md
│   ├── tiktok.md
│   └── instagram_reels.md
└── examples/        ← Exemples de clips réussis
```

### Contenu de montage_instructions.json
- `hook` : durée, type, template, zoom, son
- `body` : cuts, zooms, text overlays, transitions
- `outro` : fade, texte, sound
- `style` : pacing, energy curve, color palette
- `compliance` : disclosure, platform

---

## 5. APIs nécessaires

| API | Frégate | Usage |
|-----|---------|-------|
| YouTube Data API v3 | F00 | Stats, search, trending |
| youtube-transcript-api | F01 | Transcription vidéo |
| OpenAI GPT-4o | F02, F04, F06 | Analyse, génération, instructions |
| GLM 5.2 (NVIDIA) | F04, F06 | Génération premium |

### Clés API
```
YOUTUBE_API_KEY          → YouTube Data API v3
OPENAI_API_KEY           → GPT-4o
CLIPPING_PREMIUM_API_KEY → GLM 5.2 via NVIDIA
```

---

## 6. Prochaines étapes

### Court terme
1. ✅ F06_DIRECTOR créé
2. ⏳ Collecter des transcripts de tutos montage YouTube
3. ⏳ Tester F06 avec un vrai segment
4. ⏳ Intégrer F06 dans le workflow complet

### Moyen terme
1. Enrichir ARCHIVUM/montage/ avec plus de patterns
2. Ajouter l'IA (OpenAI/GLM) pour génération avancée
3. Tester le workflow PUR complet de bout en bout
4. Optimiser les instructions selon les learnings

---

## 7. Commandes utiles

```bash
# Lancer F06_DIRECTOR
python F06_DIRECTOR/CODEBASE/director.py F03_OUT/segment.json F04_OUT/text_payload.json context.json

# Extraire les patterns
python F06_DIRECTOR/CODEBASE/pattern_extractor.py

# Vérifier l'état de la flotte
python IW_CUSTOS.py --mode status
```

---

*"Fer au-dedans, Fer au-dehors. Le siège continue."* 🔩
