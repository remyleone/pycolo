# coding=utf-8

import logging
from pycolo import Response, Resource, codes


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
        """ generated source for method __init__ """
        super(ImageResource, self).__init__()
        self.__init__("image")

    @__init__.register(object, str)
    def __init___0(self, resourceIdentifier):
        """ generated source for method __init___0 """
        super(ImageResource, self).__init__(resourceIdentifier)
        self.title = "GET an image with different content-types"
        self.setResourceType("Image")
        self.supported.append(codes.mediaCodes["IMAGE_PNG"])
        self.supported.append(codes.mediaCodes["IMAGE_JPEG"])
        self.supported.append(codes.mediaCodes["IMAGE_GIF"])
        self.supported.append(codes.mediaCodes["IMAGE_TIFF"])
        for ct in self.supported:
            self.contentTypeCode += ct
        self.maximumSizeEstimate = 18029
        self.observable = False

    #  REST Operations /////////////////////////////////////////////////////////
    def performGET(self, request):
        """ generated source for method performGET
        :param request:
        """
        filename = "data/image/"
        ct = mediaTypeRegistry.IMAGE_PNG
        #  content negotiation
        if (ct=MediaTypeRegistry.contentNegotiation(ct, self.supported, request.getOptions(OptionNumberRegistry.ACCEPT))) == MediaTypeRegistry.UNDEFINED:
            request.respond(codes.RESP_NOT_ACCEPTABLE, "Accept GIF, JPEG, PNG, or TIFF")
            return
        filename += "image." + MediaTypeRegistry.toFileExtension(ct)
        # load representation from file
        file_ = File(filename)
        if not file_.exists():
            request.respond(codes.RESP_INTERNAL_SERVER_ERROR, "Representation not found")
            return
        # get length of file
        fileLength = int(len(file_))
        fileIn = None
        fileData = [None] * fileLength
        try:
            # open input stream from file
            fileIn = FileInputStream(file_)
            # read file into byte array
            fileIn.read(fileData)
            fileIn.close()
        except Exception as e:
            request.respond(codes.RESP_INTERNAL_SERVER_ERROR, "IO error")
            logging.critical("/image IO error: " + e.getMessage())
            return
        #  create response
        response = Response(codes.RESP_CONTENT)
        response.payload = fileData
        response.setContentType(ct)  # set content type
        request.respond(response)  # complete the request