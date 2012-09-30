import logging

import java.net.SocketException
from pycolo.coap import CodeRegistry
from pycolo.endpoint import LocalEndpoint
from pycolo.endpoint import LocalResource


class HelloWorldServer(LocalEndpoint):

    class HelloWorldResource(LocalResource):
        """ Definition of the Hello-World Resource """
        def __init__(self):
            """ generated source for method __init__ """
            #  set resource identifier
            super(self.HelloWorldResource, self).__init__("helloWorld")
            #  set display name
            self.setTitle("Hello-World Resource")

        def performGET(self, request):
            """ generated source for method performGET """
            #  respond to the request
            request.respond(CodeRegistry.RESP_CONTENT, "Hello World!")

    def __init__(self):
        """
        Constructor for a new Hello-World server. Here, the resources
        of the server are initialized.
        """
        super(HelloWorldServer, self).__init__()
        #  provide an instance of a Hello-World resource
        self.addResource(self.HelloWorldResource())


    @classmethod
    def main(cls, args):
        """ Application entry point. """
        try:
            #  create server
            print "Server listening on port " + server.port()
        except SocketException as e:
            logging.critical("Failed to initialize server: " + e.getMessage())


if __name__ == '__main__':
    import sys
    HelloWorldServer.main(sys.argv)
