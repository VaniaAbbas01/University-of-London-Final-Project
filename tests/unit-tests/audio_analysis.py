import unittest
import numpy as np
import librosa
import tempfile
import soundfile as sf
from features.audio_analysis import AudioAnalyser


class TestAudioAnalyser(unittest.TestCase):

    def setUp(self):
        # Create a short synthetic sine wave audio file for testing
        self.sr = 22050
        duration = 1.0
        t = np.linspace(0, duration, int(self.sr * duration), endpoint=False)
        sine_wave = 0.5 * np.sin(2 * np.pi * 220 * t)

        # Save to a temporary WAV file
        self.temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        sf.write(self.temp_wav.name, sine_wave, self.sr)

        self.analyser = AudioAnalyser(self.temp_wav.name)

    def tearDown(self):
        # Cleanup
        self.temp_wav.close()

    # tests extractFeatures function
    def test_extractFeatures_runs(self):
        """Ensure extractFeatures runs and returns required keys"""
        results = self.analyser.extractFeatures()
        self.assertIn("features", results)
        self.assertIn("feedback", results)
        self.assertIn("pitch_series", results)
        self.assertIn("intensity_series", results)

    # tests if empty audio raises error
    def test_empty_audio_raises_error(self):
        """Ensure empty audio raises ValueError"""
        empty_audio = np.zeros(22050)
        temp_silence = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        sf.write(temp_silence.name, empty_audio, self.sr)

        analyser = AudioAnalyser(temp_silence.name)
        with self.assertRaises(ValueError):
            analyser.extractFeatures()

    # tests for low pitch
    def test_interpretFeatures_low_pitch(self):
        """Test feedback for low pitch"""
        f = {
            "avg_pitch": 80,
            "pitch_var": 25,
            "avg_loudness_db": -20,
            "speech_rate": 3,
            "pause_ratio": 0.1,
            "jitter": 0.01,
            "shimmer": 0.02,
            "hnr": 15
        }
        feedback = self.analyser.interpretFeatures(f)
        self.assertIn("low", feedback["pitch"].lower())

    # tests for high shimmer 
    def test_interpretFeatures_high_shimmer(self):
        """Test shimmer feedback"""
        f = {
            "avg_pitch": 150,
            "pitch_var": 30,
            "avg_loudness_db": -20,
            "speech_rate": 3,
            "pause_ratio": 0.1,
            "jitter": 0.01,
            "shimmer": 0.05,
            "hnr": 15
        }
        feedback = self.analyser.interpretFeatures(f)
        self.assertIn("shimmer", " ".join(feedback.values()).lower())

    # tests for a breathy voice
    def test_interpretFeatures_breathy_voice(self):
        """Test HNR feedback"""
        f = {
            "avg_pitch": 150,
            "pitch_var": 30,
            "avg_loudness_db": -20,
            "speech_rate": 3,
            "pause_ratio": 0.1,
            "jitter": 0.01,
            "shimmer": 0.02,
            "hnr": 5
        }
        feedback = self.analyser.interpretFeatures(f)
        self.assertIn("breathy", feedback["hnr"].lower())


if __name__ == "__main__":
    unittest.main()
