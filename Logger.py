import logging
import sys


def get_logger():

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # log lower levels to stdout
    stdout_handler = logging.StreamHandler(stream=sys.stdout)
    stdout_handler.addFilter(lambda rec: rec.levelno <= logging.INFO)
    stdout_handler.setFormatter(formatter)
    logger.addHandler(stdout_handler)

    # log higher levels to stderr (red)
    stderr_handler = logging.StreamHandler(stream=sys.stderr)
    stderr_handler.addFilter(lambda rec: rec.levelno > logging.INFO)
    stderr_handler.setFormatter(formatter)
    logger.addHandler(stderr_handler)
    return logger