from configparser import ConfigParser as _ConfigParser

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
        
def is_int(num):
    try:
        int(num)
        return True
    except:
        return False

    
def is_float(num):
    if "." in num:
        try:
            float(num)
            return True
        except:
            return False
    else:
        return False

    
def is_bool_none(expr):
    if expr.lower() in [
        "true",  
        "false",  
        "none"
    ]:
        return True
    else:
        return False
    
def is_iterable(expr):
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
    if is_int(entry):
        return int(entry)
    elif is_float(entry):
        return float(entry)
    elif is_bool_none(entry):
        return eval(entry.capitalize())
    elif is_iterable(entry):
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
    
    if isinstance(config, Config):
        conf = {}
        for section, settings in config.__dict__.items():
            conf[section] = {}
            for key, val in settings.__dict__.items():
                conf[section][key] = val
        config = conf
        
    if isinstance(config, dict):
        try:
            conf = _ConfigParser()
            conf.read_dict(config)
        except Exception as e:
            print(e)    
        
    with open(file, "w+") as configfile:
        conf.write(configfile)
        
