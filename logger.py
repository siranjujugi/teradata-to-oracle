import logging

def get_logger():
    logger = logging.getLogger("ETLLogger")
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler("etl.log")
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
