# coding: utf-8
import errno
import logging
import os
import subprocess
from datetime import datetime
from threading import Timer

from contesto import config
from contesto.globals import current_test
from contesto.exceptions import ScreenCastError

log = logging.getLogger(__name__)


class ScreencastRecorder:
    device_name = None
    process = None

    def __init__(self, screencast_name, device_name):
        screencast_dir = config.utils.get('screencast_dir', None)
        if screencast_dir is None:
            log.info("No 'screencast_dir' provided in config. Defaulting to 'screencast'")
            screencast_dir = 'screencast'
        self.screencast_dir_abspath = os.path.join(
            os.path.dirname(os.path.abspath(self.__module__)),
            screencast_dir,
            screencast_name
        )
        self.screencast_name = screencast_name
        self.device_name = device_name

    def _start_getting_screenshots_from_device(self):
        log.info("Starting recorder for current session on %s to %s ..." % (self.device_name, self.screencast_dir_abspath))
        args = [
            "stf-record",
            "--adb-connect-url", self.device_name,
            "--log-level", "DEBUG",
            "--dir", self.screencast_dir_abspath
        ]
        try:
            return subprocess.Popen(args, stdout=subprocess.PIPE)
        except:
            raise ScreenCastError("Failed to start stf-record")

    def convert_images_to_video(self):
        log.info("Start converting images to video...")
        input_file = "%s/input.txt" % self.screencast_dir_abspath

        if not os.path.exists(input_file):
            raise ScreenCastError("Screencast file was not created because input.txt file for ffmpeg not found.")

        screencast_file_abspath = "%s/%s.webm" % (self.screencast_dir_abspath, self.screencast_name)
        args = [
            "ffmpeg",
            "-loglevel", "panic",
            "-f", "concat",
            "-i", input_file,
            screencast_file_abspath
        ]
        try:
            converter = subprocess.Popen(args, stdout=subprocess.PIPE)
            if converter.pid:
                converter.communicate()
        except OSError as e:
            if e.errno == errno.ENOENT:
                log.exception("ffmpeg is not installed, screenshots won't be converted to video")
            else:
                raise ScreenCastError("Error while running ffmpeg. Screencast file was not created")

        if os.path.exists(screencast_file_abspath):
            log.info("Screencast file was successfully created: %s" % screencast_file_abspath)
            return screencast_file_abspath
        else:
            raise ScreenCastError("Screencast file was not created for an unknown reason")

    def start(self):
        self.process = self._start_getting_screenshots_from_device()
        log.info("Record process has been started...")

    def stop(self):
        def kill(process):
            log.warn("Timeout expired while waiting for process to terminate. Killing...")
            process.kill()
        if self.process and not self.process.returncode:
            timer = Timer(15, kill, [self.process])
            try:
                timer.start()
                self.process.terminate()
                self.process.wait()
            finally:
                timer.cancel()
        log.info("Stopped recoder for current session on %s..." % self.device_name)

    def is_alive(self):
        if self.process and not self.process.returncode:
            log.debug("Screencast process is alive!")
            return True


def start_screencast_recorder():
    """
    Creates and starts ScreencastRecorder for current test, which will spawn stf-record process
    and save screenshots from device connected via stf-connect to screencast_dir
    """
    already_started_recorder = getattr(current_test, "screencast_recorder", None)
    if already_started_recorder is not None:
        log.error("There is already a Screencast Recorder started for this test. Skipping...")
        return
    else:
        current_time = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
        test_name = str(current_test)
        device_name = current_test.driver.capabilities.get("deviceName", None)
        if device_name is None:
            log.error("No deviceName in driver.capabilities. Failed to start screencast recorder")
            return
        current_test.screencast_recorder = ScreencastRecorder(
            screencast_name="%s_%s" % (test_name, current_time),
            device_name=device_name
        )
        try:
            current_test.screencast_recorder.start()
        except ScreenCastError:
            log.exception("Failed to start screencast recorder for test")


def stop_screencast_recorder():
    """
    Stops ScreencastRecorder for current test
    """
    if getattr(current_test, "screencast_recorder", None):
        current_test.screencast_recorder.stop()


def try_to_attach_screencast_to_results():
    """
    Tries to create .webm video using ffmpeg from screenshots saved via ScreencastRecorder and attach this video
    with current_test._meta_info. Stops ScreencastRecorder if it is not stopped yet.
    """
    if not getattr(current_test, "screencast_recorder", None):
        log.warn('No screencast_recorder found for test %s' % current_test)
        return

    if current_test.screencast_recorder.is_alive():
        current_test.screencast_recorder.stop()

    if not current_test._meta_info.get('message', None) and not current_test._meta_info.get('stack_trace', None):
        log.info('Test %s passed. Skipping making video from screenshots' % current_test)
        return

    try:
        screencast_file_path = current_test.screencast_recorder.convert_images_to_video()
        log.info("Adding screencast file %s to attachments" % screencast_file_path)
        current_test._meta_info['attachments'].append({
            "mime_type": "video/webm",
            "path": screencast_file_path,
            "name": "video"
        })
    except ScreenCastError:
        log.exception("Error trying to make video from screenshots. Nothing to attach to test results")
    current_test.screencast_recorder = None
