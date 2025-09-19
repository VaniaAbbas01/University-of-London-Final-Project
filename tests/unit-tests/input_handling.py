import io
import unittest
from unittest.mock import patch, MagicMock
from main import create_app

class UploadRouteTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SECRET_KEY'] = "test_secret"
        self.client = self.app.test_client()

    # helper function to upload audio
    def upload_file(self, filename="test.mp3", content=b"dummy data",
                    follow_redirects=False):
        """Helper to simulate a file upload."""
        data = {"audio": (io.BytesIO(content), filename)}
        return self.client.post(
            "/upload",
            data=data,
            content_type="multipart/form-data",
            follow_redirects=follow_redirects
        )

    # testing no file uploaded
    def test_no_file_uploaded(self):
        """Should redirect to index when no file is in request."""
        response = self.client.post("/upload", data={})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.location.endswith("/"))

    # testing empty filename
    def test_empty_filename(self):
        """Should redirect to index when filename is empty."""
        response = self.upload_file(filename="")
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.location.endswith("/"))

    # testing invalid file type
    def test_invalid_file_type(self):
        """Should return 400 for invalid file type."""
        with patch("routes.uploadRoute.allowed_file", return_value=False):
            response = self.upload_file(filename="test.txt")
            self.assertEqual(response.status_code, 400)
            self.assertIn(b"Invalid file type", response.data)

    @patch("routes.uploadRoute.allowed_file", return_value=True)
    @patch("routes.uploadRoute.Transcription")
    @patch("routes.uploadRoute.find_audio_duration", return_value=3.5)
    def test_valid_file_upload(self, mock_duration, mock_transcription_class, mock_allowed_file):
        """Should process and render transcription for valid file."""
        mock_instance = MagicMock()
        mock_instance.transcribeAudio.return_value = "This is a test transcription"
        mock_transcription_class.return_value = mock_instance

        response = self.upload_file()
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"This is a test transcription", response.data)

    @patch("routes.uploadRoute.allowed_file", return_value=True)
    @patch("routes.uploadRoute.Transcription")
    @patch("routes.uploadRoute.find_audio_duration", return_value=3.5)
    def test_exception_during_transcription(self, mock_duration, mock_transcription_class, mock_allowed_file):
        """Should handle exceptions during transcription gracefully."""
        
        # Mock transcription to raise exception
        mock_instance = MagicMock()
        mock_instance.transcribeAudio.side_effect = Exception("Transcription failed")
        mock_transcription_class.return_value = mock_instance

        response = self.upload_file()

        # Acceptable outcomes depending on your route logic
        self.assertIn(response.status_code, (200, 302, 400))

        # If your app flashes "Transcription failed", check it in response
        html = response.data.decode("utf-8")
        self.assertTrue(
            "Transcription failed" in html or "Error" in html or response.status_code in (302, 400)
        )

if __name__ == "__main__":
    unittest.main()
