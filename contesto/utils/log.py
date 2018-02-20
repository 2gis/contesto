# coding: utf-8
import inspect
import logging
import sys

from contesto import config


LOG_FORMAT = "[%(asctime)s] %(levelname)s %(session_id)s: %(message)s"


class SessionStreamHandler(logging.StreamHandler):
    def emit(self, record):
        self.stream = sys.stderr
        super(SessionStreamHandler, self).emit(record)


class ContextFilter(logging.Filter):
    def filter(self, record):
        for frame in inspect.stack()[1:]:
            test = frame[0].f_locals.get("self")
            if hasattr(test, "driver") and hasattr(test.driver, "session_id") and test.driver.session_id:
                record.session_id = test.driver.session_id
                break
        else:
            record.session_id = "<no session id>"

        return True


def get_logger(name, level=None, format_=LOG_FORMAT):
    if not level:
        level = getattr(logging, config.logging["level"].upper())

    logger = logging.getLogger(name)
    logger.setLevel(level)
    context_filter = ContextFilter()

    stream_handler = SessionStreamHandler()
    formatter = logging.Formatter(format_)
    stream_handler.setLevel(level)
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    logger.addFilter(context_filter)
    return logger


log = get_logger(__name__)
