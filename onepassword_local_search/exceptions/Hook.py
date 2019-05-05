from os import environ
from sys import excepthook, stderr


def exception_handler(exception_type, exception, traceback):
    if environ.get('DEBUG'):
        excepthook(exception_type, exception, traceback)
    else:
        print("%s" % exception, file=stderr)
