# coding=utf-8

import random
from pycolo.endpoint import Endpoint
from pycolo.codes import mediaCodes
from pycolo.codes import codes
import unittest
from pycolo.resource import Resource

class DeviceManufacturer(Resource):
    """ This resource implements a part of the IPSO profile. """

    def __init__(self):
        """ generated source for method __init__ """
        super(DeviceManufacturer, self).__init__("dev/mfg")
        self.title = "Manufacturer"
        self.resourceType = "ipso:dev-mfg"
        self.interfaceDescription = "core#rp"

    def performGET(self, request):
        """ generated source for method performGET
        :param request:
        """
        #  complete the request
        request.respond(codes.RESP_CONTENT,\
            "Pycolo", mediaCodes.text)


class DeviceModel(Resource):
    """ This resource implements a part of the IPSO profile. """

    def __init__(self):
        """ generated source for method __init__ """
        super(DeviceModel, self).__init__("dev/mdl")
        self.title = "Model"
        self.resourceType = "ipso:dev-mdl"
        self.setInterfaceDescription("core#rp")

    def performGET(self, request):
        """ generated source for method performGET
        :param request:
        """
        #  complete the request
        request.respond(codes.RESP_CONTENT,\
            "Pycolo", mediaCodes.text)


class DeviceName(Resource):
    """ This resource implements a part of the IPSO profile. """
    name = "IPSO Server"

    def __init__(self):
        """ generated source for method __init__ """
        self.title = "Name"
        self.resourceType = "ipso:dev-n"
        self.interfaceDescription = "core#p"
        self.address = "dev/n"

    def performGET(self, request):
        """ generated source for method performGET
        :param request:
        """
        #  complete the request
        request.respond(codes.RESP_CONTENT,\
            self.name,\
            mediaCodes.text)

    def performPUT(self, request):
        """ generated source for method performPUT
        :param request:
        """
        if request.contentType != mediaCodes.text:
            request.respond(codes.RESP_BAD_REQUEST, "text/plain only")
            return
        self.name = request.payload
        #  complete the request
        request.respond(codes.RESP_CHANGED)


class DeviceSerial(Resource):
    """ This resource implements a part of the IPSO profile. """

    def __init__(self):
        """ generated source for method __init__ """
        super(DeviceSerial, self).__init__("dev/ser")
        self.title = "Serial"
        self.resourceType = "ipso:dev-ser"
        self.interfaceDescription = "core#rp"

    def performGET(self, request):
        """ generated source for method performGET
        :param request:
        """
        #  complete the request
        request.respond(codes.RESP_CONTENT, "4711", mediaCodes.text)


class DeviceBattery(Resource):
    """ This resource implements a part of the IPSO profile. """
    power = 3.6

    def __init__(self):
    #        super(DeviceBattery, self).__init__("dev/bat")
    #        self.title = "Battery"
    #        self.setResourceType("ipso:dev-bat")
    #        #  second rt not supported by current SensiNode RD demo
    #        # setResourceType("ucum:V");
    #        self.setInterfaceDescription("core#s")
    #        self.isObservable(True)
    #        #  Set timer task scheduling
    #        timer = Timer()
    #        timer.schedule(TimeTask(), 0, 1000)

    #class TimeTask():
        """ generated source for class TimeTask """

        def run(self):
            """ generated source for method run """
            self.power -= 0.001 * random.SystemRandom()
            #  Call changed to notify subscribers
            self.changed()

    def performGET(self, request):
        """
        :param request:
        :TODO: Strange call
        """
        #  complete the request
        request.respond(codes.RESP_CONTENT,\
            self.power * 1000 / 1000,\
            mediaCodes.text)


class PowerCumulative(Resource):
    """ This resource implements a part of the IPSO profile. """
    power = 0

    def __init__(self):

    #        super(PowerCumulative, self).__init__("pwr/kwh")
    #        self.title = "Cumulative Power"
    #        self.resourceType = "ipso:pwr-kwh"
    #        #  second rt not supported by current SensiNode RD demo
    #        # setResourceType("ucum:kWh");
    #        self.setInterfaceDescription("core#s")
    #        self.observable = True
    #        #  Set timer task scheduling
    #        timer = Timer()
    #        timer.schedule(TimeTask(), 0, 1000)

    #class TimeTask:

        def run(self):
            """ generated source for method run """

        #            if PowerRelay.getRelay():
        #                self.power += Math.round(10 * random.SystemRandom() * (PowerDimmer.getDimmer() / 100))
        #                #  Call changed to notify subscribers
        #                self.changed()

    def performGET(self, request):
        """ generated source for method performGET
        :param request:
        """
        #  complete the request

#        request.respond(codes.RESP_CONTENT, Double.toString(self.power), mediaCodes.text)

