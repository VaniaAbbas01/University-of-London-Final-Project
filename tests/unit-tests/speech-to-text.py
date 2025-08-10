import unittest
import os
from models.speech_to_text import Transcription

transcription = Transcription()

class TestSpeechRecognition(unittest.TestCase):
    """Unit tests for the speech-to-text transcription functionality."""
    def setUp(self):
        # Path to your sample audio files
        self.valid_audio = os.path.join("tests", "audio_samples", "hello.wav")
        self.invalid_audio = os.path.join("tests", "audio_samples", "corrupted.wav")  # optional
        self.silence_audio = os.path.join("tests", "audio_samples", "silence.wav")    # optional

    def test_transcription_valid_audio(self):
        """Test transcription of a valid audio file."""
        transcript = transcription.transcribe_audio(self.valid_audio)
        self.assertIsInstance(transcript, str)
        self.assertIn("hello", transcript.lower())  # Adjust based on known content

    def test_transcription_empty_file(self):
        """Test behavior when transcribing a silent or empty audio."""
        with self.assertRaises(ValueError):  # or your app's specific exception
            transcription.transcribe_audio(self.silence_audio)

    def test_transcription_invalid_format(self):
        """Test handling of corrupted or invalid audio format."""
        with self.assertRaises(Exception):  # or your custom exception
            transcription.transcribe_audio(self.invalid_audio)


if __name__ == '__main__':
    unittest.main()
