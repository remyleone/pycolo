# -*- coding:utf-8 -*-
"""
Etsi testing package.
Resources available :

- /test
- /seg1/seg2/seg3
- /location1/location2/location3
- /location-query
- /query
- /separate
- /large
- /large-update
- /large-create
- /obs
- /.well-known/core
- /multi-format
- /link1
- /link2
- /link3
- /path
- /path/sub1
- /path/sub2
- /path/sub3
- /alternate

Notes:

- Resources used in TD_COAP_CORE tests should not exceed 64 bytes
- Large resources used in TD_COAP_BLOCK tests shall not exceed 2048 bytes
- TD_COAP_LINK tests may require usage of Block options with some implementations
"""
import datetime
from threading import Timer
import unittest
from pycolo import codes
from pycolo.codes import mediaCodes
from pycolo.endpoint import Endpoint
from pycolo.message import Response
from pycolo.resource import Resource

server = Endpoint("PlugTestServer", PLUGTEST_BLOCK_SIZE=64)

@server.add("/large",
    rt="BlockWiseTransferTester",
    methods=["GET"],
    title="This is a large resource (>1024 bytes) for testing block-wise transfer.")
def large():
    """
    This class implements a resource that returns a larger amount of
    data on GET requests in order to test blockwise transfers.

    Large resources used in TD_COAP_BLOCK tests shall not exceed 2048 bytes

    This resource implements a test of specification for the ETSI IoT CoAP
    Plugtests.

    TD_COAP_BLOCK_01
    TD_COAP_BLOCK_02
    TD_COAP_BLOCK_03
    TD_COAP_BLOCK_04
    """
    if request.method  = "GET":
        junk_data = 4 * 5 * 64 * "7"
        return Response(code=codes.content,
            payload=junk_data,
            contentType=mediaCodes.text)


@server.add("/large_create", rt="block",
    methods=["GET", "POST", "DELETE"],
    name="Large resource that can be created using POST method")
def large_create():
    """
    Large resource that can be created using POST method (>1024 bytes)
    Large resources used in TD_COAP_BLOCK tests shall not exceed 2048 bytes

    This resource implements a test of specification for the
    ETSI IoT CoAP Plugtests.

    TD_COAP_BLOCK_04
    """

    data = None
    dataCt = -1

    if request.method == "GET":
        response = Response()
    #        if not self.data:
    #            response = Response(codes.content)
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
        return response  # complete the request

    if request.method == "POST":

        if request.contentType == mediaCodes.undefined:
            return Reponse(codes.bad_request, "Content-Type not set")
            #  store payload
        self.storeData(request)
        #  create new response
        response = Response(codes.RESP_CREATED)
        #  inform client about the location of the new resource
        response.setLocationPath("/nirvana")
        #  complete the request
        request.respond(response)

    if request.method == "DELETE":
        # DELETE the data and act as resouce was deleted.

        self.data = None
        #  complete the request
        return Response(codes.deleted)

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


@server.add("/large-update",
    methods=["GET"],
    rt="block",
    name="Large resource that can be updated using PUT method")
def large_update():
    """
    Large resource that can be updated using PUT method (>1024 bytes)
    Large resources used in TD_COAP_BLOCK tests shall not exceed 2048 bytes

    This resource implements a test of specification for the ETSI IoT CoAP
    Plugtests, Paris, France, 24 - 25 March 2012.

    TD_COAP_BLOCK_03
    """
    data = None
    dataCt = mediaCodes.text

    if request.method == "GET":
        # GETs the content of this storage resource.
        # If the content-type of the request is set to application/link-format
        # or if the resource does not store any data, the contained sub-resources
        # are returned in link format.


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

    if request.method == "POST":
        if request.contentType == mediaCodes.undefined:
            return Reponse(code=codes.bad_request, "Content-Type not set")
        else:
            #  store payload
            self.storeData(request)
            return Response(code=codes.changed)

    def storeData(self, request):
        """
        Convenience function to store data contained in a
        PUT/POST-Request. Notifies observing endpoints about
        the change of its contents.
        """

        # set payload and content type

#        data = request.payload
#        dataCt = request.contentType
#        self.clearAttribute(LinkFormat.CONTENT_TYPE)
#        self.setContentTypeCode(dataCt)
#        # signal that resource state changed
#        self.changed()

@server.add("/observe",
    obs=True,
    title="Observable resource which changes every 5 seconds")
