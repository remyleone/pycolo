# coding=utf-8
from abc import ABCMeta


class ResponseHandler(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def handleResponse(self, response):
        pass
