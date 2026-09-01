# 🔥 MONDE FORGE — CLIPPING

> *"Une campagne est une forteresse. Un angle d'attaque est un plan de siège. Le texte est l'artillerie qui ouvre la brèche."*

---

## 📋 POSITIONNEMENT

**PERTURABO/CLIPPING** = le QG des campagnes **Whop Content Rewards**.

```
PERTURABO/CLIPPING  →  QUOI raconter (stratégie + copywriting)
        ↓
OMNIS_WATCH         →  COMMENT couper/rendre (tactique + production)
        ↓
Opérateur humain    →  Poster + soumettre Whop (dernière porte)
```

**La séparation des rôles est sacrée :**
- **PERTURABO** = quoi raconter (stratégie + copywriting)
- **OMNIS_WATCH** = comment couper/rendre (tactique + production)
- **L'opérateur humain** = poster + soumettre Whop (dernière porte)

---

## 🎯 LES 4 INPUTS DU WARSMITH

1. Doc directif de la campagne (goal doc Whop — tout est dedans)
2. Clip de référence (celui qui a percé, fourni par la campagne)
3. Plateforme cible (YouTube / TikTok / Instagram)
4. Marché cible (ex : US / Anglais / Jeune)

**PERTURABO demande :** "Combien d'angles d'attaque ?"
→ N → N plans de siège → N production packs → N vidéos

Chaque pack = **1 vidéo pour 1 plateforme pour 1 marché**. Pas de multi-plateforme par pack.

---

## 🎬 LES 4 PORTES

| Porte | Frégates mobilisées | Produit | Validateur |
|-------|---------------------|---------|------------|
| **1** | F02_TYRANT_CAMP (réactif + prospectif) | verdict.json (GO/NO-GO + blue_ocean_unlocked) | Warsmith |
| **2** | ANGLESMITH (via F02 stratégie) | angles.json (N angles sur direct + océan bleu) | Warsmith |
| **3** | F03_SOURCE_HUNTER + F04_COPYWRITER | source_specimen.json + text_payload.json + .md | Warsmith + IRON ordonnancement |
| **4** | F05_PACKAGER | N production_pack.json → OMNIS_WATCH | Warsmith |

---

## ⚔️ LES FRÉGATES

| Code | Nom | Rôle | Output |
|------|-----|------|--------|
| **F00** | CAPTEURS | Scan viral (RSS, Trends, YouTube, Suggest) | raw_source.json |
| **F01** | SCOUT | Transcription vidéo | transcript.json |
| **F02** | TYRANT_CAMP | Verdict GO/NO-GO + océan bleu | campaign_verdict.json |
| **F03** | SOURCE_HUNTER | Sélection du segment parfait | segment.json |
| **F04** | COPYWRITER | Forger le texte viral (frégate lourde) | text_payload.json + .md |
| **F05** | PACKAGER | Emballer le production pack final | production_pack.json |
| **F06** | DIRECTOR | Instructions de montage | montage_instructions.json |

---

## 🔥 LES 4 MODES DE CONTENU

### 1. 📰 INFORMATIF
Clips informatifs — facts, news, documents.
- Source : vidéos existantes
- Style : sérieux, éducatif
- Hook : question ou statement percutant

### 2. 😂 HUMOUR
Clips humoristiques — spin comique, punchlines.
- Source : vidéos existantes
- Style : décalé, drôle
- Hook : punchline ou situation absurde

### 3. 🎭 MEME
Clips mèmes — formats viraux, reactions, trends.
- Source : tendances/keyword
- Style : viral, réaction
- Hook : moment choquant ou drôle

### 4. ✂️ PUR ← **NOUVEAU**
Clips EXTRAITS de long-form (podcast, interview, conf).
- Source : podcast/stream fourni par le streamer Whop
- Style : moment clé extrait
- Hook : la phrase choc du podcast

**Workflow PUR :**
```
F00 → Assimile source streamer (podcast + clip ref)
F01 → Transcription complète
F02 → Identifie les règles de viralité + consulte ARCHIVUM
F03 → Sélectionne le segment parfait (timestamp précis)
F04 → Forge hook visuel (titres, overlays) + métadonnées
F05 → Emballe le production pack
F06 → Génère les instructions de montage détaillées
```

---

## 🎬 F06_DIRECTOR — Le Directeur de Montage

