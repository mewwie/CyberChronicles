import os
import unittest
from app import app
from unittest.mock import patch
import io

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        # Create uploads folder if it doesn't exist
        if not os.path.exists('uploads'):
            os.makedirs('uploads')

    def tearDown(self):
        # Clean up created files
        for item in os.listdir('uploads'):
            os.remove(os.path.join('uploads', item))

    def test_index_page(self):
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'PII Redaction Service', result.data)

    def test_redact_text_success(self):
        with patch('app.redact_pii') as mock_redact:
            mock_redact.return_value = ('Redacted text', False)
            result = self.app.post('/redact', data={'text': 'My email is test@example.com'})
            self.assertEqual(result.status_code, 200)
            self.assertIn(b'Redacted text', result.data)
            mock_redact.assert_called_once()

    def test_redact_text_error(self):
        with patch('app.redact_pii') as mock_redact:
            mock_redact.return_value = ('Original text', True)
            result = self.app.post('/redact', data={'text': 'My email is test@example.com'})
            self.assertEqual(result.status_code, 200)
            # Check that the error file was created
            self.assertTrue(any(f.endswith('_error.txt') for f in os.listdir('uploads')))

    def test_redact_file_success(self):
        with patch('app.redact_pii') as mock_redact:
            mock_redact.return_value = ('Redacted file content', False)
            data = {'file': (io.BytesIO(b'My email is test@example.com'), 'test.txt')}
            result = self.app.post('/redact', data=data, content_type='multipart/form-data')
            self.assertEqual(result.status_code, 200)
            self.assertIn(b'Redacted file content', result.data)
            # Check that the uploaded file was deleted
            self.assertEqual(len(os.listdir('uploads')), 0)

    def test_redact_file_error(self):
        with patch('app.redact_pii') as mock_redact:
            mock_redact.return_value = ('Original file content', True)
            data = {'file': (io.BytesIO(b'My email is test@example.com'), 'test.txt')}
            result = self.app.post('/redact', data=data, content_type='multipart/form-data')
            self.assertEqual(result.status_code, 200)
            # Check that the uploaded file was saved
            self.assertEqual(len(os.listdir('uploads')), 1)
            self.assertTrue(os.path.exists('uploads/test.txt'))

if __name__ == '__main__':
    unittest.main()
