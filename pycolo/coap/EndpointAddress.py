# coding=utf-8
import java.net.Inet6Address
import java.net.InetAddress
import java.net.URI
import java.net.UnknownHostException
import java.util.logging.Logger
import ch.ethz.inf.vs.californium.util.Properties


class EndpointAddress(object):
    """
    The class EndpointAddress stores IP address and port.
    It is mainly used to handle {@link Message}s.
    """
    #  Logging ////////////////////////////////////////////////////////////////
    #  Members ////////////////////////////////////////////////////////////////
    #  The address.
    address = None

    #  The port.
    port = Properties.std.getInt("DEFAULT_PORT")

    #  Constructors ///////////////////////////////////////////////////////////
    #
    # 	 * Instantiates a new endpoint address using the default port.
    # 	 *
    # 	 * @param address the IP address
    #
    @overloaded
    def __init__(self, address):
        """ generated source for method __init__ """
        self.address = address

    #
    # 	 * Instantiates a new endpoint address, setting both, IP and port.
    # 	 *
    # 	 * @param address the IP address
    # 	 * @param port the custom port
    #
    @__init__.register(object, InetAddress, int)
    def __init___0(self, address, port):
        """ generated source for method __init___0 """
        self.address = address
        self.port = port

    # 
    # 	 * A convenience constructor that takes the address information from a URI object.
    # 	 *
    # 	 * @param uri the URI
    # 	 
    @__init__.register(object, URI)
    def __init___1(self, uri):
        """ generated source for method __init___1 """
        #  Allow for correction later, as host might be unknown at initialization time.
        try:
            self.address = InetAddress.getByName(uri.getHost())
        except UnknownHostException as e:
            self.LOG.warning("Cannot fully initialize: {:s}".format(e.getMessage()))
        if uri.getPort() != -1:
            self.port = uri.getPort()

    #  Methods ////////////////////////////////////////////////////////////////
    #  (non-Javadoc)
    # 	 * @see java.lang.Object#toString()
    # 	 
    def __str__(self):
        """ generated source for method toString """
        if isinstance(, (Inet6Address,)):
            return "[{:s}]:{:d}".format(self.address.getHostAddress(), self.port)
        else:
            return "{:s}:{:d}".format(self.address.getHostAddress(), self.port)

    def getAddress(self):
        """ Returns the IP address. """
        return self.address

    def getPort(self):
        """ Returns the port number. """
        return self.port

EndpointAddress.LOG = Logger.getLogger(EndpointAddress.__class__.__name__)
