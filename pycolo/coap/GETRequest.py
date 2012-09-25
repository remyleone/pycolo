# coding=utf-8
from pycolo.coap import Request


class GETRequest(Request):

    def __init__(self):
        super(GETRequest, self).__init__(True)

    def dispatch(self, handler):
        handler.performGET(self)
