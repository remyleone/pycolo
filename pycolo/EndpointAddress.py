# coding=utf-8

from pycolo.coap import DEFAULT_PORT
import logging


class EndpointAddress:
    """
    The class EndpointAddress stores IP address and port.
    It is mainly used to handle {@link Message}s.
    """

    address = None

    port = DEFAULT_PORT

    @overloaded
    def __init__(self, address):
        """
        Instantiates a new endpoint address using the default port.
        @param address the IP address
        @param port the custom port
        """
        self.address = address
        self.port = port

    @__init__.register(object, URI)
    def __init___1(self, uri):
        """
        A convenience constructor that takes the address information from a
        URI object.
        Allow for correction later, as host might be unknown at initialization
        time.
        """
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
