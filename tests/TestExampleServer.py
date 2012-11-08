# coding=utf-8

import http
import logging
import unittest
from pycolo.codes import options, codes, mediaCodes
from pycolo.endpoint import Endpoint
from pycolo.resource import Resource


class ToUpperResource(Resource):
    """
    This class implements a 'toUpper' resource for demonstration purposes.
    Defines a resource that returns a POSTed string in upper-case letters.
    """
    def __init__(self):
        self.title = "POST text here to convert it to uppercase"
        self.resourceType = "UppercaseConverter"

    def performPOST(self, request):

        if request.contentType != mediaCodes.text:
            request.respond(codes.RESP_UNSUPPORTED_MEDIA_TYPE, "Use text/plain")
            return
            #  complete the request
        request.respond(codes.RESP_CONTENT, request.payload.upper(), mediaCodes.text)


class ExampleServer(Endpoint):
    """
    The class ExampleServer shows how to implement a server by extending
    {@link LocalEndpoint}. In the implementation class, use
    {@link LocalEndpoint#addResource(ch.ethz.inf.vs.californium.endpoint.LocalResource)}
    to add custom resources extending {@link LocalResource}.
    """
    #  exit codes for runtime errors
    ERR_INIT_FAILED = 1

    def __init__(self):
        """
        the port, etc. according to the {@link LocalEndpoint} constructors.
        Add all initial {@link LocalResource}s here.
        """
        #  add resources to the server
        self.addResource(HelloWorldResource())
        self.addResource(ToUpperResource())
        self.addResource(StorageResource())
        self.addResource(SeparateResource())
        self.addResource(LargeResource())
        self.addResource(TimeResource())
        self.addResource(ParisWeatherResource())
        self.addResource(ImageResource())
        self.addResource(CarelessResource())


if __name__ == '__main__':
    unittest.main()
