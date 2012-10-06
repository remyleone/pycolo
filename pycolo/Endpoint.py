# coding=utf-8
from pycolo import MessageHandler, MessageReceiver, Communicator

from pycolo.endpoint import Resource
from pycolo import DEFAULT_PORT


class EndpointAddress:

    address = None

    def __init__(self, address, port=DEFAULT_PORT):
        """
        Instantiates a new endpoint address using the default port.
        A convenience constructor that takes the address information from a
        URI object.
        Allow for correction later, as host might be unknown at initialization
        time.

        @param address the IP address
        @param port the custom port
        """
        self.address = address
        self.port = port
        try:
            self.address = InetAddress.getByName(uri.getHost())
        except Exception as e:
            logging.info("Cannot fully initialize: {:s}".format(e.getMessage()))
        if uri.getPort() != -1:
            self.port = uri.getPort()

    def __str__(self):
        """ generated source for method toString """
        if isinstance(, (Inet6Address,)):
            return "[{:s}]:{:d}".format(self.address.getHostAddress(), self.port)
        else:
            return "{:s}:{:d}".format(self.address.getHostAddress(), self.port)



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
        return self.rootResource.subResourceCount() + 1 if self.rootResource is not None else 0

    def receiveMessage(self, msg):
        """ generated source for method receiveMessage """
        msg.handleBy(self)

    def port(self):
        """ generated source for method port """
        return Communicator.getInstance().port()
