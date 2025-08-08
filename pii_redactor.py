import re
from faker import Faker

fake = Faker()

def redact_pii(text):
    """
    Redacts PII from the given text.
    """
    # Redact email addresses
    text = re.sub(r'\S+@\S+', f"<{fake.email().split('@')[0]}>", text)

    # Redact phone numbers
    text = re.sub(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', f"<{fake.phone_number().split('x')[0].strip()}>", text)

    # Redact names (simple approach, might have false positives)
    # This is a simplistic approach and might redact words that are not names.
    # A more robust solution would involve NLP libraries like spaCy or NLTK.
    # For this example, we'll redact capitalized words that are not at the start of a sentence.
    def repl(m):
        return f'<{fake.first_name()}>'
    text = re.sub(r'(?<=\s)[A-Z][a-z]+', repl, text)

    return text
