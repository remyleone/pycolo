# coding=utf-8

"""
TODO
"""

import unittest

from pycolo.codes import mediaCodes, codes
from pycolo.endpoint import Endpoint
from pycolo.message import Response
from pycolo.resource import Resource


class ImageResource(Resource):
    """
    This class implements an "/image" resource for demonstration purposes.

    Provides different representations of an image through supports content
    negotiation.
    The required files are provided through the folder of the source.
    Make sure to fix the location when running elsewhere.
    """
    supported = list()

    def __init__(self):
        self.title = "GET an image with different content-types"
        self.resourceType = "Image"
        self.supported.append(mediaCodes.png)
        self.supported.append(mediaCodes.jpeg)
        self.supported.append(mediaCodes.gif)
        self.supported.append(mediaCodes.tiff)
        for ct in self.supported:
            self.contentTypeCode += ct
        self.maximumSizeEstimate = 18029
        self.observable = False

    def performGET(self, request):
        """
        Give back a image in a binary form.
        :param request:
        """
        ct = mediaCodes.png
        fileData = bytearray()  # load representation from file
        with open("img/python.png") as f:
            fileData = f.read()
        response = Response(codes.RESP_CONTENT)
        response.payload = fileData
        response.contentType = ct  # set content type
        request.respond(response)  # complete the request


class TestImageResource(unittest.TestCase):
    """
    TODO
    """

    def setUp(self):
        """
        TODO
        """
        server = Endpoint()
        res = ImageResource()
        server.register(res)


if __name__ == '__main__':
    unittest.main()
