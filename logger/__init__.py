import logging
from datetime import datetime
import os

# Get the name of the current file
current_file = os.path.basename(__file__)

LOG_DIR = "scraping_log"
CURRENT_TIME_STAMP = f"{datetime.now().strftime('%Y-%m-%d %H-%M-%S')}"
LOG_FILE_NAME = f"log_{CURRENT_TIME_STAMP}.log"

os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE_PATH = os.path.join(LOG_DIR, LOG_FILE_NAME)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    filemode="w",
    format='[%(asctime)s] ;%(filename)s ;%(levelname)s ;%(message)s',
    level=logging.INFO
)

# Add log messages at appropriate points in your code
logging.info(f"Logging started in {current_file}")

# Rest of your code...

# Add log messages to indicate the completion or any other important steps
logging.info("Scraping pages...")
