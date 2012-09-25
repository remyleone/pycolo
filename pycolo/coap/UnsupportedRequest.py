# coding=utf-8
import logging

from pycolo.coap import Request


class UnsupportedRequest(Request):
    """ generated source for class UnsupportedRequest """
    def __init__(self, code_):
        """ generated source for method __init__ """
        super(UnsupportedRequest, self).__init__(code_)

    def send(self):
        """ generated source for method send """
        logging.critical("Cannot send UnsupportedRequest")
