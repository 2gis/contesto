# coding: utf-8
import os

from contesto.globals import current_test
from contesto.utils.log import log
from contesto.utils.collect import get_path_for_metadata, get_filename_base


class Logcat:
    def __init__(self, driver):
        self.driver = driver
        self._before_start_messages = self._get_log()
        self._essential_messages = []

    def fetch(self):
        self._essential_messages += self._get_log()

    def _get_log(self):
        try:
            return self.driver.get_log("logcat")
        except:
            log.exception("Cannot fetch logcat")

    @staticmethod
    def _get_lines_from(lines):
        for line in lines:
            yield line.get("message", "")

    @property
    def additional_messages(self):
        return self._get_lines_from(self._before_start_messages)

    @property
    def essential_messages(self):
        return self._get_lines_from(self._essential_messages)

    @property
    def messages(self):
        return self._get_lines_from(self._before_start_messages + self._essential_messages)

    def dump_to_file(self, file_name, custom_data=None):
        messages = custom_data if custom_data else self.messages
        with open(file_name, "w") as file:
            [file.write(message + "\n") for message in messages]

    def collect(self, test_obj=None):
        if not test_obj:
            test_obj = current_test
        path_to_file = '%s.txt' % os.sep.join(
            [get_path_for_metadata(), get_filename_base()]
        )
        self.fetch()
        if self._before_start_messages or self._essential_messages:
            self.dump_to_file(path_to_file)
            meta_info = {
                "path": path_to_file,
                "name": 'Logcat',
                "mime_type": "text/plain"
            }
            test_obj._meta_info["attachments"].append(meta_info)
