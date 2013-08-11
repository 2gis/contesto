import ConfigParser
import os


class Config(object):
    selenium = {
        "host": "",
        "port": "",
        "browser": "",
        "platform": "",
    }
    timeout = {
        "normal": "",
    }
    session = {
        "shared": "",
    }
    sizzle = {
        "url": "",
    }

    def __init__(self, *args):
        """
        :type args: tuple of str
        """
        for ini_path in args:
            self.add_config_file(ini_path)

    def add_config_file(self, path_to_file):
        """
        :type path_to_file: str
        """
        ### @todo value type parsing
        parser = ConfigParser.SafeConfigParser()
        parser.read(path_to_file)
        sections = parser.sections()
        for section in sections:
            params = parser.items(section)
            section = section.lower()
            d = {}
            for param in params:
                key, value = param
                d[key] = value
            if hasattr(self, section):
                getattr(self, section).update(d)
            else:
                setattr(self, section, d)


config = Config(
    os.path.abspath(os.path.dirname(__file__)) + "/config/config.core.ini",
    os.path.abspath(os.path.dirname(__file__)) + "/config/config.default.ini",
)
