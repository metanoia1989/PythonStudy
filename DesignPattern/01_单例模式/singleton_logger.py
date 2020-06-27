#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
单例模式
控制对象创建过程的控制权
"""
class Logger(object):
    class __SingleLogger():
        def __init__(self, file_name):
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


        # the rest of the class definition will folow here, as per the previous logging script 
    instance = None

    def __new__(cls, file_name):
        if not cls.instance:
            cls.instance = cls.__SingleLogger(file_name)
        return cls.instance

    def __getattr__(self, name):
        func = getattr(self.instance, name, None)
        if callable(func):
            func()
            
        
if __name__ == "__main__":
    logger = Logger('./singleton_logger.log')
    logger.info(type(logger))
    logger.warn('The is your first warning!')