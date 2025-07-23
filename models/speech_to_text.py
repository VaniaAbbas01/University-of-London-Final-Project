import whisper


def loadModel():
    """Load the OpenAI Whisper model."""
    print("Loading OpenAI Whisper model...")
    return whisper.load_model("small")  


def transcribeAudio(model, audio_path):
    """Transcribe audio using the OpenAI Whisper model."""
    print(f"Transcribing audio file: {audio_path}")
    result = model.transcribe(audio_path)
    return result["text"].strip().lower()

