import inspect
import logging
import json


def trace(cls):
    ### @todo adding trace for property-methods
    ### @todo prettify log messages
    def log(func):
        if func.__name__ == 'wrapped':
            return func

        def wrapped(*args, **kwargs):
            try:
                log_handler.inc_depth()
                logging.info("Entering: " + args[0].__class__.__name__ + "->" + func.__name__)
                log_handler.inc_depth()
                try:
                    return func(*args, **kwargs)
                except Exception, e:
                    logging.warning("Exception: " + str(e) + args[0].__class__.__name__ + "->" + func.__name__)
                    raise
            finally:
                log_handler.dec_depth()
                logging.info("Exiting: " + args[0].__class__.__name__ + "->" + func.__name__)
                log_handler.dec_depth()

        return wrapped

    for name, m in inspect.getmembers(cls, inspect.ismethod):
        setattr(cls, name, log(m))
    return cls


class ContestoLogHandler(logging.Handler):
    def __init__(self, **kwargs):
        super(ContestoLogHandler, self).__init__(**kwargs)
        self._list = []
        self._depth = 0

    def emit(self, record):
        """
        :type record: LogRecord
        """

        def insert(lst, depth, el):
            cur = lst
            d = 0
            while d < depth:
                if len(cur) == 0 or not isinstance(cur[-1], list):
                    cur.append([])
                cur = cur[-1]
                d += 1
            cur.append(el)

        msg = {
            "timestamp": record.created,
            "level": record.levelname,
            "message": record.msg,
        }

        insert(self._list, self._depth, msg)

    def inc_depth(self):
        self._depth += 1

    def dec_depth(self):
        if self._depth > 0:
            self._depth -= 1

    def get_json_log(self):
        return json.dumps(self._list)


log_handler = ContestoLogHandler()
