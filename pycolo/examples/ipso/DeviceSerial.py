# coding=utf-8

from pycolo.coap import CodeRegistry
from pycolo.coap import MediaTypeRegistry
from pycolo.endpoint import LocalResource
from pycolo import mediaTypeRegistry

class DeviceSerial(LocalResource):
    """ This resource implements a part of the IPSO profile. """
    def __init__(self):
        """ generated source for method __init__ """
        super(DeviceSerial, self).__init__("dev/ser")
        setTitle("Serial")
        setResourceType("ipso:dev-ser")
        setInterfaceDescription("core#rp")

    def performGET(self, request):
        """ generated source for method performGET """
        #  complete the request
        request.respond(CodeRegistry.RESP_CONTENT, "4711", mediaTypeRegistry["TEXT_PLAIN"])
