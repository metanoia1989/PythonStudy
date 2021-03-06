#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Logger(object):
    """
    A file-based message logger with the following properties

    Attributes:
        file_name: a string representing the full path of the log file to which
        this logger will write its messages
    """
    def __init__(self, file_name):
        """
        Return a Logger object whose file_name is *file_name* 
        """
        self.file_name = file_name

    def _write_log(self, level, msg):
        with open(self.file_name, "a") as log_file:
            log_file.write("[{0}] {1}\n".format(level, msg))

    def critical(self, msg):
        self._write_log("CRITICAL", msg)

    def error(self, msg):
        self._write_log("ERROR", msg)

    def warn(self, msg):
        self._write_log("WARN", msg)

    def info(self, msg):
        self._write_log("INFO", msg)

    def debug(self, msg):
        self._write_log("DEBUG", msg)
    

if __name__ == "__main__":
    logger_object = Logger("./class_logger.log")
    logger_object.info("This is an info message")