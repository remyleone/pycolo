# coding=utf-8

"""
TODO
"""

import unittest

from pycolo import codes
from pycolo.codes import mediaCodes
from pycolo.endpoint import Endpoint
from pycolo.message import Response
from pycolo.resource import Resource

class LargeResource(Resource):
    """
    TODO
    """

    def performGET(self, request):
        """
        TODO
        """
        builder = "7" * 8 * 3

        request.respond(codes.RESP_CONTENT, builder.__str__())


class Large(Resource):
    """
    This class implements a resource that returns a larger amount of
    data on GET requests in order to test blockwise transfers.

    Large resources used in TD_COAP_BLOCK tests shall not exceed 2048 bytes

    This resource implements a test of specification for the ETSI IoT CoAP
    Plugtests, Paris, France, 24 - 25 March 2012.

    TD_COAP_BLOCK_01
    TD_COAP_BLOCK_02
    """

    def __init__(self, name="/large"):
        self.title = "This is a large resource for testing block-wise transfer. Large resource (>1024 bytes) "
        self.name = name
        self.resourceType = "BlockWiseTransferTester"

    def performGET(self, request):
        """ generated source for method performGET
        :param request:
        """
        builder = 4 * 5 * 64 * "7"
        request.respond(codes.RESP_CONTENT, str(builder), mediaCodes.text)


class LargeCreate(Resource):
    """
    Large resource that can be created using POST method (>1024 bytes)
    Large resources used in TD_COAP_BLOCK tests shall not exceed 2048 bytes

    This resource implements a test of specification for the
    ETSI IoT CoAP Plugtests, Paris, France, 24 - 25 March 2012.

    TD_COAP_BLOCK_04
    """

    data = None
    dataCt = -1

    def __init__(self, name="/large_create"):
        """
        Constructs a new storage resource with the given resourceIdentifier.
        """
        self.name = name
        self.title = "Large resource that can be created using POST method"
        self.resourceType = "block"

    def performGET(self, request):
        """
        :param request:
        """

    #        response = None
    #        if not self.data:
    #            response = Response(codes.RESP_CONTENT)
    #            response.setPayload("Nothing posted yet", mediaCodes.text)
    #        else:
    #            #  content negotiation
    #            self.supported.add(self.dataCt)
    #            if ct = mediaCodes.contentNegotiation(self.dataCt, self.supported, request.getOptions(options.ACCEPT))) == var = MediaTypeRegistry.UNDEFINED
    #            :
    #            request.respond(codes.RESP_NOT_ACCEPTABLE, "Accept %s" % mediaCodes.toString(self.dataCt))
    #            return
    #            response = Response(codes.RESP_CONTENT)
    #
    #            response.payload = self.data  # load data into payload
    #            response.setContentType(ct)  # set content type
    #
    #        request.respond(response)  # complete the request

    def performPOST(self, request):
        """ POST content to create this resource.
        :param request:
        """
        if request.getContentType() == mediaCodes.UNDEFINED:
            request.respond(codes.RESP_BAD_REQUEST, "Content-Type not set")
            return
            #  store payload
        self.storeData(request)
        #  create new response
        response = Response(codes.RESP_CREATED)
        #  inform client about the location of the new resource
        response.setLocationPath("/nirvana")
        #  complete the request
        request.respond(response)

    def performDELETE(self, request):
        """ DELETE the data and act as resouce was deleted.
        :param request:
        """
        #  delete
        self.data = None
        #  complete the request
        request.respond(Response(codes.RESP_DELETED))

        #  Internal ////////////////////////////////////////////////////////////////
        #
        # 	 * Convenience function to store data contained in a
        # 	 * PUT/POST-Request. Notifies observing endpoints about
        # 	 * the change of its contents.
        #
        #
        # 	private synchronized void storeData(Request request) {
        #  set payload and content type
        # 		data = request.getPayload();
        # 		dataCt = request.getContentType();
        # 		clearAttribute(LinkFormat.CONTENT_TYPE);
        # 		setContentTypeCode(dataCt);
        #  signal that resource state changed
        # 		changed();
        # 	}


