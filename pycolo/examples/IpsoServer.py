# coding=utf-8

import logging
from pycolo.coap import LinkFormat
from pycolo.coap import mediaTypeRegistry
from pycolo.endpoint import LocalEndpoint
from .ipso import DeviceName
from .ipso import DeviceManufacturer
from .ipso import DeviceModel
from .ipso import DeviceSerial
from .ipso import DeviceBattery
from .ipso import PowerInstantaneous
from .ipso import PowerCumulative
from .ipso import PowerRelay
from .ipso import PowerDimmer


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
                logging.info("Hint: You can give the RD URI as first argument.")
                logging.info("Fallback to SensiNode RD")
            if args[1].matches("[A-Za-z0-9-_]+") and len(args):
                hostname = args[1]
            else:
                logging.info("Hint: You can give an alphanumeric (plus '-' and '_') string as second argument to specify a custom hostname.")
                logging.info("Fallback to hostname")
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
                logging.critical("Failed to execute request: " + e.getMessage())
                sys.exit(cls.ERR_INIT_FAILED)
        except SocketException as e:
            logging.critical("Failed to create " + IpsoServer.__class__.getSimpleName() + ": %s\n", e.getMessage())
            sys.exit(cls.ERR_INIT_FAILED)
