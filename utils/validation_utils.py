import logging
from email.utils import parseaddr

# Configure logging (optional, you can configure globally in Django setting)
logger = logging.getLogger(__name__)

def is_valid_email(email: str) -> bool:
    """
    Validate an email address using Python's built-in email parsing.
    Returns True if valid, False otherwise.
    """
    try:
        if not email or "@" not in email:
            return False
        
        # parseaddr returns (realname, email_address)
        realname, parsed_email = parseaddr(email)

        # Basic validation: must contain "@" and non-empty local/domain parts
        if parsed_email and "@" in parsed_email:
            local, domain = parsed_email.split("@", 1)
            if local and domain:
                return True
        return False
    
    except Exception as e:
        logger.error(f"Error validating email '{email}': {e}")
        return False