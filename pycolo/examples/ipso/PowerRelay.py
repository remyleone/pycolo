# coding=utf-8
from pycolo.coap.CodeRegistry import CodeRegistry
from pycolo.coap.MediaTypeRegistry import MediaTypeRegistry
from pycolo.endpoint import LocalResource


class PowerRelay(LocalResource):
    """ This resource implements a part of the IPSO profile. """
    on = True

    @classmethod
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
        """ generated source for method performGET """
        #  complete the request
        request.respond(CodeRegistry.RESP_CONTENT, "1" if self.on else "0", MediaTypeRegistry.TEXT_PLAIN)

    def performPUT(self, request):
        """ generated source for method performPUT """
        if request.getContentType() != MediaTypeRegistry.TEXT_PLAIN:
            request.respond(CodeRegistry.RESP_BAD_REQUEST, "text/plain only")
            return
        pl = request.getPayloadString()
        if pl == "true" or pl == "1":
            if self.on == True:
                return
            self.on = True
        elif pl == "false" or pl == "0":
            if self.on == False:
                return
            self.on = False
        else:
            request.respond(CodeRegistry.RESP_BAD_REQUEST, "use true/false or 1/0")
            return
        #  complete the request
        request.respond(CodeRegistry.RESP_CHANGED)
        self.changed()
