# coding: utf-8
import os

from contesto.globals import current_test
from contesto.utils.log import log
from contesto.utils.collect import get_path_for_metadata, get_filename_base


class Logcat():
    def __init__(self, driver):
        self.driver = driver
        self._logcat = []
        self.fetch()

    def fetch(self):
        try:
            self._logcat += self.driver.get_log("logcat")
        except:
            log.exception("Cannot fetch logcat")

    @property
    def messages(self):
        for item in self._logcat:
            yield item.get("message", "")

    def dump_to_file(self, file_name):
        with open(file_name, "w") as file:
            [file.write(message + "\n") for message in self.messages]

    def collect(self, test_obj=None):
        if not test_obj:
            test_obj = current_test
        path_to_file = '%s.txt' % os.sep.join(
            [get_path_for_metadata(), get_filename_base()]
        )
        self.fetch()
        if self._logcat:
            self.dump_to_file(path_to_file)
            meta_info = {
                "path": path_to_file,
                "name": 'Logcat',
                "mime_type": "text/plain"
            }
            test_obj._meta_info["attachments"].append(meta_info)
