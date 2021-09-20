#!/usr/bin/env python
"""
-------------------------------------------------------
2021-02-01 -- Christian Foerster
christian.foerster@eawag.ch
-------------------------------------------------------
"""
from configparser import ConfigParser as _ConfigParser
from copy import deepcopy as _deepcopy
import os as _os


def str_is_int(num):
    try:
        int(num)
        return True
    except:
        return False

    
def str_is_float(num):
    if "." in num:
        try:
            float(num)
            return True
        except:
            return False
    else:
        return False

    
def str_is_bool_none(expr):
    if expr.lower() in [
        "true",  
        "false",  
        "none"
    ]:
        return True
    else:
        return False


def str_is_iterable(expr):
    if expr.startswith("[") and expr.endswith("]"):
        try:
            return isinstance(eval(expr), list)
        except:
            return False
    elif expr.startswith("{") and expr.endswith("}"):
        try:
            return isinstance(eval(expr), dict)
        except:
            return False        
    else:
        return False


def is_indented(expr):
    indented = False
    found = ""
    for char in expr:
        if found:
            if char == "\n":
                if found == "=":
                    found = char
                    indented = True
                else:
                    return False
            elif char == "=":
                if found == "\n":
                    found = char
                    indented = True
                else:
                    return False
        else:
            if char == "=" or char == "\n":
                found = char

    return indented


def parse_indented(expr):
    key_value_pairs = expr.split("\n")
    if key_value_pairs[0] == "\n" or key_value_pairs[0] == "":
        key_value_pairs = key_value_pairs[1:]

    formatted = "{"
    for kv in key_value_pairs:
        k, v = kv.split("=")
        formatted += f"'{k.rstrip().lstrip()}': '{v.rstrip().lstrip()}', "
    formatted += "}"
    return eval(formatted)


def convert_entry(entry):
    if str_is_int(entry):
        return int(entry)
    elif str_is_float(entry):
        return float(entry)
    elif str_is_bool_none(entry):
        return eval(entry.capitalize())
    elif str_is_iterable(entry):
        return eval(entry)
    elif is_indented(entry):
        parse_dict = parse_indented(entry)
        for key in parse_dict:
            parse_dict[key] = convert_entry(parse_dict[key])
        return parse_dict
    else:
        return entry


def read_config(file, convert=True):
    """
    
    Parameters
    ----------
    file: str,
        specifying path to *.ini file
    convert: bool,
        convert types of config arguments
    """

    if not _os.path.exists(file):
        raise FileNotFoundError(f"The file '{file}' does not exist.")
    try:

        config = _ConfigParser()
        config.read(file)

        parsed = {}
        for conf in config:
            p_conf = dict(config[conf])
            if p_conf:
                parsed[conf] = p_conf

        if convert:
            for section, dct in parsed.items():
                for key, entry in dct.items():
                    parsed[section][key] = convert_entry(entry)

        return parsed

    except Exception as e:
        print("Unfortunately you passed an invalid configuration file '{file}', that cannot be read.")
        raise e


def write_config(file, config):
    """
    
    Parameters
    ----------
    file: str,
        specifying path to *.ini file
    config: Configparser | dict | Config,
        passing the settings you want to write
    """

    config_dict = _deepcopy(config)
    conf = {}
        
    if isinstance(config_dict, dict):
        try:

            for section, parameters in config_dict.items():
                for key, value in parameters.items():
                    config_dict[section][key] = value if isinstance(value, str) else repr(value)

            conf = _ConfigParser()
            conf.read_dict(config_dict)

        except Exception as e:
            print(e)
        
    with open(file, "w+") as configfile:
        conf.write(configfile)


