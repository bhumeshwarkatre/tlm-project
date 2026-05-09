import time
import random
from config import MIN_DELAY, MAX_DELAY


def random_delay():
    """
    Human-like random delay
    """
    delay = random.uniform(MIN_DELAY, MAX_DELAY)
    time.sleep(delay)


def safe_print(message):
    print(f"[INFO] {message}")