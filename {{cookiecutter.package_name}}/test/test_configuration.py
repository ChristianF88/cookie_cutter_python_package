import unittest
import os
from grtr.utils.config import *

class TestConfigTypeConverter(unittest.TestCase):

    def test_str_is_int(self):
        self.assertTrue(str_is_int("3"), "3")
        self.assertFalse(str_is_int("3.4"), "3.4")
        self.assertFalse(str_is_int("s"), "s")
        self.assertFalse(str_is_int(" "), " ")

    def test_str_is_float(self):
        self.assertTrue(str_is_float("3.4"), "3.4")
        self.assertFalse(str_is_float("3"), "3")
        self.assertFalse(str_is_float("s"), "s")
        self.assertFalse(str_is_float(" "), " ")

    def test_str_is_bool_none(self):
        self.assertTrue(str_is_bool_none("true"), "true")
        self.assertTrue(str_is_bool_none("false"), "false")
        self.assertTrue(str_is_bool_none("none"), "none")
        self.assertTrue(str_is_bool_none("True"), "True")
        self.assertTrue(str_is_bool_none("False"), "False")
        self.assertTrue(str_is_bool_none("None"), "None")
        self.assertFalse(str_is_bool_none("f"))
        self.assertFalse(str_is_bool_none(" "))
        self.assertFalse(str_is_bool_none("3"))
        self.assertFalse(str_is_bool_none("4.3"))

    def test_str_is_iterable(self):
        self.assertTrue(str_is_iterable("[3,4,5,6]"), "list")
        self.assertTrue(str_is_iterable("{4:3, 34:33}"), "dict")
        self.assertFalse(str_is_iterable("[[]"))
        self.assertFalse(str_is_iterable("{}}"))
        self.assertFalse(str_is_iterable("f"))
        self.assertFalse(str_is_iterable(" "))
        self.assertFalse(str_is_iterable("3"))
        self.assertFalse(str_is_iterable("4.3"))

    def test_convert_entry(self):
        self.assertIsInstance(convert_entry("3"), int,)
        self.assertIsInstance(convert_entry("4.5"), float)
        self.assertIsInstance(convert_entry("trUe"), bool)
        self.assertIsInstance(convert_entry("False"), bool)
        self.assertIsInstance(convert_entry("none"), type(None))
        self.assertIsInstance(convert_entry("[4,5]"), list)
        self.assertIsInstance(convert_entry("{'d':44}"), dict)
        self.assertIsInstance(convert_entry("abc"), str)


class TestConfigParser(unittest.TestCase):

    __active_test_folder = "current_test"
    __file_path = os.path.join(__active_test_folder, "config.ini")
    __configuration = {
        "NonIterables": {
            "string": "Value_1",
            "int": 1,
            "float": 2.3,
            "boolean_1": True,
            "boolean_2": False,
            "none_type": None
        },
        "Iterables": {
            "iter_1": [2, 3, ["es", True, None]],
            "iter_2": {"abc": 3}
        }
    }

    def setUp(self) -> None:
        if not os.path.exists(self.__active_test_folder):
            os.mkdir(self.__active_test_folder)

    def test_write_and_read_config(self):
        write_config(
            self.__file_path,
            self.__configuration
        )
        read_dict = read_config(
            self.__file_path
        )
        self.assertDictEqual(read_dict, self.__configuration)

    def tearDown(self) -> None:
        if os.path.exists(self.__active_test_folder):
            for file in os.listdir(self.__active_test_folder):
                os.remove(
                    os.path.join(
                        self.__active_test_folder,
                        file
                    )
                )
            os.rmdir(self.__active_test_folder)



if __name__ == '__main__':
    unittest.main()

