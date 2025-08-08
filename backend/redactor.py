# backend/redactor.py
import re

def redact_text(text):
    """
    A simple PII redactor.
    This is a placeholder and should be replaced with a more robust implementation.
    """
    # Redact email addresses
    text = re.sub(r'\S+@\S+', '[REDACTED_EMAIL]', text)
    # Redact phone numbers
    text = re.sub(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', '[REDACTED_PHONE]', text)

    return text
