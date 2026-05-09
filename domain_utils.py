# from urllib.parse import urlparse
# from config import INVALID_DOMAIN_KEYWORDS


# def clean_domain(url):
#     """
#     Convert full URL to root domain
#     """
#     try:
#         if not url:
#             return None

#         parsed = urlparse(url)
#         domain = parsed.netloc.lower()

#         if not domain:
#             domain = parsed.path.lower()

#         domain = domain.replace("www.", "").strip()

#         if is_invalid_domain(domain):
#             return None

#         return domain

#     except Exception:
#         return None


# def is_invalid_domain(domain):
#     """
#     Filter unwanted domains
#     """
#     for bad in INVALID_DOMAIN_KEYWORDS:
#         if bad in domain:
#             return True
#     return False

from urllib.parse import urlparse
import re
from config import INVALID_DOMAIN_KEYWORDS


def clean_domain(url):
    """
    Convert full URL to clean root domain

    Fixes:
    - adds scheme if missing
    - removes www
    - removes trailing dots (IMPORTANT)
    - removes paths, query, fragments
    - filters invalid domains
    """

    try:
        if not url:
            return None

        url = url.strip()

        # ---------------------------
        # Ensure scheme exists
        # ---------------------------
        if not url.startswith(("http://", "https://")):
            url = "http://" + url

        parsed = urlparse(url)

        domain = parsed.netloc.lower()

        # fallback if netloc empty
        if not domain:
            domain = parsed.path.lower()

        # ---------------------------
        # CLEAN DOMAIN
        # ---------------------------
        domain = domain.replace("www.", "")

        # 🔥 REMOVE TRAILING DOTS / GARBAGE
        domain = domain.strip().strip(".")

        # remove spaces
        domain = domain.strip()

        # remove unwanted characters
        domain = re.sub(r"[^a-z0-9\.-]", "", domain)

        # ---------------------------
        # BASIC VALIDATION
        # ---------------------------
        if not domain or "." not in domain:
            return None

        # ---------------------------
        # FILTER INVALID DOMAINS
        # ---------------------------
        if is_invalid_domain(domain):
            return None

        # ---------------------------
        # BLOCK FILE TYPES (IMPORTANT)
        # ---------------------------
        invalid_extensions = [
            ".png", ".jpg", ".jpeg",
            ".gif", ".svg", ".webp",
            ".css", ".js", ".pdf"
        ]

        for ext in invalid_extensions:
            if domain.endswith(ext):
                return None

        return domain

    except Exception:
        return None


def is_invalid_domain(domain):
    """
    Filter unwanted domains
    """
    for bad in INVALID_DOMAIN_KEYWORDS:
        if bad in domain:
            return True
    return False