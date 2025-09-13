import whisper

class Transcription:
    def __init__(self):
        self.model = self.loadModel()

    # load the OpenAI Whisper model
    def loadModel(self):
        """Load the OpenAI Whisper model."""
        return whisper.load_model("base")

    # Transcribe audio using the OpenAI Whisper model
    def transcribeAudio(self, audio_path):
        """Transcribe audio using the OpenAI Whisper model."""
        print(f"Transcribing audio file: {audio_path}")
        result = self.model.transcribe(audio_path)
        transcription = result["text"].strip().lower()

        # Empty or silent audio
        if not transcription: 
            raise ValueError("Audio is silent or contains no transcribable speech.")

        return transcription

