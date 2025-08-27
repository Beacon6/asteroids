import logging


def get_logger(logger_name: str) -> logging.Logger:
    logger = logging.getLogger(logger_name)
    log_format = '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
    console_handler = logging.StreamHandler()
    logging.basicConfig(handlers=(console_handler,), level=logging.INFO, format=log_format)
    return logger
