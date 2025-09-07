import io
import unittest
from unittest.mock import patch
from main import create_app

class FlaskFunctionalTests(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True

    # testing upload route with mocked Transcription class
    @patch("routes.uploadRoute.Transcription")
    def test_upload_audio(self, mock_transcription):
        """ Tests if the Upload Route transcribes text"""
        # Mock transcription behavior 
        mock_instance = mock_transcription.return_value
        mock_instance.transcribeAudio.return_value = "mock transcription"

        # Create fake audio file
        fake_audio = (io.BytesIO(b"fake audio content"), "test.mp3")
        response = self.client.post(
            "/upload",
            data={"audio": fake_audio},
            content_type="multipart/form-data",
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"mock transcription", response.data)

    @patch("routes.analysisRoute.generate_feedback")
    def test_analyse_route(self, mock_feedback):
        """Tests if the analyse route returns with an HTML Page"""

        # mock feedbaclk data
        mock_feedback.return_value = (
            {
                "transcription": "I is happy",
                "fluency": {
                    "words_per_minute": 120,
                    "filler_words": 3,
                    "pauses": 1.25,
                    "vocabulary_richness": 0.85
                },
                "tone": "Happy",
                "feedback": [
                    {"type": "Grammar", "suggestion": "Consider subject-verb agreement."},
                    {"type": "Pacing", "suggestion": "Try to reduce pauses."}
                ],
                "audio": {
                    "features": {
                        "avg_pitch": 115.5,
                        "pitch_var": 12.3,
                        "avg_loudness_db": -20.5,
                        "speech_rate": 3.5,
                        "pause_ratio": 0.12,
                        "jitter": 0.0045,
                        "shimmer": 0.0078,
                        "hnr": 18.2
                    }
                }
            },
            {
                "pitch_series": [
                    {"time": 0.0, "value": 100},
                    {"time": 1.0, "value": 110},
                    {"time": 2.0, "value": 120}
                ],
                "intensity_series": [
                    {"time": 0.0, "value": 0.5},
                    {"time": 1.0, "value": 0.7},
                    {"time": 2.0, "value": 0.9}
                ]
            }
        )

        with self.client.session_transaction() as sess:
            sess["audioPath"] = "./uploads/sample.mp3"
            sess["audioDuration"] = 10

        response = self.client.post(
            "/analyse",
            data={"transcription": "I is happy"},
            content_type="multipart/form-data"
        )

        self.assertEqual(response.status_code, 200)
        html = response.data.decode("utf-8")
        self.assertIn("Happy", html)
        self.assertIn("120", html)

        mock_feedback.assert_called_once_with("I is happy", "./uploads/sample.mp3", 10)


if __name__ == "__main__":
    unittest.main()
