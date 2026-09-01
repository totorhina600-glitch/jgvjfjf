# ARCHIVUM/broll/

Bibliothèque de B-roll pour le mode PUR.

## Structure

```
broll/
├── stock/              ← Clips images génériques (Pexels, Pixabay)
├── ai_generated/       ← B-roll générés par IA
├── campaign_assets/    ← B-roll fournis par les campagnes Whop
└── README.md
```

## Sources

| Source | Priorité | Usage |
|--------|----------|-------|
| Campaign assets | 1 (toujours en priorité) | Clips fournis par le streamer |
| AI generated | 2 (backup) | 1-2 clips max par vidéo |
| Stock footage | 3 (dernier recours) | Assets génériques |

## Règles

- **Hook (0-3s)** : pas de B-roll, visage du speaker
- **Après le hook** : 1 B-roll toutes les 7-10 secondes
- **Max** : 3 B-roll pour un clip de 30s, 5 pour 60s
- **Jamais** pendant le moment émotionnel le plus intense

## Format

Chaque B-roll doit avoir :
- Un fichier vidéo/image
- Une durée cible (2-3 secondes)
- Un contexte d'utilisation (pour quel moment du clip)
