# coding=utf-8
from pycolo.coap.CodeRegistry import CodeRegistry
from pycolo.coap import mediaTypeRegistry
from pycolo.endpoint import LocalResource


class DeviceManufacturer(LocalResource):
    """ This resource implements a part of the IPSO profile. """
    def __init__(self):
        """ generated source for method __init__ """
        super(DeviceManufacturer, self).__init__("dev/mfg")
        self.title = "Manufacturer"
        self.resourceType = "ipso:dev-mfg"
        self.interfaceDescription = "core#rp"

    def performGET(self, request):
        """ generated source for method performGET """
        #  complete the request
        request.respond(CodeRegistry.RESP_CONTENT, \
                        "Pycolo", mediaTypeRegistry["TEXT_PLAIN"])
