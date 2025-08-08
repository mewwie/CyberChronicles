import unittest
import sys
import os

# Add the parent directory to the path to allow imports
# This allows the test to be run from the root directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from redactor import redact_text, NLP

class TestRedactor(unittest.TestCase):

    def test_redact_email(self):
        text = "Contact me at test@example.com."
        expected = "Contact me at [REDACTED]."
        self.assertEqual(redact_text(text), expected)

    def test_redact_phone(self):
        text = "My number is +14155552671."
        expected = "My number is [REDACTED]."
        self.assertEqual(redact_text(text), expected)

    def test_redact_iban(self):
        text = "Transfer to NL20INGB0001234567."
        expected = "Transfer to [REDACTED]."
        self.assertEqual(redact_text(text), expected)

    def test_redact_credit_card(self):
        text = "Card number: 4111111111111111."
        expected = "Card number: [REDACTED]."
        self.assertEqual(redact_text(text), expected)

    def test_mask_mode(self):
        text = "My email is a@b.co and my phone is +12345678901."
        expected = "My email is XXXXXX and my phone is XXXXXXXXXXXX."
        options = {'mode': 'mask'}
        self.assertEqual(redact_text(text, options), expected)

    def test_mask_mode_with_custom_char(self):
        text = "My email is a@b.co."
        expected = "My email is ######."
        options = {'mode': 'mask', 'mask_char': '#'}
        self.assertEqual(redact_text(text, options), expected)

    @unittest.skipIf(NLP is None, "spaCy model not loaded")
    def test_ner_redaction_person(self):
        text = "My name is John Smith."
        expected = "My name is [REDACTED]."
        self.assertEqual(redact_text(text), expected)

    @unittest.skipIf(NLP is None, "spaCy model not loaded")
    def test_ner_redaction_location(self):
        text = "I live in New York."
        expected = "I live in [REDACTED]."
        self.assertEqual(redact_text(text), expected)

    @unittest.skipIf(NLP is None, "spaCy model not loaded")
    def test_regex_priority_over_ner(self):
        # "New York" is a GPE, but "york@example.com" should be redacted by regex first.
        text = "Contact New York office at york@example.com."
        expected = "Contact [REDACTED] office at [REDACTED]."
        # The NER redaction for "New York" should not create a nested or overlapping redaction.
        # Our implementation should handle this gracefully.
        self.assertEqual(redact_text(text), expected)

    def test_no_pii(self):
        text = "This is a simple sentence."
        self.assertEqual(redact_text(text), text)

if __name__ == '__main__':
    unittest.main()
