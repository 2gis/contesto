# coding: utf-8

from selenium.webdriver.common.by import By


class ContestoBy(By):
    ANDROID_UIAUTOMATOR = "-android uiautomator"


class Locator(dict):
    def __init__(self, by, value):
        super(Locator, self).__init__()
        self['by'] = by
        self['value'] = value