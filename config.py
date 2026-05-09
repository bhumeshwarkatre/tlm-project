import os

# -----------------------------
# General Settings
# -----------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, "data")
LOG_DIR = os.path.join(BASE_DIR, "logs")
SESSION_DIR = os.path.join(BASE_DIR, "browser_session")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(SESSION_DIR, exist_ok=True)

# -----------------------------
# CSV Files
# -----------------------------

COMPANIES_CSV = os.path.join(DATA_DIR, "companies.csv")
FAILED_CSV = os.path.join(DATA_DIR, "failed_domains.csv")
RAW_CSV = os.path.join(DATA_DIR, "raw_companies.csv")

# -----------------------------
# Browser Session
# -----------------------------

SESSION_FILE = os.path.join(SESSION_DIR, "session.json")

# -----------------------------
# TLM Safe Mode Settings
# -----------------------------

MAX_TABS = 3
BATCH_SIZE = 10

MIN_DELAY = 2
MAX_DELAY = 4

TLM_WAIT_TIMEOUT = 8000  # milliseconds
TLM_RETRY_COUNT = 1

# -----------------------------
# Google Maps Search Keywords
# -----------------------------

DEFAULT_KEYWORDS = [
    "construction company usa",
    # "software company",
    # "marketing agency",
    # "consulting firm",
    # "startup"
]

# -----------------------------
# Invalid Domain Filters
# -----------------------------

INVALID_DOMAIN_KEYWORDS = [
    "facebook",
    "instagram",
    "linkedin",
    "yelp",
    "justdial",
    "wixsite",
    "wordpress",
    "blogspot",
    "gmail",
    "yahoo"
]

# TLM MULTI TAB
# -----------------------------------

TLM_TAB_COUNT = 5