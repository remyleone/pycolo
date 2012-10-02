# coding=utf-8
from pycolo.coap import CodeRegistry
from pycolo.coap import mediaTypeRegistry
from pycolo.endpoint import LocalResource


class DeviceModel(LocalResource):
    """ This resource implements a part of the IPSO profile. """
    def __init__(self):
        """ generated source for method __init__ """
        super(DeviceModel, self).__init__("dev/mdl")
        self.setTitle("Model")
        self.setResourceType("ipso:dev-mdl")
        self.setInterfaceDescription("core#rp")

    def performGET(self, request):
        """ generated source for method performGET """
        #  complete the request
        request.respond(CodeRegistry.RESP_CONTENT, \
                        "Californium", mediaTypeRegistry["TEXT_PLAIN"])
