# MODAL — DEPLOYER (transcription GPU F00B_VOX)

> L'Oreille Absolue transcrit sur GPU Modal au lieu du CPU local.
> Ce guide permet a UN NOUVEL OPERATEUR de redployer le service depuis zero,
> y compris avec un NOUVEAU compte Modal (credits gratuits a rotation).

---

## 1. Creer / recuperer un compte Modal

1. Aller sur https://modal.com et creer un compte (les credits gratuits ~$1 sont credites).
2. Installer le CLI :
   ```bash
   pip install modal
   ```
3. S'authentifier :
   ```bash
   modal setup
   # ou, avec un token API cree dans le dashboard (Settings -> API Tokens) :
   modal token set --token-id <ID> --token-secret <SECRET>
   ```

## 2. Deployer le service

Depuis la racine du repo :

```bash
cd MONDES_FORGES/CLIPPING/F00_IRON_SENTINEL/F00B_VOX/MODAL
modal deploy transcribe.py
```

Modal affiche l'URL du service, du type :
`https://<workspace>--perturabo-whisper.modal.run`

> Le modele est `medium` par defaut. Pour changer : `WHISPER_MODEL=large-v3 modal deploy transcribe.py`
> (large-v3 = meilleur, plus lent/plus cher ; medium = equilibre, c'est le choix par defaut).

## 3. Pointer F00B_VOX sur Modal

Editer `f00b_secrets.json` (gitignore — ne JAMAIS commiter) :

```json
{
  "env_var_name": "MODAL_TOKEN",
  "model_id": "medium",
  "provider": "other",
  "base_url": "https://<workspace>--perturabo-whisper.modal.run",
  "language": "en",
  "fallback_env_var": "AI_GATEWAY_API_KEY"
}
```

Puis exporter le token dans l'environnement de la machine du Warsmith :

```bash
export MODAL_TOKEN="<token-secret>"
```

> f00b_vox n'a besoin d'AUCUNE modification de code : `PremiumTranscriber`
> lit cette config et envoie deja le multipart `/audio/transcriptions` attendu.

## 4. Test rapide

```bash
curl -X POST https://<workspace>--perturabo-whisper.modal.run/audio/transcriptions \
  -F "file=@/tmp/test.m4a" -F "language=en"
# -> {'words': [{'word': '...', 'start': ..., 'end': ...}, ...], 'text': '...'}
```

## 5. Notes operateur

- **Aucun secret dans le repo.** Le token modal (MODAL_TOKEN) est env-only.
- **Rotation de compte** : quand les credits gratuits sont epuises, refaire les etapes 1 a 3
  avec un nouveau compte, puis re-pointer `base_url`. Le code ne change pas.
- **Budget** : 105 min d'audio sur `medium` (T4) ~ quelques centimes, bien sous les $1 gratuits.
- **VAD** : le service active `vad_filter=True` (ignore silences/musique) — utile pour les
  VOD Twitch dont l'audio est partiellement mute (segments "index-muted").
