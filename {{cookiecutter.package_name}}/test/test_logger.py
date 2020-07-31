import unittest
from io import StringIO as _StringIO
import logging as _logging
import re
from grtr.utils.logger import *

def get_single_line_log_text(sio):
    header_and_text = sio.getvalue()
    text = re.split("\[\d{4}\-\d{2}\-\d{2}\ \d{2}\:\d{2}\:\d{2}\ \-\ \w+\]\ \-\ ", header_and_text)[1]
    return text.rstrip("\n")

class TestLogger(unittest.TestCase):

    def setUp(self) -> None:
        self.sio = _StringIO()

    def test_logger_creation(self):
        logger1 = get_logger()
        logger2 = get_logger(
            stream=self.sio
        )
        logger3 = get_logger(
            logger_level=_logging.WARNING
        )
        logger4 = get_logger(
            logger_id="some_string"
        )

    def test_logger_instances(self):
        self.assertTrue(get_logger() is get_logger())
        self.assertFalse(get_logger() is get_logger(logger_id="some_string"))

    def test_log_text(self):
        logger1 = get_logger(
            stream=self.sio,
            logger_level=_logging.INFO
        )
        to_be_logged = "test string"
        logger1.info(to_be_logged)
        self.assertEqual(to_be_logged, get_single_line_log_text(self.sio))

    def tearDown(self) -> None:
        del self.sio

if __name__ == '__main__':
    unittest.main()

