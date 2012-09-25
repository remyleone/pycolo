# coding=utf-8
from pycolo.coap import Request


class POSTRequest(Request):
    def __init__(self):
        super(POSTRequest, self).__init__(True)

    def dispatch(self, handler):
        handler.performPOST(self)
