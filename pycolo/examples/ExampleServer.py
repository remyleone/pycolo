# coding=utf-8

import logging
from pycolo.endpoint import LocalEndpoint
from pycolo.examples.resources import CarelessResource
from pycolo.examples.resources import HelloWorldResource
from pycolo.examples.resources import ImageResource
from pycolo.examples.resources import LargeResource
from pycolo.examples.resources import SeparateResource
from pycolo.examples.resources import StorageResource
from pycolo.examples.resources import TimeResource
from pycolo.examples.resources import ToUpperResource
from pycolo.examples.resources import ZurichWeatherResource


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
        super(ExampleServer, self).__init__()
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
        """ generated source for method handleRequest """
        #  Add additional handling like special logging here.
        request.prettyPrint()
        #  dispatch to requested resource
        super(ExampleServer, self).handleRequest(request)

    #  Application entry point /////////////////////////////////////////////////
    @classmethod
    def main(cls, args):
        """ generated source for method main """
        Log.init()
        #  create server
        try:
            logging.info("ExampleServer listening on port %d.\n", server.port())
        except SocketException as e:
            System.err.printf("Failed to create SampleServer: %s\n", e.getMessage())
            System.exit(cls.ERR_INIT_FAILED)

ExampleServer.# 	 * Constructor for a new ExampleServer. Call {@code super(...)} to configure


if __name__ == '__main__':
    import sys
    ExampleServer.main(sys.argv)
