# coding: utf-8
import inspect
import logging


class SessionLogger(object):
    def __getattr__(self, item):
        logger = logging.getLogger(__name__)
        for frame in inspect.stack()[1:]:
            test = frame[0].f_locals.get("self")
            if test and hasattr(test, "driver"):
                try:
                    logger = logging.getLogger(str(test.driver.session_id))
                except AttributeError:
                    logger.warning("Could not find driver session_id")
                break

        return getattr(logger, item)

log = SessionLogger()