class LargeUpdate(Resource):
    """
    Large resource that can be updated using PUT method (>1024 bytes)
    Large resources used in TD_COAP_BLOCK tests shall not exceed 2048 bytes

    This resource implements a test of specification for the ETSI IoT CoAP
    Plugtests, Paris, France, 24 - 25 March 2012.

    TD_COAP_BLOCK_03
    """
    data = None
    dataCt = mediaCodes.text

    def __init__(self):
        """
        Constructs a new storage resource with the given resourceIdentifier.
        """
        self.name = "large-update"
        self.title = "Large resource that can be updated using PUT method"
        self.resourceType = "block"


    def performGET(self, request):
        """
        GETs the content of this storage resource.
        If the content-type of the request is set to application/link-format
        or if the resource does not store any data, the contained sub-resources
        are returned in link format.
        :param request:
        """
        #  content negotiation

    #        supported = list()
    #        supported.add(self.dataCt)
    #        ct = mediaCodes.png
    #        if ct = mediaCodes.contentNegotiation(self.dataCt, supported, request.getOptions(options.ACCEPT))) == var = mediaCodes.UNDEFINED:
    #        request.respond(codes.RESP_NOT_ACCEPTABLE, "Accept %s" % mediaCodes.toString(self.dataCt))
    #        return
    #        #  create response
    #        response = Response(codes.RESP_CONTENT)
    #        if self.data is None:
    #            builder = """
    #            /-------------------------------------------------------------\
    #            |                 RESOURCE BLOCK NO. 1 OF 5                   |
    #            |               [each line contains 64 bytes]                 |
    #            \------------------------------------------------------------/
    #            /-------------------------------------------------------------\
    #            |                 RESOURCE BLOCK NO. 2 OF 5                   |
    #            |               [each line contains 64 bytes]                 |
    #            \------------------------------------------------------------/
    #            /-------------------------------------------------------------\
    #            |                 RESOURCE BLOCK NO. 3 OF 5                   |
    #            |               [each line contains 64 bytes]                 |
    #            \------------------------------------------------------------/
    #            /-------------------------------------------------------------\
    #            |                 RESOURCE BLOCK NO. 4 OF 5                   |
    #            |               [each line contains 64 bytes]                 |
    #            \------------------------------------------------------------/
    #            /-------------------------------------------------------------\
    #            |                 RESOURCE BLOCK NO. 5 OF 5                   |
    #            |               [each line contains 64 bytes]                 |
    #            \------------------------------------------------------------/
    #            """
    #            request.respond(codes.RESP_CONTENT, builder.__str__(), ct)
    #        else:
    #            #  load data into payload
    #            response.payload = self.data
    #            #  set content type
    #            response.setContentType(ct)
    #            #  complete the request
    #            request.respond(response)

    def performPUT(self, request):
        """ generated source for method performPUT
        :param request:
        """

    #        if request.getContentType() == mediaCodes.UNDEFINED:
    #            request.respond(codes.RESP_BAD_REQUEST, "Content-Type not set")
    #            return
    #            #  store payload
    #        self.storeData(request)
    #        #  complete the request
    #        request.respond(codes.RESP_CHANGED)

    def storeData(self, request):
        """
        Convenience function to store data contained in a
        PUT/POST-Request. Notifies observing endpoints about
        the change of its contents.
        :param request:
        :return:
        """
        # set payload and content type

#        data = request.payload
#        dataCt = request.contentType
#        self.clearAttribute(LinkFormat.CONTENT_TYPE)
#        self.setContentTypeCode(dataCt)
#        # signal that resource state changed
#        self.changed()


class TestLarge(unittest.TestCase):
    """
    TODO
    """

    def setUp(self):
        """
        TODO
        """
        server = Endpoint()
        res = Large()
        server.register(res)

    def test_GET_block_early(self):
        """
        Identifier: TD_COAP_BLOCK_01
        Objective: Handle GET blockwise transfer for large resource (early negotiation)
        Configuration: CoAP_CFG_01

        Pre-test conditions:
            • Client supports Block transfers
            • Server supports Block transfers
            • Server offers a large resource /large
            • Client knows /large requires block transfer

        Step 1 stimulus Client is requested to retrieve resource /large

        Step 2 (check (CON)) Client sends a GET request containing Block2 option
        indicating block number 0 and desired block size

        Step 3 (check (CON)) Server sends response containing
        Block2 option indicating block number and size

        Step 4 (check (CON)) Client send GET requests for further blocks

        Step 5 (check (CON)) Each request contains Block2 option indicating block number
        of the next block and size of the last received block

        Step 6 (check (CON)) Server sends further responses containing
        Block2 option indicating block number and size

        Step 7 (verify (IOP)) Client displays the received information
        """
        pass

    def test_GET_block_late(self):
        """
        Identifier: TD_COAP_BLOCK_02
        Objective: Handle GET blockwise transfer for large resource (late negotiation)
        Configuration: CoAP_CFG_01

        Pre-test conditions:
            • Client supports Block transfers
            • Server supports Block transfers
            • Server offers a large resource /large
            • Client does not know /large requires block transfer

        Step 1 stimulus Client is requested to retrieve resource /large

        Step 2 (check (CON)) Client sends a GET request not containing Block2 option

        Step 3 (check (CON)) Server sends response containing
        Block2 option indicating block number and size

        Step 4 (check (CON)) Client send GET requests for further blocks

        Step 5 (check (CON)) Each request contains Block2 option indicating block number
        of the next block and size of the last received block or the
        desired size of next block

        Step 6 (check (CON)) Server sends further responses containing
        Block2 option indicating block number and size

        Step 7 (verify (IOP)) Client displays the received information
        """
        pass

    def test_PUT_block(self):
        """
        Identifier: TD_COAP_BLOCK_03
        Objective: Handle PUT blockwise transfer for large resource
        Configuration: CoAP_CFG_01

        Pre-test conditions:
            • Client supports Block transfers
            • Server supports Block transfers
            • Server offers a large updatable resource /large-update

        Step 1 (stimulus) Client is requested to update resource /large-update on
        Server

        Step 2 (check (CON)) Client sends a PUT request containing Block1 option
        indicating block number 0 and block size

        Step 3 (check (CON)) Client sends further requests containing
        Block1 option indicating block number and size

        Step 4 (verify (IOP)) Server indicates presence of the complete updated resource
        /large-update
        """
        pass

    def test_POST_block(self):
        """
        Identifier: TD_COAP_BLOCK_04
        Objective: Handle POST blockwise transfer for large resource
        Configuration: CoAP_CFG_01

        Pre-test conditions:
            • Client supports Block transfers
            • Server supports Block transfers
            • Server accepts creation of new resources on /large-create

        Step 1 stimulus Client is requested to create a new resource on Server

        Step 2 (check (CON)) Client sends a POST request containing Block1 option
        indicating block number 0 and block size

        Step 3 (check (CON)) Client sends further requests containing
        Block1 option indicating block number and size

        Step 4 (verify (IOP)) Server indicates presence of the complete new resource
        """
        pass

if __name__ == '__main__':
    unittest.main()
