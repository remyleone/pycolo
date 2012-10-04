# coding=utf-8
from pycolo import MessageHandler, MessageReceiver, Communicator

from pycolo.endpoint import Resource


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
