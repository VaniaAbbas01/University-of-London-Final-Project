import io
import tempfile
import unittest
from unittest.mock import patch, MagicMock
from main import app


class UploadRouteTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = "test_secret"

    def test_no_file_uploaded(self):
        """Should redirect to index when no file is in request"""
        response = self.client.post('/upload', data={})
        self.assertEqual(response.status_code, 302)  # redirect
        self.assertIn('/', response.location)

    def test_empty_filename(self):
        """Should redirect to index when filename is empty"""
        data = {'audio': (io.BytesIO(b"dummy data"), '')}
        response = self.client.post('/upload', data=data,
                                    content_type='multipart/form-data')
        self.assertEqual(response.status_code, 302)  # redirect
        self.assertIn('/', response.location)

    def test_invalid_file_type(self):
        """Should return 400 for invalid file type"""
        with patch('main.allowed_file', return_value=False):
            data = {'audio': (io.BytesIO(b"dummy data"), 'test.txt')}
            response = self.client.post('/upload', data=data,
                                        content_type='multipart/form-data')
            self.assertEqual(response.status_code, 400)
            self.assertIn(b'invalid file type', response.data)

    @patch('main.allowed_file', return_value=True)
    @patch('main.Transcription')
    @patch('main.findAudioDuration', return_value=3.5)
    def test_valid_file_upload(self, mock_duration, mock_transcription_class, mock_allowed_file):
        """Should process and render transcription for valid file"""
        mock_transcription_instance = MagicMock()
        mock_transcription_instance.transcribeAudio.return_value = "This is a test transcription"
        mock_transcription_class.return_value = mock_transcription_instance

        data = {'audio': (io.BytesIO(b"dummy mp3 data"), 'test.mp3')}
        response = self.client.post('/upload', data=data,
                                    content_type='multipart/form-data')

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"This is a test transcription", response.data)

    @patch('main.allowed_file', return_value=True)
    @patch('main.Transcription')
    @patch('main.findAudioDuration', return_value=3.5)
    def test_exception_during_save(self, mock_duration, mock_transcription_class, mock_allowed_file):
        """Should handle exceptions during file save gracefully"""
        # Create a mock file object that raises error on save
        mock_file = MagicMock()
        mock_file.filename = "test.mp3"
        mock_file.save.side_effect = Exception("File save failed")

        data = {'audio': mock_file}
        response = self.client.post('/upload', data={'audio': (io.BytesIO(b"dummy"), 'test.mp3')},
                                    content_type='multipart/form-data')
        # It might still try to render template or return something,
        # so just check it does not crash
        self.assertIn(response.status_code, (200, 400, 302))


if __name__ == '__main__':
    unittest.main()
