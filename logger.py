import logging
import os
from config import LOG_DIR

LOG_FILE = os.path.join(LOG_DIR, "app.log")


def setup_logger():
    logger = logging.getLogger("TLMBot")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        file_handler = logging.FileHandler(LOG_FILE)
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


logger = setup_logger()