import logging
import os


def configure_logger(log_file):
    log_directory = os.path.dirname(log_file)
    if log_directory:
        os.makedirs(log_directory, exist_ok=True)

    logger = logging.getLogger("student_info_system")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        handler = logging.FileHandler(log_file, encoding="utf-8")
        handler.setFormatter(
            logging.Formatter("%(asctime)s %(levelname)s %(message)s")
        )
        logger.addHandler(handler)
    return logger
