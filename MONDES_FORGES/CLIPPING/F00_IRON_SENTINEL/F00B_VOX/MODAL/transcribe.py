"""
MODAL/transcribe.py — Service de transcription GPU pour F00B_VOX (l'Oreille Absolue)
======================================================================================
Endpoint OpenAI-compatible `/audio/transcriptions` consomme par
`auto_detector.PremiumTranscriber`.

Contrat d'entree (multipart/form-data, envoye par f00b_vox) :
  - file                    : audio (.m4a AAC)
  - model                   : ignore (modele fixe au deploy via WHISPER_MODEL)
  - language                : ex. "en"
  - response_format         : ignore (on renvoie TOUJOURS du word-level)
  - timestamp_granularities[]: ignore

Contrat de sortie (JSON) — format "Case 1" que VOX prefere pour le scoring :
  {"words": [{"word": "...", "start": 1.23, "end": 1.45}, ...], "text": "..."}

AUCUN secret dans ce fichier. Le token Modal se configure hors repo :
  modal token set --token-id <id> --token-secret <secret>

Deploy :
  modal deploy transcribe.py
L'URL est affichee par Modal ; la copier dans f00b_secrets.json -> base_url.
"""

import os

import modal
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

MODEL_NAME = os.environ.get("WHISPER_MODEL", "medium")
GPU = os.environ.get("WHISPER_GPU", "T4")

image = (
    modal.Image.debian_slim(python_version="3.11").pip_install(
        "faster-whisper==1.1.1",
        "fastapi==0.115.0",
        "uvicorn[standard]==0.30.6",
        "python-multipart==0.0.20",
    )
)

app = modal.App("perturabo-whisper")

web_app = FastAPI(title="PERTURABO Whisper (F00B_VOX)")

_model = None


def _get_model():
    global _model
    if _model is None:
        from faster_whisper import WhisperModel

        _model = WhisperModel(MODEL_NAME, device="cuda", compute_type="float16")
    return _model


@app.function(image=image, gpu=GPU, scaledown_window=120)
@modal.asgi_app()
def fastapi_app():
    return web_app


@web_app.get("/")
def health():
    return {"ok": True, "model": MODEL_NAME, "gpu": GPU}


@web_app.post("/audio/transcriptions")
async def transcribe(request: Request):
    form = await request.form()
    upload = form.get("file")
    if upload is None:
        return JSONResponse({"error": "champ 'file' manquant"}, status_code=400)

    data = await upload.read()
    language = form.get("language") or None

    import tempfile

    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(suffix=".m4a", delete=False) as f:
            f.write(data)
            tmp_path = f.name

        model = _get_model()
        segments, info = model.transcribe(
            tmp_path,
            language=language or None,
            word_timestamps=True,
            beam_size=5,
            vad_filter=True,
        )

        words = []
        for seg in segments:
            for w in getattr(seg, "words", None) or []:
                words.append(
                    {"word": w.word, "start": round(w.start, 3), "end": round(w.end, 3)}
                )

        text = " ".join(w["word"] for w in words).strip()
        return {
            "words": words,
            "text": text,
            "language": getattr(info, "language", language),
        }
    finally:
        if tmp_path:
            try:
                os.remove(tmp_path)
            except OSError:
                pass
