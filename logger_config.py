import logging
import os

def setup_logger():
    """
    Sets up a logger for GDPR compliance.
    """
    logger = logging.getLogger('gdpr_compliance')

    # Avoid adding handlers multiple times if the logger is already configured
    if logger.hasHandlers():
        # Clear existing handlers to ensure a clean state for tests
        logger.handlers.clear()

    logger.setLevel(logging.ERROR)

    if not os.path.exists('logs'):
        os.makedirs('logs')

    handler = logging.FileHandler('logs/gdpr_compliance.log')
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger

# Initialize the logger
error_logger = setup_logger()