def observe(Resource):
    """
    Observable resource which changes every 5 seconds.

    This resource implements a test of specification for the ETSI IoT CoAP
    Plugtests.

    - TD_COAP_OBS_01
    - TD_COAP_OBS_02
    - TD_COAP_OBS_03
    - TD_COAP_OBS_04
    - TD_COAP_OBS_05
    - TD_COAP_OBS_06
    - TD_COAP_OBS_07
    - TD_COAP_OBS_08
    """
    #  The current time represented as string
    time = ""

    def __init__(self):
        Timer(5.0, self._update).start()  # Set timer task scheduling

    def _update(self):
        """ Defines a new timer task to return the current time """
        self.time = datetime.datetime.now().strftime("%H:%m:%S")
        self.changed()  # Call changed to notify subscribers

    def performGET(self, request):
        """

        :param request:
        """
        response = Response(codes.RESP_CONTENT)
        response.payload = self.time
        response.contentType = mediaCodes.text
        response.maxAge = 5
        request.respond(response)  # complete the request

@server.add("/test",
    methods=["GET", "POST", "PUT", "DELETE"],
    title="Default test resource")
def default():
    """
    This resource implements a Default test resource for the
    ETSI IoT CoAP Plugtests.

    - TD_COAP_CORE_01
    - TD_COAP_CORE_02
    - TD_COAP_CORE_03
    - TD_COAP_CORE_04
    - TD_COAP_CORE_05
    - TD_COAP_CORE_06
    - TD_COAP_CORE_07
    - TD_COAP_CORE_08
    - TD_COAP_CORE_10
    - TD_COAP_CORE_11
    - TD_COAP_CORE_14
    - TD_COAP_CORE_18
    - TD_COAP_CORE_21
    - TD_COAP_CORE_22
    - TD_COAP_CORE_23
    - TD_COAP_CORE_24
    - TD_COAP_CORE_27
    - TD_COAP_CORE_28
    - TD_COAP_CORE_29
    - TD_COAP_LINK_08
    - TD_COAP_LINK_10
    """
    if request.method == "GET:"

        response = Response(codes.content, contentType=mediaCodes.text)
        if request.token:
            response.token = request.token

        if len(request.payload) > 64:
            payload = request.payload[:62] + '»'
        else:
            response.payload = request.payload

        return response # complete the request

    if request.method == "POST":
        response = Response(codes.created)

        payload = {"type": request.type,
                   "code": request.code,
                   "Message ID": request.MID,
                   "Content Type": request.contentType,
                   "Size": request.payloadSize}

        if request.token:
            payload["Token String"] = request.getTokenString()

        if len(str(payload)) > 64:
            payload.delete(62, len(payload))
            payload += '>>'

        response.payload = str(payload)
        response.contentType = mediaCodes.text
        response.path = "/nirvana"
        return response  # complete the request

    if request.method == "PUT":
        response = Response(codes.changed)

        payload = str(request)

        if request.token:
            payload += "\nTo: "
            payload += request.token

        if len(payload) > 64:
            payload.delete(62, len(payload))
            payload += '>>'

        response.payload = str(payload)
        response.contentType = mediaCodes.text
        return response  # complete the request


    if request.method == "DELETE":
        response = Response(codes.deleted)

        payload = str(request)
        if request.token:
            payload += "Token: "
            payload += request.getTokenString()

        if len(payload) > 64:
            payload.delete(62, len(payload))
            payload += '>>'

        response.payload = payload
        response.contentType = mediaCodes.text
        return response  # complete the request

@server.add("/query", title="Resource accepting query parameters")
def query():
    """
    Resource accepting query parameters

    This resource implements a test of specification for the
    ETSI IoT CoAP Plugtests.

    TD_COAP_CORE_13
    """
    if request.method = "GET":
        response = Response(code=codes.content, contentType=mediaCodes.text)
        payload = {
            "messageID": request.messageID,
            "code": request.code,
            "options": request.args,
        }
        response.payload = str(payload)
        return response  # complete the request

@server.add("/separate",
    rt="SepararateResponseTester",
    methods = ["GET"],
    title="Resource which cannot be served immediately and which\
             cannot be acknowledged in a piggy-backed way")
def separate():
    """
    This implements a 'separate' resource for demonstration purposes.
    Defines a resource that returns a response in a separate CoAP Message
    """
    if request.method == "GET":
        # we know this stuff may take longer... promise the client that this
        # request will be acted upon by sending an Acknowledgement
        request.accept()
        datetime.time.sleep(1)  # do the time-consuming computation

        payload = {"type": request.type.ordinal(),
                   "type-string": request.msgType,
                   "code": request.code,
                   "message ID": request.messageID}

        # create response
        response = Response(
            contentType=mediaCodes.text,
            payload=str(payload),
            code=codes.content)

        return response  # complete the request

@server.add("/seg1/seg2/seg3", methods=["GET"])
def long_path():
    """
    Long path resource

    This resource implements a test Long Path resource for the ETSI IoT CoAP
    Plugtests.

    - TD_COAP_CORE_12
    """
    if request.method == "GET":
        return Response(code=codes.RESP_CONTENT,
                contentType=mediaCodes.text, payload=request.payload)