# coding: utf-8
import unittest
import os

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

try:
    from mock import Mock, patch
except ImportError:
    from unittest.mock import Mock, patch

from contesto.utils import screencast
from contesto.exceptions import ScreenCastError


class TestCaseConvertScreencast(unittest.TestCase):
    def test_input_file_not_found(self):
        with patch(
            "os.path.exists", Mock(side_effect=[False, False])
        ), patch(
            "subprocess.Popen", Mock()
        ):
            screencast_recorder = screencast.ScreencastRecorder(
                screencast_name="TestCase_2016_01_01_00_00_01",
                device_name="device"
            )
            error_message = "Screencast file was not created because input.txt file for ffmpeg not found."

            try:
                screencast_recorder.convert_images_to_video()
            except ScreenCastError as e:
                self.assertEqual(e.msg, error_message)

    def test_error_ffmpeg(self):
        with patch(
            "os.path.exists", Mock(side_effect=[True, False])
        ), patch(
            "subprocess.Popen", Mock(side_effect=[OSError])
        ):
            screencast_recorder = screencast.ScreencastRecorder(
                screencast_name="TestCase_2016_01_01_00_00_01",
                device_name="device"
            )
            error_message = "Error while running ffmpeg. Screencast file was not created"

            try:
                screencast_recorder.convert_images_to_video()
            except ScreenCastError as e:
                self.assertEqual(e.msg, error_message)

    def test_screencast_file_not_found(self):
        with patch(
            "os.path.exists", Mock(side_effect=[True, False])
        ), patch(
            "subprocess.Popen", Mock()
        ):
            screencast_recorder = screencast.ScreencastRecorder(
                screencast_name="TestCase_2016_01_01_00_00_01",
                device_name="device"
            )
            error_message = "Screencast file was not created for an unknown reason"

            try:
                screencast_recorder.convert_images_to_video()
            except ScreenCastError as e:
                self.assertEqual(e.msg, error_message)

    def test_success_convert_screencast(self):
        with patch(
            "os.path.exists", Mock(side_effect=[True, True])
        ), patch(
            "subprocess.Popen", Mock()
        ):
            screencast_recorder = screencast.ScreencastRecorder(
                screencast_name="TestCase_2016_01_01_00_00_01",
                device_name="device"
            )
            path = "screencast/TestCase_2016_01_01_00_00_01/TestCase_2016_01_01_00_00_01.webm"
            path = "%s/%s" % (os.getcwd(), path)

            screencast_path = screencast_recorder.convert_images_to_video()
            self.assertEqual(screencast_path, path)
