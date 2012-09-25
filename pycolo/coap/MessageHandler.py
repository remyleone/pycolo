# coding=utf-8
from abc import ABCMeta


class MessageHandler(object):
    """ generated source for interface MessageHandler """
    __metaclass__ = ABCMeta

    @abstractmethod
    def handleRequest(self, request):
        """ generated source for method handleRequest """

    @abstractmethod
    def handleResponse(self, response):
        """ generated source for method handleResponse """
