# coding=utf-8
from abc import ABCMeta


class RequestHandler(object):
    """ generated source for interface RequestHandler """
    __metaclass__ = ABCMeta

    @abstractmethod
    def performGET(self, request):
        """ generated source for method performGET """

    @abstractmethod
    def performPOST(self, request):
        """ generated source for method performPOST """

    @abstractmethod
    def performPUT(self, request):
        """ generated source for method performPUT """

    @abstractmethod
    def performDELETE(self, request):
        """ generated source for method performDELETE """
