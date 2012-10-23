# coding=utf-8

import logging
import socket
import unittest
import sys
from .TestQuery import Query
from .TestSeparate import Separate
from .TestObserve import Observe
from .TestLarge import LargeCreate
from .TestLarge import LargeUpdate
from .TestLarge import Large
from .TestDefault import DefaultResource
from pycolo.endpoint import Endpoint


class PlugtestServer(Endpoint):
    """
    The class PlugtestServer implements the test specification for the
    ETSI IoT CoAP Plugtests, Paris, France, 24 - 25 March 2012.
    """
    #  exit codes for runtime errors
    ERR_INIT_FAILED = 1

    def __init__(self):
        #  add resources to the server
        self.addResource(DefaultResource())
        self.addResource(Query())
        self.addResource(Separate())
        self.addResource(Large())
        self.addResource(LargeUpdate())
        self.addResource(LargeCreate())
        self.addResource(Observe())

    def handleRequest(self, request):
        """ generated source for method handleRequest
        :param request:
        """
        str(request)
        PlugtestServer.handleRequest(request)  # dispatch to requested resource


class TestSeparate(unittest.TestCase):

    def setUp(self):
        sep = Separate()



if __name__ == '__main__':
    unittest.main()
