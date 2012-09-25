# coding=utf-8
from pycolo.coap import Request


class PUTRequest(Request):
    def __init__(self):
        super(PUTRequest, self).__init__(True)

    def dispatch(self, handler):
        handler.performPUT(self)
