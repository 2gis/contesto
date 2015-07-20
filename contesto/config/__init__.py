# coding: utf-8
import ConfigParser
import os
import ast


class Config(object):
    ### @todo add method for reinitializing config
    selenium = {
        "host": "",
        "port": "",
        "browser": "",
        "platform": "",
    }
    browsermobproxy = {
        'enabled': "",
        'url': "",
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
    utils = {
        "save_screenshots": "",
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
        parser = ConfigParser.SafeConfigParser()
        parser.optionxform = str
        parser.read(path_to_file)
        sections = parser.sections()
        for section in sections:
            params = parser.items(section)
            section = section.lower()
            d = {}
            for param in params:
                key, value = param
                try:
                    value = ast.literal_eval(value)
                except (ValueError, SyntaxError):
                    pass
                d[key] = value
            if hasattr(self, section):
                getattr(self, section).update(d)
            else:
                setattr(self, section, d)


config = Config(
    os.path.abspath(os.path.dirname(__file__)) + "/config.core.ini",
    os.path.abspath(os.path.dirname(__file__)) + "/config.default.ini",
)
