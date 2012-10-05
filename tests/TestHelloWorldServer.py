# coding=utf-8
import logging
import unittest
from pycolo import codes, Endpoint
from pycolo.Resource import Resource


class HelloWorldServer(Endpoint):

    class HelloWorldResource(Resource):
        """ Definition of the Hello-World Resource """
        def __init__(self):
            """ generated source for method __init__ """
            #  set resource identifier
            super(self.HelloWorldResource, self).__init__("helloWorld")
            #  set display name
            self.setTitle("Hello-World Resource")

        def performGET(self, request):
            """ generated source for method performGET
            :param request:
            """
            #  respond to the request
            request.respond(codes.RESP_CONTENT, "Hello World!")

    def __init__(self):
        """
        Constructor for a new Hello-World server. Here, the resources
        of the server are initialized.
        """
        super(HelloWorldServer, self).__init__()
        #  provide an instance of a Hello-World resource
        self.addResource(self.HelloWorldResource())


    def main(cls, args):
        """ Application entry point.
        :param args:
        """
        try:
            #  create server
            print "Server listening on port " + server.port()
        except SocketException as e:
            logging.critical("Failed to initialize server: " + e.getMessage())


if __name__ == '__main__':
    unittest.main()
