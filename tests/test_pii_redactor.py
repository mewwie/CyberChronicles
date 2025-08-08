import unittest
import re
from unittest.mock import patch, MagicMock
from pii_redactor import redact_pii

class TestPiiRedactor(unittest.TestCase):

    def test_redact_email(self):
        text = "My email is test@example.com"
        redacted_text = redact_pii(text, "test_chat_id")
        self.assertNotEqual(text, redacted_text)
        self.assertFalse(re.search(r'test@example.com', redacted_text))

    def test_redact_phone_number(self):
        text = "My phone number is 123-456-7890"
        redacted_text = redact_pii(text, "test_chat_id")
        self.assertNotEqual(text, redacted_text)
        self.assertFalse(re.search(r'123-456-7890', redacted_text))

    def test_redact_name(self):
        text = "My name is John Doe."
        redacted_text = redact_pii(text, "test_chat_id")
        self.assertNotEqual(text, redacted_text)
        self.assertFalse(re.search(r'John', redacted_text))

    def test_no_pii(self):
        text = "There is no PII here."
        redacted_text = redact_pii(text, "test_chat_id")
        self.assertTrue(len(redacted_text) > 0)

    @patch('pii_redactor.fake.email', MagicMock(side_effect=Exception("Faker error")))
    @patch('pii_redactor.error_logger.error')
    def test_logging_on_failure(self, mock_logger_error):
        chat_id = "test_log_chat_id"
        text = "My email is test@example.com"
        redact_pii(text, chat_id)

        mock_logger_error.assert_called_once()
        call_args, _ = mock_logger_error.call_args
        log_message = call_args[0]
        self.assertIn(f"Chat ID: {chat_id}", log_message)
        self.assertIn("Placeholder: email", log_message)
        self.assertIn("Error: Faker error", log_message)

if __name__ == '__main__':
    unittest.main()
