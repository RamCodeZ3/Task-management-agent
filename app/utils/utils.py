import os
import subprocess
import tempfile
import whisper


model = whisper.load_model("small")


async def transcribe_audio_to_text(
        audio_bytes: bytes,
        original_filename: str = "audio"
    ) -> str:

    if len(audio_bytes) == 0:
        raise ValueError("The uploaded audio file is empty.")

    ext = os.path.splitext(original_filename)[-1].lower() or ".ogg"
    
    with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as tmp_input:
        tmp_input.write(audio_bytes)
        input_path = tmp_input.name

    wav_path = input_path.replace(ext, ".wav")

    try:
        subprocess.run([
            "ffmpeg", "-y",
            "-i", input_path,
            "-ar", "16000",
            "-ac", "1",
            wav_path
        ], check=True, capture_output=True)

        result = model.transcribe(wav_path, language="es")
        return result["text"]

    finally:
        os.unlink(input_path)
        if os.path.exists(wav_path):
            os.unlink(wav_path)

