# coding=utf-8

from pycolo import resource
from pycolo.codes import mediaCodes, codes
from pycolo.message import Response


class ImageResource(resource):
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
        self.supported.append(codes.mediaCodes["IMAGE_PNG"])
        self.supported.append(codes.mediaCodes["IMAGE_JPEG"])
        self.supported.append(codes.mediaCodes["IMAGE_GIF"])
        self.supported.append(codes.mediaCodes["IMAGE_TIFF"])
        for ct in self.supported:
            self.contentTypeCode += ct
        self.maximumSizeEstimate = 18029
        self.observable = False

    def performGET(self, request):

        """
        Give back a image in a binary form.
        :param request:
        """
        ct = mediaCodes.IMAGE_PNG
        fileData = bytearray()  # load representation from file
        with open("img/python.png") as f:
            fileData = f.read()
        response = Response(codes.RESP_CONTENT)
        response.payload = fileData
        response.contentType = ct  # set content type
        request.respond(response)  # complete the request
