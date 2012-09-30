import java.net.InetAddress
import java.net.SocketException
import java.net.UnknownHostException
import java.util.logging.Level
import logging
from pycolo.coap import LinkFormat
from pycolo.coap import MediaTypeRegistry
from pycolo.endpoint import LocalEndpoint


class IpsoServer(LocalEndpoint):
    """
    The class IpsoServer provides an example of the IPSO Profile specification.
    The server registers its resources at the SensiNode Resource Directory.
    """
    #  exit codes for runtime errors
    ERR_INIT_FAILED = 1

    def __init__(self):
        """
        Constructor for a new PlugtestServer.Call to configure
        the port, etc. according to the {@link LocalEndpoint} constructors.
        Add all initial {@link LocalResource}s here.
        """
        super(IpsoServer, self).__init__()
        #  add resources to the server
        self.addResource(DeviceName())
        self.addResource(DeviceManufacturer())
        self.addResource(DeviceModel())
        self.addResource(DeviceSerial())
        self.addResource(DeviceBattery())
        self.addResource(PowerInstantaneous())
        self.addResource(PowerCumulative())
        self.addResource(PowerRelay())
        self.addResource(PowerDimmer())

    #  Logging ////////////////////////////////////////////////////////////////
    def handleRequest(self, request):
        """ generated source for method handleRequest """
        #  Add additional handling like special logging here.
        request.prettyPrint()
        #  dispatch to requested resource
        super(IpsoServer, self).handleRequest(request)

    #  Application entry point /////////////////////////////////////////////////
    @classmethod
    def main(cls, args):
        """ generated source for method main """
        #  create server
        try:
            logging.info(IpsoServer.__class__.getSimpleName() + " listening on port %d.\n", server.port())
            #  specific handling for this request
            #  here: response received, output a pretty-print
            #  RD location
            if args[0].startsWith("coap://") and len(args):
                rd = args[0]
            else:
                print "Hint: You can give the RD URI as first argument."
                print "Fallback to SensiNode RD"
            if args[1].matches("[A-Za-z0-9-_]+") and len(args):
                hostname = args[1]
            else:
                print "Hint: You can give an alphanumeric (plus '-' and '_') string as second argument to specify a custom hostname."
                print "Fallback to hostname"
                try:
                    hostname = InetAddress.getLocalHost().getHostName()
                except UnknownHostException as e1:
                    print "Unable to retrieve hostname for registration"
                    print "Fallback to random"
            register.setURI(rd + "?h=Cf-" + hostname)
            register.setPayload(LinkFormat.serialize(server.getRootResource(), None, True), MediaTypeRegistry.APPLICATION_LINK_FORMAT)
            try:
                print("Registering at " + rd + " as Cf-" + hostname)
                register.execute()
            except Exception as e:
                System.err.println("Failed to execute request: " + e.getMessage())
                System.exit(cls.ERR_INIT_FAILED)
        except SocketException as e:
            System.err.printf("Failed to create " + IpsoServer.__class__.getSimpleName() + ": %s\n", e.getMessage())
            System.exit(cls.ERR_INIT_FAILED)


if __name__ == '__main__':
    import sys
    IpsoServer.main(sys.argv)
