# coding=utf-8

import logging
from pycolo import LocalEndpoint
from tests.resources import CarelessResource, SeparateResource, StorageResource, ImageResource, LargeResource, TimeResource
from tests.resources import ZurichWeatherResource
from tests.resources import ToUpperResource, HelloWorldResource
import unittest


class ExampleServer(LocalEndpoint):
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
        self.addResource(ZurichWeatherResource())
        self.addResource(ImageResource())
        self.addResource(CarelessResource())

    def handleRequest(self, request):
        """ generated source for method handleRequest
        :param request:
        """
        #  Add additional handling like special logging here.
        request.prettyPrint()
        #  dispatch to requested resource
        super(ExampleServer, self).handleRequest(request)

    #  Application entry point /////////////////////////////////////////////////

    def main(cls, args):
        #  create server
        """

        :param cls:
        :param args:
        """
        try:
            logging.info("ExampleServer listening on port %d.\n", server.port())
        except SocketException as e:
            logging.critical("Failed to create SampleServer: %s\n", e.getMessage())
            sys.exit(cls.ERR_INIT_FAILED)

ExampleServer.# 	 * Constructor for a new ExampleServer. Call {@code super(...)} to configure


if __name__ == '__main__':
    unittest.main()
