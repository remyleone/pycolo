# coding=utf-8

from pycolo.coap.CodeRegistry import CodeRegistry
from pycolo.coap import Response
from pycolo.endpoint import LocalResource


class Separate(LocalResource):
    """
    This class implements a 'separate' resource for demonstration purposes.
    Defines a resource that returns a response in a separate CoAP Message
    """
    def __init__(self):
        """ generated source for method __init__ """
        super(Separate, self).__init__("separate")
        self.setTitle("Resource which cannot be served immediately and which\
         cannot be acknowledged in a piggy-backed way")

    def performGET(self, request):
        """ generated source for method performGET """
        #  we know this stuff may take longer...
        #  promise the client that this request will be acted upon
        #  by sending an Acknowledgement
        request.accept()
        #  do the time-consuming computation
        try:
            Thread.sleep(1000)
        except Exception as e:
            e.stacktrace()

        response = Response(CodeRegistry.RESP_CONTENT)  # create response
        #  set payload
        response.payload = "Type: {:d} ({:s})\nCode: {:d} ({:s})\nMID: {:d}" % \
            request.type.ordinal(), \
            request.typeString(), \
            request.code, \
            CodeRegistry.(request.code), \
            request.getMID()))
        response.setContentType(MediaTypeRegistry.TEXT_PLAIN)
        #  complete the request
        request.respond(response)
