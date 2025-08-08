# backend/tests/test_redactor.py
import unittest
import sys
import os

# Add the parent directory to the path to allow imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from redactor import redact_pii

class TestRedactor(unittest.TestCase):

    def test_redact_email(self):
        text = "Contact me at test@example.com"
        expected = "Contact me at [REDACTED_EMAIL]"
        self.assertEqual(redact_pii(text), expected)

    def test_redact_phone(self):
        text = "My number is 123-456-7890"
        expected = "My number is [REDACTED_PHONE]"
        self.assertEqual(redact_pii(text), expected)

    def test_no_pii(self):
        text = "This text has no PII."
        self.assertEqual(redact_pii(text), text)

if __name__ == '__main__':
    unittest.main()
