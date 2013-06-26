import ConfigParser
from paths import contesto_path, app_config_path


class Config(object):
    selenium = {
        "host": "",
        "port": "",
        "browser": "",
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
    contesto_path + "/config/config.core.ini",
    contesto_path + "/config/config.default.ini",
    app_config_path + "config.ini",
    app_config_path + "config.my.ini",
)
