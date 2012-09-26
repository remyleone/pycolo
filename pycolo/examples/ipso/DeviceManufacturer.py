# coding=utf-8
from pycolo.coap import CodeRegistry
from pycolo.coap.MediaTypeRegistry import MediaTypeRegistry
from pycolo.endpoint import LocalResource


class DeviceManufacturer(LocalResource):
    """ This resource implements a part of the IPSO profile. """
    def __init__(self):
        """ generated source for method __init__ """
        super(DeviceManufacturer, self).__init__("dev/mfg")
        self.setTitle("Manufacturer")
        self.setResourceType("ipso:dev-mfg")
        self.setInterfaceDescription("core#rp")

    def performGET(self, request):
        """ generated source for method performGET """
        #  complete the request
        request.respond(CodeRegistry.RESP_CONTENT, "ETH Zurich", MediaTypeRegistry.TEXT_PLAIN)
