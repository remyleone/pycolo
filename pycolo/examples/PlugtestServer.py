# coding=utf-8

import logging
from pycolo.endpoint import LocalEndpoint


class PlugtestServer(LocalEndpoint):
    """
    The class PlugtestServer implements the test specification for the
    ETSI IoT CoAP Plugtests, Paris, France, 24 - 25 March 2012.
    """
    #  exit codes for runtime errors
    ERR_INIT_FAILED = 1

    def __init__(self):
        """ generated source for method __init__ """
        super(PlugtestServer, self).__init__()
        #  add resources to the server
        self.addResource(DefaultTest())
        self.addResource(LongPath())
        self.addResource(Query())
        self.addResource(Separate())
        self.addResource(Large())
        self.addResource(LargeUpdate())
        self.addResource(LargeCreate())
        self.addResource(Observe())

    #  Logging /////////////////////////////////////////////////////////////////
    def handleRequest(self, request):
        """ generated source for method handleRequest """
        #  Add additional handling like special logging here.
        request.prettyPrint()
        #  dispatch to requested resource
        super(PlugtestServer, self).handleRequest(request)

    #  Application entry point /////////////////////////////////////////////////
    @classmethod
    def main(cls, args):
        """ generated source for method main """
        #  create server
        try:
            System.out.printf(PlugtestServer.__class__.getSimpleName() + " listening on port %d.\n", server.port())
        except SocketException as e:
            logging.critical("Failed to create " + PlugtestServer.__class__.getSimpleName() + ": %s\n", e.getMessage())
            System.exit(cls.ERR_INIT_FAILED)


if __name__ == '__main__':
    import sys
    PlugtestServer.main(sys.argv)
