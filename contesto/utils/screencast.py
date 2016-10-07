# coding: utf-8
import errno
import json
import logging
import os
import subprocess
from datetime import datetime

from contesto import config
from contesto.globals import current_test

log = logging.getLogger(__name__)


class ScreencastRecorder:
    device_serial = None
    process = None

    def __init__(self, screencast_name, device_name):
        self.screencast_dir = os.path.join(
            os.path.dirname(os.path.abspath(self.__module__)),
            config.utils["screencast_dir"],
            screencast_name
        )
        self.screencast_name = screencast_name
        self.device_name = device_name

    def _start_getting_screenshots_from_device(self):
        log.info("Starting recorder for current session on %s to %s ..." % (self.device_name, self.screencast_dir))
        args = [
            "stf-record",
            "--adb-connect-url", self.device_name,
            "--log-level", "DEBUG",
            "--dir", self.screencast_dir
        ]
        return subprocess.Popen(args, stdout=subprocess.PIPE)

    def convert_images_to_video(self):
        log.info("Start converting images to video...")
        input_file = "%s/input.txt" % self.screencast_dir

        if not os.path.exists(input_file):
            log.error("Input file for conversion was not found. Skipping... ")
            return

        screencast_filename = "%s/%s.webm" % (self.screencast_dir, self.screencast_name)
        args = [
            "ffmpeg",
            "-loglevel", "panic",
            "-f", "concat",
            "-i", input_file,
            screencast_filename
        ]
        try:
            converter = subprocess.Popen(args, stdout=subprocess.PIPE)
            if converter.pid:
                converter.communicate()
        except OSError as e:
            if e.errno == errno.ENOENT:
                log.exception("ffmpeg is not installed, screenshots won't be converted to video")
            else:
                raise

        if os.path.exists(screencast_filename):
            log.info("Screencast file was successfully created: %s" % screencast_filename)
            return screencast_filename.replace("/v4-ui-tests/", "")
        else:
            log.warn("Screencast file was not created")

    def start(self):
        self.process = self._start_getting_screenshots_from_device()
        log.info("Record process has been started...")

    def stop(self):
        if self.process and not self.process.returncode:
            self.process.terminate()
            self.process.wait()
        log.info("Stopped recoder for current session on %s..." % self.device_serial)

    def is_alive(self):
        if self.process and not self.process.returncode:
            log.debug("Screencast process is alive!")
            return True


def start_screencast_recorder():
    if config.utils["record_screencast"]:
        current_time = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
        safe_test_name = str(current_test).translate({
            ord("("): "",
            ord(")"): "",
            ord(" "): "_"
        })
        device_name = current_test.driver.capabilities.get("deviceName", None)
        if device_name is None:
            log.error("")
        current_test.screencast_recorder = ScreencastRecorder(
            screencast_name="%s_%s" % (safe_test_name, current_time),
            device_name=device_name
        )
        current_test.screencast_recorder.start()


def stop_screencast_recorder():
    if getattr(current_test, "screencast_recorder", None):
        current_test.screencast_recorder.stop()


def attach_screencast_to_results():
    if not getattr(current_test, "screencast_recorder", None):
        log.warn('No screencast_recorder found for test %s' % current_test)
        return

    if current_test.screencast_recorder.is_alive():
        current_test.screencast_recorder.stop()

    if not current_test._meta_info.get('message', None) and not current_test._meta_info.get('stack_trace', None):
        log.info('Test %s passed. Skipping making video from screenshots' % current_test)
        return

    screencast_file_path = current_test.screencast_recorder.convert_images_to_video()
    current_test.screencast_recorder = None
    if screencast_file_path:
        log.info("Adding screencast file %s to attachments" % screencast_file_path)
        current_test._meta_info['attachments'].append({
            "mime_type": "video/webm",
            "path": screencast_file_path,
            "name": "video"
        })

