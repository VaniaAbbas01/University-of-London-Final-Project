import unittest
import os
from features.speech_to_text import Transcription

transcription = Transcription()

class TestSpeechRecognition(unittest.TestCase):
    """Unit tests for the speech-to-text transcription functionality."""

    # Setting up paths to audio files for testing
    def setUp(self):
        # Path to your sample audio files
        base_dir = os.path.dirname(os.path.abspath(__file__))  # points to unit-tests/
        uploads_dir = os.path.join(base_dir, "uploads")

        self.valid_audio = os.path.join(uploads_dir, "hello.mp3")
        self.silence_audio = os.path.join(uploads_dir, "silence.mp3")

    # test case for transcription of valid audio
    def test_transcription_valid_audio(self):
        """Test transcription of a valid audio file."""
        transcript = transcription.transcribeAudio(self.valid_audio)
        self.assertIsInstance(transcript, str)
        self.assertIn("hello", transcript.lower())

    # test case for transcription of empty or silent audio
    def test_transcription_empty_file(self):
        """Test behavior when transcribing a silent or empty audio."""
        with self.assertRaises(ValueError): 
            transcription.transcribeAudio(self.silence_audio)

if __name__ == '__main__':
    unittest.main()
