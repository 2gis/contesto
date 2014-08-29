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


INDENT = {
    'INIT': 0,
    'ENV': 1,
    'ACTION': 2,
}


class StdoutHandler(logging.Handler):
    def emit(self, record):
        try:
            msg = self.format(record)
            fs = "%s\n"
            try:
                if (isinstance(msg, unicode) and
                    getattr(sys.stdout, 'encoding', None)):
                    ufs = u'%s\n'
                    try:
                        sys.stdout.write(ufs % msg)
                    except UnicodeEncodeError:
                        #Printing to terminals sometimes fails. For example,
                        #with an encoding of 'cp1251', the above write will
                        #work if written to a stream opened or wrapped by
                        #the codecs module, but fail when writing to a
                        #terminal even when the codepage is set to cp1251.
                        #An extra encoding step seems to be needed.
                        sys.stdout.write((ufs % msg).encode(sys.stdout.encoding))
                else:
                    sys.stdout.write(fs % msg)
            except UnicodeError:
                sys.stdout.write(fs % msg.encode("UTF-8"))
            sys.stdout.flush()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)


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


class IndentLogger(logging.Logger):
    FORMAT = "%(levelname)s :: %(message)s"

    def __init__(self, name):
        logging.Logger.__init__(self, name, logging.DEBUG)

        indent_formatter = IndentFormatter(self.FORMAT)

        console = StdoutHandler()
        console.setFormatter(indent_formatter)

        self.addHandler(console)
        return


logging.setLoggerClass(IndentLogger)

INIT_LEVEL = 17
ENV_LEVEL = 18
ACTION_LEVEL = 19
logging.addLevelName(INIT_LEVEL, "INIT")
logging.addLevelName(ACTION_LEVEL, "ACTION")
logging.addLevelName(ENV_LEVEL, "ENV")


def init(self, message, *args, **kws):
    self._log(INIT_LEVEL, message, args, **kws)


def action(self, message, *args, **kws):
    self._log(ACTION_LEVEL, message, args, **kws)


def env(self, message, *args, **kws):
    self._log(ENV_LEVEL, message, args, **kws)


logging.Logger.init = init
logging.Logger.action = action
logging.Logger.env = env

log = logging.getLogger("TEST")