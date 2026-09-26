import os
import shlex
import subprocess
from pathlib import Path


def transcribe_audio(audio_path: str):
    command = os.getenv("LOCALBRIEF_WHISPER_COMMAND", "").strip()
    if not command:
        raise RuntimeError(
            "No Whisper command is configured. Set LOCALBRIEF_WHISPER_COMMAND to your "
            "Qualcomm AI Hub Whisper Windows runner."
        )

    cmd = command.replace("{audio}", str(Path(audio_path).resolve()))
    completed = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or "Whisper runner failed")
    transcript = completed.stdout.strip()
    if not transcript:
        raise RuntimeError("Whisper runner returned an empty transcript")
    return transcript
