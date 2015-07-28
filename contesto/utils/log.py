import inspect
import logging
import json
import sys


def trace(cls):
    ### @todo adding trace for property-methods
    ### @todo prettify log messages
    def log(func):
        if func.__name__ == 'wrapped':
            return func

        def wrapped(*args, **kwargs):
            try:
                log_handler.inc_depth()
                place = args[0].__class__.__name__ + u"->" + func.__name__
                logging.info(u"Entering: %s" % place)
                log_handler.inc_depth()
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    try:
                        exception = u"Exception: %s in %s" % (str(e), place)
                    except UnicodeDecodeError:
                        exception = u"Exception: %s in %s" % (str(e).encode(sys.stdout.encoding), place)

                    logging.error(exception)
                    raise e
            finally:
                log_handler.dec_depth()
                logging.info(u"Exiting: " + place)
                log_handler.dec_depth()

        return wrapped

    for name, m in inspect.getmembers(
            cls, lambda x: inspect.isfunction(x) or inspect.ismethod(x)):
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


class StdoutHandler(logging.Handler):
    def emit(self, record):
        try:
            msg = self.format(record)
            sys.stdout.write(msg)
            sys.stdout.write("\n")
            sys.stdout.flush()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)


INDENT = {
    'INIT': 0,
    'ENV': 1,
    'ACTION': 2,
    'INTERNAL': 3,
}


class IndentFormatter(logging.Formatter):
    indent = "  "

    def __init__(self, msg):
        logging.Formatter.__init__(self, msg)

    def format(self, record):
        levelname = record.levelname
        if levelname in INDENT:
            indent_levelname = (INDENT[levelname]) * self.indent + levelname
            record.levelname = indent_levelname
        return logging.Formatter.format(self, record)


INIT_LEVEL = 19
ENV_LEVEL = 18
ACTION_LEVEL = 17
INTERNAL_LEVEL = 16


logging.addLevelName(INIT_LEVEL, "INIT")
logging.addLevelName(ACTION_LEVEL, "ACTION")
logging.addLevelName(ENV_LEVEL, "ENV")
logging.addLevelName(INTERNAL_LEVEL, "INTERNAL")


class IndentLogger(logging.Logger):
    FORMAT = "%(levelname)s :: %(message)s"

    def __init__(self, name):
        logging.Logger.__init__(self, name, logging.DEBUG)

        indent_formatter = IndentFormatter(self.FORMAT)

        console = StdoutHandler()
        console.setFormatter(indent_formatter)

        self.addHandler(console)

    def init(self, message, *args, **kws):
        self._log(INIT_LEVEL, message, args, **kws)

    def action(self, message, *args, **kws):
        self._log(ACTION_LEVEL, message, args, **kws)

    def env(self, message, *args, **kws):
        self._log(ENV_LEVEL, message, args, **kws)

    def internal(self, message, *args, **kws):
        self._log(INTERNAL_LEVEL, message, args, **kws)


logging.setLoggerClass(IndentLogger)
log = IndentLogger("TEST")