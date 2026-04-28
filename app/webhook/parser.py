import requests
import os
import tempfile
import subprocess
from dotenv import load_dotenv
import whisper


load_dotenv()
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")

model = whisper.load_model("small")


def get_audio_url(media_id: str) -> str:
    """Obtiene una URL fresca del audio usando el media_id"""
    r = requests.get(
        f"https://graph.facebook.com/v18.0/{media_id}",
        headers={"Authorization": f"Bearer {WHATSAPP_TOKEN}"}
    )
    r.raise_for_status()
    return r.json()["url"]

def transcribe_audio(media_id: str) -> str:
    """Descarga y transcribe el audio de WhatsApp"""
    
    url = get_audio_url(media_id)

    # Descarga del audio
    response = requests.get(
        url, headers={"Authorization": f"Bearer {WHATSAPP_TOKEN}"}
    )
    response.raise_for_status()
    audio_bytes = response.content

    if len(audio_bytes) == 0:
        raise ValueError("El audio descargado está vacío, la URL puede haber expirado")

    # Convertir OGG/Opus a WAV con ffmpeg usando archivos temporales
    with tempfile.NamedTemporaryFile(suffix=".ogg", delete=False) as ogg_file:
        ogg_file.write(audio_bytes)
        ogg_path = ogg_file.name

    wav_path = ogg_path.replace(".ogg", ".wav")

    try:
        subprocess.run([
            "ffmpeg", "-y",
            "-i", ogg_path,
            "-ar", "16000", # 16kHz que necesita Whisper
            "-ac", "1", # mono
            wav_path
        ], check=True, capture_output=True)


        result = model.transcribe(wav_path, language="es")
        return result["text"]

    finally:
        os.unlink(ogg_path)
        if os.path.exists(wav_path):
            os.unlink(wav_path)


def parser_message(message: dict):
    try:
        if message["type"] == "audio":
            media_id = message["audio"]["id"]
            return transcribe_audio(media_id)

        elif message["type"] == "text":
            return message["text"]["body"]

        else:
            return None

    except Exception as e:
        raise ValueError(f"Hubo un error obteniendo los datos: {e}")
