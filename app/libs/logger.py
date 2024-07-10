import sys
from logging import DEBUG, Formatter, Logger, StreamHandler, getLogger


def get_logger() -> Logger:
    logger = getLogger("dynamodb-back-to-basics")
    logger.setLevel(DEBUG)
    stream_handler = StreamHandler(sys.stdout)
    log_formatter = Formatter(
        "%(asctime)s [%(processName)s: %(process)d] [%(threadName)s: %(thread)d] [%(levelname)s] %(name)s: %(message)s"
    )
    stream_handler.setFormatter(log_formatter)
    logger.addHandler(stream_handler)

    return logger
