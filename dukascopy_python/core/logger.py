import logging
import sys
from contextlib import contextmanager
from contextvars import ContextVar
from collections.abc import Iterator

LOGGER_NAME = "dukascopy"

_current_logger: ContextVar[logging.Logger | None] = ContextVar(
    "current_logger",
    default=None,
)


def create_logger(
    name: str = LOGGER_NAME,
    level: int = logging.INFO,
) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.NOTSET)
        handler.setFormatter(
            logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
        )
        logger.addHandler(handler)

    logger.propagate = False
    return logger


_default_logger = create_logger()


def get_logger() -> logging.Logger:
    logger = _current_logger.get()
    return logger if logger is not None else _default_logger


@contextmanager
def use_logger(logger: logging.Logger) -> Iterator[None]:
    token = _current_logger.set(logger)

    try:
        yield
    finally:
        _current_logger.reset(token)

def debug(*args):
    get_logger().debug(" ".join(map(str, args)))