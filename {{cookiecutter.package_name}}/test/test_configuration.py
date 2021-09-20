import pytest
from {{cookiecutter.package_name}}.utils.config import *

def test_str_is_int():
    assert str_is_int("3")
    assert not str_is_int("3.4") 
    assert not str_is_int("s") 
    assert not str_is_int(" ") 

def test_str_is_float():
    assert str_is_float("3.4")
    assert not str_is_float("3") 
    assert not str_is_float("s") 
    assert not str_is_float(" ") 

def test_str_is_bool_none():
    assert str_is_bool_none("true")
    assert str_is_bool_none("false")
    assert str_is_bool_none("none")
    assert str_is_bool_none("True")
    assert str_is_bool_none("False")
    assert str_is_bool_none("None")
    assert not str_is_bool_none("f")
    assert not str_is_bool_none(" ")
    assert not str_is_bool_none("3")
    assert not str_is_bool_none("4.3")

def test_str_is_iterable():
    assert str_is_iterable("[3,4,5,6]")
    assert str_is_iterable("{4:3, 34:33}")
    assert not str_is_iterable("[[]")
    assert not str_is_iterable("{}}")
    assert not str_is_iterable("f")
    assert not str_is_iterable(" ")
    assert not str_is_iterable("3")
    assert not str_is_iterable("4.3")

def test_convert_entry():
    assert type(convert_entry("3")) is int
    assert type(convert_entry("4.5")) is float
    assert type(convert_entry("trUe")) is bool
    assert type(convert_entry("False")) is bool
    assert type(convert_entry("none")) is type(None)
    assert type(convert_entry("[4,5]")) is list
    assert type(convert_entry("{'d':44}")) is dict
    assert type(convert_entry("abc")) is str

def test_read_and_variable_conversions(ini):
    conf = read_config(ini)
    
    assert type(conf["HEADER_1"]["int"]) is int
    assert type(conf["HEADER_1"]["float"]) is float
    assert type(conf["HEADER_1"]["int_as_str"]) is str
    assert type(conf["HEADER_1"]["float_as_str"]) is str
    
    assert type(conf["HEADER_2"]["bool_1"]) is bool
    assert type(conf["HEADER_2"]["bool_2"]) is bool
    assert type(conf["HEADER_2"]["bool_3"]) is bool
    assert type(conf["HEADER_2"]["empty"]) is str
    assert type(conf["HEADER_2"]["dt_fmt"]) is str
    assert type(conf["HEADER_2"]["none"]) is type(None)
    
    assert type(conf["HEADER_3"]["nested"]) is dict
    assert type(conf["HEADER_3"]["nested"]["first"]) is int
    assert type(conf["HEADER_3"]["nested"]["second"]) is str
    assert type(conf["HEADER_3"]["nested"]["third"]) is list
    assert type(conf["HEADER_3"]["nested"]["fourth"]) is float
    assert type(conf["HEADER_3"]["nested"]["fifth"]) is str
    

    
