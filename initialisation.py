import logging
from dotenv import load_dotenv

load_dotenv()

class initialisation():
    def __init__(self):
        log_level_str = os.getenv("LOG_LEVEL", "INFO").upper()
        log_level = getattr(logging, log_level_str, logging.INFO)
        ENABLE_LOG = os.getenv("ENABLE_LOG", "False").lower() == "true"
        LOG_FILE_LOCATION = os.getenv("LOG_FILE_LOCATION", "/var/log/scratchpad.log")

        if ENABLE_LOG:
            log_dir = os.path.dirname(LOG_FILE_LOCATION)
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir, exist_ok=True)
            # Ensure file exists
            if not os.path.exists(LOG_FILE_LOCATION):
                with open(LOG_FILE_LOCATION, "a"):
                    pass
            logging.basicConfig(
                filename=LOG_FILE_LOCATION,
                level=log_level,
                format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            logger = logging.getLogger(__name__)
            logger.info("log enabled")
        else:
            logging.basicConfig(
                level=log_level,
                format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            logger = logging.getLogger(__name__)
