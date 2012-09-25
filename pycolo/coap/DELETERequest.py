# coding=utf-8
from pycolo.coap import Request


class DELETERequest(Request):
    """ generated source for class DELETERequest """
    def __init__(self):
        """ generated source for method __init__ """
        super(DELETERequest, self).__init__(True)

    def dispatch(self, handler):
        """ generated source for method dispatch """
        handler.performDELETE(self)
