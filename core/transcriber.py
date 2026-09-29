import os

import whisper


WHISPER_MODEL = os.getenv("WHISPER_MODEL", "small")

_model = None


def load_model():
    global _model

    if _model is None:
        print(f"Loading Whisper model: {WHISPER_MODEL} ...")
        _model = whisper.load_model(WHISPER_MODEL)
        print("Whisper model loaded.")

    return _model


def transcribe_chunk(chunk_path: str, language: str = "english") -> str:
    model = load_model()

    task = "translate" if language.lower() == "hinglish" else "transcribe"

    result = model.transcribe(
        chunk_path,
        task=task
    )

    return result["text"].strip()


def transcribe_all(chunks: list[str], language: str = "english") -> str:
    transcripts = []

    engine = "Whisper translation" if language.lower() == "hinglish" else "Whisper"
    print(f"Using {engine} for transcription.")

    for i, chunk in enumerate(chunks):
        print(f"Transcribing chunk {i + 1}/{len(chunks)}...")

        text = transcribe_chunk(chunk, language=language)
        transcripts.append(text)

    print("Transcription complete.")

    return " ".join(transcripts)