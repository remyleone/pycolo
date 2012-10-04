# coding=utf-8

from pycolo import Resource
from pycolo.codes import codes
from pycolo import Response
from pycolo.codes import mediaCodes


class DefaultTest(Resource):
    """
    This resource implements a test of specification for the
    ETSI IoT CoAP Plugtests, Paris, France, 24 - 25 March 2012.
    """

    def __int__(self):

        self.title = "Default test resource"

    def performGET(request):

        # Check: Type, Code

        # create response
        response = Response(codes.RESP_CONTENT)

        payload =  "Type: %d (%s)\nCode: %d (%s)\nMID: %d" %\
                                     request.getType().ordinal(),\
                                     request.typeString(),\
                                     request.code,\
                                     request.MID

        if request.getToken().length > 0:
            payload.append("Token: ")
            payload.append(request.getTokenString())

        if len(payload) > 64:
            payload.delete(62, len(payload))
            payload.append('>>')


        # set payload
        response.payload = payload
        response.contentType = mediaCodes.text

        # complete the request
        request.respond(response)

    def performPOST(request):

        # Check: Type, Code, has Content-Type

        # create new response
        response = Response(codes.RESP_CREATED)

        payload = "Type: %d (%s)\nCode: %d (%s) MID: %d" %\
                                     request.type.ordinal(),\
                                     request.type,\
                                     request.code,\
                                     request.MID

        payload.join("\nCT: %d\nPL: %d" % request.getContentType(), request.payloadSize())

        if request.getToken():
            payload.append("\nTo: ")
            payload.append(request.getTokenString())

        if len(payload) > 64:
            payload.delete(62, payload.length())
            payload.append('>>')

        response.payload = str(payload)
        response.contentType = mediaCodes.TEXT_PLAIN

        response.setLocationPath("/nirvana")

        # complete the request
        request.respond(response)

    def performPUT(request):

        # Check: Type, Code, has Content-Type

        # create new response
        response = Response(codes.RESP_CHANGED)

        payload = "Type: %d (%s)\nCode: %d (%s)\nMID: %d" %\
                                     request.getType().ordinal(),\
                                     request.typeString(),\
                                     request.getCode(),\
                                     request.getMID()

        payload.append("\nCT: %d\nPL: %d" % request.getContentType(), request.payloadSize())

        if request.getToken().length > 0:
            payload.append("\nTo: ")
            payload.append(request.getTokenString())

        if payload.length() > 64:
            payload.delete(62, payload.length())
            payload.append('>>')

        response.payload = str(payload)
        response.contentType = mediaCodes.text


        # complete the request
        request.respond(response)


    def performDELETE(request):

        # Check: Type, Code, has Content-Type

        # create new response
        response = Response(codes.RESP_DELETED);

        payload = "Type: %d (%s)\nCode: %d (%s)\nMID: %d" %\
                                     request.getType().ordinal(),\
                                     request.typeString(),\
                                     request.getCode(),\
                                     request.getMID()

        if request.getToken().length > 0:
            payload.append("\nToken: ")
            payload.append(request.getTokenString())

        if payload.length() > 64:
            payload.delete(62, payload.length())
            payload.append('>>')

        response.setPayload(payload.toString())
        response.setContentType(mediaCodes.TEXT_PLAIN)

        # complete the request
        request.respond(response)