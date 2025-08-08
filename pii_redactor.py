import re
from faker import Faker
from logger_config import error_logger

fake = Faker()

def redact_pii(text, chat_id):
    """
    Redacts PII from the given text and logs any errors.
    Returns a tuple of (redacted_text, has_error).
    """
    has_error = False
    try:
        # Redact email addresses
        text = re.sub(r'\S+@\S+', lambda m: f"<{fake.email().split('@')[0]}>", text)
    except Exception as e:
        error_logger.error(
            f"Chat ID: {chat_id} - Placeholder: email - "
            f"Error: {e} - Cause: Failed to generate or substitute email placeholder."
        )
        has_error = True

    try:
        # Redact phone numbers
        text = re.sub(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', lambda m: f"<{fake.phone_number().split('x')[0].strip()}>", text)
    except Exception as e:
        error_logger.error(
            f"Chat ID: {chat_id} - Placeholder: phone_number - "
            f"Error: {e} - Cause: Failed to generate or substitute phone number placeholder."
        )
        has_error = True

    try:
        # Redact names (simple approach)
        def repl(m):
            return f'<{fake.first_name()}>'
        text = re.sub(r'(?<=\s)[A-Z][a-z]+', repl, text)
    except Exception as e:
        error_logger.error(
            f"Chat ID: {chat_id} - Placeholder: name - "
            f"Error: {e} - Cause: Failed to generate or substitute name placeholder."
        )
        has_error = True

    return text, has_error