**F06** est la frégate qui génère les **instructions de montage** pour OMNIS_WATCH.

### Inputs
- Segment (F03)
- Text payload (F04)
- Contexte (plateforme, émotion, durée)

### Outputs
- `montage_instructions.json`

### Ce que contiennent les instructions :
- **Hook** : durée, type, template, zoom, son
- **Body** : cuts, zooms, text overlays, transitions
- **Outro** : fade, texte, sound
- **Style** : pacing, energy curve, color palette

### ARCHIVUM/montage/
- `transcripts/` — Vidéos tutos montage YouTube
- `patterns/` — Patterns extraits (hooks, zooms, cuts)
- `rules/` — Règles par plateforme (YouTube Shorts, TikTok, Instagram Reels)
- `examples/` — Exemples de clips réussis

---

## 📊 ARCHIVUM — LES 10 ZONES

| Zone | Contenu | Rôle |
|------|---------|------|
| `rules/` | whop_rules.md, clipping_rules.md, platform_{3}.md | Savoir statique |
| `campaign/` | directive.md, reference_clip.json, verdict.json | LA campagne en cours |
| `platform_generator/` | youtube_profile.md, tiktok_profile.md, instagram_profile.md | Profil plateforme |
| `market_generator/` | us_young_english.md (+ futurs) | Profil marché |
| `knowledge_base/` | sites/, docs/, transcripts/ | TOUT sur le clipping |
| `copywriting/` | 8 sous-dossiers (hooks, formulas, subliminal, slang...) | Musée du copywriting |
| `angles/` | angle_patterns.json, angle_performance.json | Bibliothèque d'angles |
| `demons/` | <demon_id>.json | Démon campagne + veille |
| `channels/` | <account_slug>/identity.json + performance.json | Comptes de clipping |
| `learnings/` | learnings.json | Boucle rétro-active |
| **montage/** | transcripts/, patterns/, rules/, examples/ | **Bibliothèque de montage** ← NOUVEAU |

---

## ⚠️ HÉRÉSIES INTERDITES

Le forge CLIPPING ne fait jamais :
- ❌ Coupe vidéo (boulot d'OMNIS_WATCH)
- ❌ Rendu (boulot d'OMNIS_WATCH)
- ❌ Auto-posting (l'opérateur poste — risque ban)
- ❌ Duplication des règles core (liens, pas copies)
- ❌ Chasse externe aux sources (assets campagne seulement)
- ❌ Variation directe du clip de référence
- ❌ Re-ciblage océan bleu au-delà de 1 couche
- ❌ Scrap auto F00_CAPTEURS (commandité Warsmith seulement)
- ❌ Décider du style visuel final (OMNIS_WATCH applique ses presets)

---

## 🔧 STACK D'INTÉGRATION

### APIs utilisées
| API | Frégate | Usage |
|-----|---------|-------|
| YouTube Data API v3 | F00 | Stats, search, trending |
| youtube-transcript-api | F01 | Transcription vidéo |
| OpenAI GPT-4o | F02, F04, F06 | Analyse, génération texte, instructions |
| GLM 5.2 (NVIDIA) | F04, F06 | Génération premium |

### Clés API nécessaires
```
YOUTUBE_API_KEY          → YouTube Data API v3
OPENAI_API_KEY           → GPT-4o
CLIPPING_PREMIUM_API_KEY → GLM 5.2 via NVIDIA
```

---

## 🚀 DÉPLOIEMENT RAPIDE

```bash
# Cloner
git clone https://github.com/kioka8877-ux/PERTURABO
cd PERTURABO/MONDES_FORGES/CLIPPING

# Vérifier l'état
python F06_DIRECTOR/CODEBASE/director.py --help

# Lancer F06_DIRECTOR
python F06_DIRECTOR/CODEBASE/director.py F03_OUT/segment.json F04_OUT/text_payload.json context.json

# Extraire les patterns
python F06_DIRECTOR/CODEBASE/pattern_extractor.py
```

---

## 📝 NOTES

- **Mode PUR** : le streamer Whop fournit le podcast + clip ref
- **F06_DIRECTOR** : ne touche jamais à la vidéo, produit des instructions
- **ARCHIVUM/montage/** : s'enrichit avec chaque campagne
- **Patterns** : extraits des transcripts de tutos montage YouTube

---

*"Fer au-dedans, Fer au-dehors. Aucune hérésie ne survivra au siège."* 🔩
