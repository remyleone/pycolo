# coding=utf-8
import logging

from pycolo.coap import Communicator
from pycolo.coap import Message
from pycolo.coap import MessageHandler
from pycolo.coap import MessageReceiver
from pycolo.coap import Request


class Endpoint(MessageReceiver, MessageHandler):
    """
    The abstract class Endpoint is the basis for the server-sided
    {@link LocalEndpoint} and the client-sided {@link RemoteEndpoint} skeleton.
    """

    rootResource = Resource()

    def execute(self, request):
        """ generated source for method execute """

    def resourceCount(self):
        """ generated source for method resourceCount """
        return self.rootResource.subResourceCount() + 1 if self.rootResource != None else 0

    def receiveMessage(self, msg):
        """ generated source for method receiveMessage """
        msg.handleBy(self)

    def port(self):
        """ generated source for method port """
        return Communicator.getInstance().port()

Endpoint.LOG = Logger.getLogger(Endpoint.__class__.__name__)
