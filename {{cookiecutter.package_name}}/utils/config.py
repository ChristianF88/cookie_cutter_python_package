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


class Section:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    
    def __str__(self):
        config = ""
        for key, val in self.__dict__.items():
            config += "%s: %s\n" % (key, val)
        return config


class Config():
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    
    def __str__(self):
        config = ""
        for section, settings in self.__dict__.items():
            config += "%s\n%s\n" % (section, "-"*len(section))
            
            for key, val in settings.__dict__.items():
                config += "%s: %s\n" % (key, val)
                
        return config


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


def convert_entry(entry):
    if str_is_int(entry):
        return int(entry)
    elif str_is_float(entry):
        return float(entry)
    elif str_is_bool_none(entry):
        return eval(entry.capitalize())
    elif str_is_iterable(entry):
        return eval(entry)
    else:
        return entry


def read_config(file, convert=True, obj=False):
    """
    
    Parameters
    ----------
    file: str,
        specifying path to *.ini file
    convert: bool,
        convert types of config arguments
    obj: bool,
        return object representation
    """

    if not _os.path.exists(file):
        raise FileNotFoundError(f"The file '{file}' does not exist.")

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
                
    if obj:
        for section, dct in parsed.items():
            parsed[section] = Section(**dct)
        parsed = Config(**parsed)
    return parsed


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

    if isinstance(config_dict, Config):

        for section, settings in config_dict.__dict__.items():
            conf[section] = {}
            for key, val in settings.__dict__.items():
                conf[section][key] = val
        config_dict = conf
        
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
