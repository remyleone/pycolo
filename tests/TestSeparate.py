# coding=utf-8

from pycolo.codes import mediaCodes
from pycolo import Response


class Separate(Resource):
    """
    This class implements a 'separate' resource for demonstration purposes.
    Defines a resource that returns a response in a separate CoAP Message
    """
    def __init__(self):
        """ generated source for method __init__ """
        self.title = "Resource which cannot be served immediately and which\
         cannot be acknowledged in a piggy-backed way"

    def performGET(self, request):
        """
        we know this stuff may take longer...
        promise the client that this request will be acted upon
        by sending an Acknowledgement
        :param request:
        :return:
        """

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
        response.setContentType(mediaCodes.text)
        #  complete the request
        request.respond(response)