class PowerDimmer(Resource):
    """ This resource implements a part of the IPSO profile. """
    percent = 100

    def __init__(self):
        """ generated source for method __init__ """
        super(PowerDimmer, self).__init__("pwr/dim")
        self.title = "Load Dimmer"
        self.resourceType = "ipso:pwr-dim"
        self.interfaceDescription = "core#a"
        self.observable = True

    def performGET(self, request):
        """ generated source for method performGET
        :param request:
        """
        #  complete the request
        request.respond(codes.RESP_CONTENT,\
            int(self.percent),\
            mediaCodes.text)

    def performPUT(self, request):
        """ generated source for method performPUT
        :param request:
        """
        if request.contentType != mediaCodes.text:
            request.respond(codes.RESP_BAD_REQUEST, "text/plain only")
            return
        pl = int(request.payload)
        if 0 <= pl <= 100:
            if self.percent == pl:
                return
            self.percent = pl
            request.respond(codes.RESP_CHANGED)
            self.changed()
        else:
            request.respond(codes.RESP_BAD_REQUEST, "use 0-100")


class PowerInstantaneous(Resource):
    """ This resource implements a part of the IPSO profile. """
    power = 0

    def __init__(self):
    #        super(PowerInstantaneous, self).__init__("pwr/w")
    #        self.title = "Instantaneous Power"
    #        self.resourceType = "ipso:pwr-w"
    #        #  second rt not supported by current SensiNode RD demo
    #        # setResourceType("ucum:W");
    #        self.interfaceDescription = "core#s"
    #        self.observable = True
    #        #  Set timer task scheduling
    #        timer = Timer()
    #        timer.schedule(TimeTask(), 0, 1000)

    #class TimeTask:
        def run(self):
            pass

        #            """ generated source for method run """
        #            if self.PowerRelay.getRelay():
        #                self.power = 1500 * random.SystemRandom() * (PowerDimmer.getDimmer() / 100)
        #            else:
        #                #  skip changed() update if nothing changed
        #                if self.power == 0:
        #                    return
        #                self.power = 0
        #                #  Call changed to notify subscribers
        #            self.changed()

    def performGET(self, request):
        """ generated source for method performGET
        :param request:
        """
        #  complete the request
        request.respond(codes.RESP_CONTENT,\
            str(self.power),\
            mediaCodes.text)


class PowerRelay(Resource):
    """ This resource implements a part of the IPSO profile. """
    on = True

    def getRelay(cls):
        """ generated source for method getRelay """
        return cls.on

    def __init__(self):
        """ generated source for method __init__ """
        super(PowerRelay, self).__init__("pwr/rel")
        self.setTitle("Load Relay")
        self.setResourceType("ipso:pwr-rel")
        self.setInterfaceDescription("core#a")
        self.isObservable(True)

    def performGET(self, request):
        """ generated source for method performGET
        :param request:
        """
        #  complete the request
        request.respond(codes.RESP_CONTENT,\
            "1" if self.on else "0",\
            mediaCodes.text)

    def performPUT(self, request):
        """ generated source for method performPUT
        :param request:
        """
        if request.contentType != mediaCodes.text:
            request.respond(codes.RESP_BAD_REQUEST, "text/plain only")
            return
        pl = request.getPayloadString()
        if pl == "true" or pl == "1":
            if self.on:
                return
            self.on = True
        elif pl == "false" or pl == "0":
            if not self.on:
                return
            self.on = False
        else:
            request.respond(codes.RESP_BAD_REQUEST,\
                "use true/false or 1/0")
            return
            #  complete the request
        request.respond(codes.RESP_CHANGED)
        self.changed()


class IpsoServer(Endpoint):
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
        Add all initial {@link Resource}s here.
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

    def handleRequest(self, request):
        """ generated source for method handleRequest
        :param request:
        """
        #  Add additional handling like special logging here.
        request.prettyPrint()
        #  dispatch to requested resource
        super(IpsoServer, self).handleRequest(request)

    #  Application entry point /////////////////////////////////////////////////

    def main(cls, args):
        """ generated source for method main
        :param args:
        """
        #  create server

#        try:
#            #  specific handling for this request
#            #  here: response received, output a pretty-print
#            #  RD location
#            if args[0].startsWith("coap://") and len(args):
#                rd = args[0]
#            else:
#                logging.info("Hint: You can give the RD URI as first argument.")
#                logging.info("Fallback to SensiNode RD")
#            if args[1].matches("[A-Za-z0-9-_]+") and len(args):
#                hostname = args[1]
#            else:
#                logging.info("Hint: You can give an alphanumeric (plus '-' and '_') string as second argument to specify a custom hostname.")
#                logging.info("Fallback to hostname")
#                try:
#                    hostname = InetAddress.getLocalHost().getHostName()
#                except UnknownHostException as e1:
#                    print("Unable to retrieve hostname for registration")
#                    print("Fallback to random")
#            register.setURI("%s?h=Cf-%s" % (rd, hostname))
#            register.setPayload(link.serialize(server.getRootResource(), None, True), mediaCodes.APPLICATION_LINK_FORMAT)
#            try:
#                print("Registering at %s as Cf-%s" % (rd, hostname))
#                self.register.execute()
#            except Exception as e:
#                logging.critical("Failed to execute request: %s" % e.getMessage())
#                sys.exit(cls.ERR_INIT_FAILED)
#        except SocketException as e:
#            logging.critical("Failed to create %s: %s\n" % IpsoServer.__class__.getSimpleName(), e.getMessage())
#            sys.exit(cls.ERR_INIT_FAILED)

if __name__ == '__main__':
    unittest.main()
