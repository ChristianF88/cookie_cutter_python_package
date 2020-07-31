import logging as _logging
import sys as _sys

class MultiLineFormatter(_logging.Formatter):
    def format(self, record):
        record_string = _logging.Formatter.format(self, record)
        if record.exc_text is None:
            header, _ = record_string.split(record.message)
        else:
            header, _ = record_string.split(record.message+"\n"+record.exc_text)
        record_string = record_string.replace('\n', '\n' + ' '*len(header))
        return record_string

def get_logger(
        stream=_sys.stdout,
        logger_level=_logging.DEBUG,
        fmt='[%(asctime)s - %(levelname)s] - %(message)s',
        logger_id='streamLogger'
):

        logger = _logging.getLogger(logger_id)
        logger.setLevel(logger_level)
        handler = _logging.StreamHandler(stream)
        handler.setLevel(logger_level)
        formatter = MultiLineFormatter(fmt, "%Y-%m-%d %H:%M:%S")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

