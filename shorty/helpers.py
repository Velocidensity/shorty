import random
import string
from urllib.parse import urlparse

CHARACTERS = string.ascii_letters + string.digits


def generate_stem(length: int = 5) -> str:
    """Generates a stem of desired length"""
    return ''.join([random.choice(CHARACTERS) for _ in range(length)])


def validate_url(url: str) -> bool:
    """Validates whether a given URL is a valid HTTP/HTTPS url"""
    try:
        parsed = urlparse(url)
    except (TypeError, ValueError):
        return False

    return parsed.scheme in ('http', 'https')
