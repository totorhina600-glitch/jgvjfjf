# 📋 NOTE D'INTÉGRATION — F06_DIRECTOR + Mode PUR

> **À l'attention du prochain sandbox / assistant**
> Ce fichier explique quoi intégrer et où.

---

## 🎯 Objectif

Intégrer **F06_DIRECTOR** (Le Directeur de Montage) et le **Mode PUR** dans le repository PERTURABO (`kioka8877-ux/PERTURABO`).

---

## 📦 Fichiers à intégrer

### Structure à créer dans PERTURABO

```
MONDES_FORGES/CLIPPING/
├── F06_DIRECTOR/                    ← NOUVEAU
│   ├── CODEBASE/
│   │   ├── director.py              ← Script principal (génère montage_instructions.json)
│   │   ├── pattern_extractor.py     ← Extrait patterns des transcripts tutos
│   │   └── requirements_f06.txt     ← Dépendances
│   ├── IN/.gitkeep
│   ├── OUT/.gitkeep
│   └── TRACKING/
│       └── F06_LOG.md               ← Journal
│
├── ARCHIVUM/
│   └── montage/                     ← NOUVEAU
│       ├── transcripts/.gitkeep     ← Vidéos tutos montage YouTube (à collecter)
│       ├── patterns/.gitkeep        ← Patterns extraits
│       ├── rules/
│       │   ├── youtube_shorts.md    ← Règles montage YouTube Shorts
│       │   ├── tiktok.md            ← Règles montage TikTok
│       │   └── instagram_reels.md   ← Règles montage Instagram Reels
│       └── examples/.gitkeep        ← Exemples clips réussis
│
├── README.md                        ← À REMPLACER (version avec mode pur)
└── liber_clipping.json              ← À REMPLACER (version avec F06)
```

### Fichiers à la racine du repo

```
CONTINUATION_F00.md                  ← À REMPLACER (version avec F06)
```

---

## 🔧 Comment intégrer

### Méthode 1 — Copie manuelle

```bash
# Clone PERTURABO
git clone https://github.com/kioka8877-ux/PERTURABO
cd PERTURABO

# Crée les dossiers
mkdir -p MONDES_FORGES/CLIPPING/F06_DIRECTOR/CODEBASE
mkdir -p MONDES_FORGES/CLIPPING/F06_DIRECTOR/TRACKING
mkdir -p MONDES_FORGES/CLIPPING/ARCHIVUM/montage/rules
mkdir -p MONDES_FORGES/CLIPPING/ARCHIVUM/montage/transcripts
mkdir -p MONDES_FORGES/CLIPPING/ARCHIVUM/montage/patterns
mkdir -p MONDES_FORGES/CLIPPING/ARCHIVUM/montage/examples

# Copie les fichiers depuis le repo source (totorhina600-glitch/jgvjfjf)
# Les fichiers sont dans la même structure
```

### Méthode 2 — API GitHub

Utilise la méthode `push_file()` avec un token pour copier fichier par fichier.

---

## 📝 Fichiers source (dans le repo totorhina600-glitch/jgvjfjf)

| Fichier source | Destination PERTURABO |
|----------------|----------------------|
| `F06_DIRECTOR/CODEBASE/director.py` | `MONDES_FORGES/CLIPPING/F06_DIRECTOR/CODEBASE/director.py` |
| `F06_DIRECTOR/CODEBASE/pattern_extractor.py` | `MONDES_FORGES/CLIPPING/F06_DIRECTOR/CODEBASE/pattern_extractor.py` |
| `F06_DIRECTOR/CODEBASE/requirements_f06.txt` | `MONDES_FORGES/CLIPPING/F06_DIRECTOR/CODEBASE/requirements_f06.txt` |
| `F06_DIRECTOR/TRACKING/F06_LOG.md` | `MONDES_FORGES/CLIPPING/F06_DIRECTOR/TRACKING/F06_LOG.md` |
| `ARCHIVUM/montage/rules/youtube_shorts.md` | `MONDES_FORGES/CLIPPING/ARCHIVUM/montage/rules/youtube_shorts.md` |
| `ARCHIVUM/montage/rules/tiktok.md` | `MONDES_FORGES/CLIPPING/ARCHIVUM/montage/rules/tiktok.md` |
| `ARCHIVUM/montage/rules/instagram_reels.md` | `MONDES_FORGES/CLIPPING/ARCHIVUM/montage/rules/instagram_reels.md` |
| `README.md` | `MONDES_FORGES/CLIPPING/README.md` (REMPLACER) |
| `CONTINUATION_F00.md` | `CONTINUATION_F00.md` (REMPLACER) |
| `liber_clipping.json` | `MONDES_FORGES/CLIPPING/liber_clipping.json` (REMPLACER) |

---

## ⚠️ Points importants

1. **Le README.md et liber_clipping.json sont des REMPLACEMENTS** — pas des ajouts
2. **Les dossiers .gitkeep** servent à maintenir la structure vide (Git ne suit pas les dossiers vides)
3. **ARCHIVUM/montage/transcripts/** est vide — il faut y ajouter des transcripts de tutos montage YouTube
4. **F06_DIRECTOR** est une frégate **passive** — elle ne touche jamais à la vidéo

---

## ✅ Checklist d'intégration

- [ ] Dossiers créés (F06_DIRECTOR, ARCHIVUM/montage)
- [ ] Fichiers Python copiés (director.py, pattern_extractor.py)
- [ ] Rules plateformes copiées (youtube_shorts.md, tiktok.md, instagram_reels.md)
- [ ] README.md remplacé
- [ ] CONTINUATION_F00.md remplacé
- [ ] liber_clipping.json remplacé
- [ ] Commit + Push
- [ ] Vérifier que `git status` est clean

---

## 🔗 Repository source

**URL** : https://github.com/totorhina600-glitch/jgvjfjf
**Branche** : main
**Commit** : `8baddf0` (feat: Add F06_DIRECTOR and mode PUR)

---

*"Fer au-dedans, Fer au-dehors. Le siège continue."* 🔩
