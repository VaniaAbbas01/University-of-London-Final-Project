import io
import unittest
from unittest.mock import patch
from main import app

class FlaskFunctionalTests(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    @patch("main.Transcription")
    def test_upload_audio(self, mock_transcription):
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

    @patch("main.SpeechToEmotion")
    @patch("main.GrammarCorrection")
    def test_analyse_route(self, mock_grammar, mock_emotion):
        # Mock GrammarCorrection
        mock_grammar.return_value.correctGrammar.return_value = "Corrected sentence."
        # Mock SpeechToEmotion
        mock_emotion.return_value.predictEmotion.return_value = "Happy"
        # Set session values first (Flask test_client supports this with session_transaction)
        with self.client.session_transaction() as sess:
            sess["audioPath"] = "./uploads/sample.mp3"
            sess["audioDuration"] = 10
        # Send form-data (not JSON!)
        response = self.client.post(
            "/analyse",
            data={"transcription": "I is happy"},
            content_type="multipart/form-data"
        )
        # Assert
        self.assertEqual(response.status_code, 200)
        # Since it's HTML, check text inside response
        html = response.data.decode("utf-8")
        self.assertIn("Corrected sentence.", html)
        self.assertIn("Happy", html)
        # Ensure mocks were called
        mock_emotion.return_value.predictEmotion.assert_called_once_with("./uploads/sample.mp3")
        mock_grammar.return_value.correctGrammar.assert_called_once_with("I is happy")



if __name__ == "__main__":
    unittest.main()
