# -*- coding:utf-8 -*-

from pycolo.coap import Request
from pycolo.coap import Message
from pycolo.coap import Response
from pycolo.coap import GETRequest
from pycolo.coap import POSTRequest
from pycolo.coap import PUTRequest
from pycolo.coap import DELETERequest


class CodeRegistry():
    #  Constants //////////////////////////////////////////////////////////////
    EMPTY_MESSAGE = 0

    #  CoAP method codes //////////////////////////////////////////////////////
    METHOD_GET = 1
    METHOD_POST = 2
    METHOD_PUT = 3
    METHOD_DELETE = 4

    #  CoAP response codes ////////////////////////////////////////////////////
    CLASS_SUCCESS = 2
    CLASS_CLIENT_ERROR = 4
    CLASS_SERVER_ERROR = 5

    #  class 2.xx
    RESP_CREATED = 65
    RESP_DELETED = 66
    RESP_VALID = 67
    RESP_CHANGED = 68
    RESP_CONTENT = 69

    #  class 4.xx
    RESP_BAD_REQUEST = 128
    RESP_UNAUTHORIZED = 129
    RESP_BAD_OPTION = 130
    RESP_FORBIDDEN = 131
    RESP_NOT_FOUND = 132
    RESP_METHOD_NOT_ALLOWED = 133
    RESP_NOT_ACCEPTABLE = 134
    RESP_PRECONDITION_FAILED = 140
    RESP_REQUEST_ENTITY_TOO_LARGE = 141
    RESP_UNSUPPORTED_MEDIA_TYPE = 143

    #  class 5.xx
    RESP_INTERNAL_SERVER_ERROR = 160
    RESP_NOT_IMPLEMENTED = 161
    RESP_BAD_GATEWAY = 162
    RESP_SERVICE_UNAVAILABLE = 163
    RESP_GATEWAY_TIMEOUT = 164
    RESP_PROXYING_NOT_SUPPORTED = 165

    #  from draft-IETF-core-block
    RESP_REQUEST_ENTITY_INCOMPLETE = 136

    #  Static methods /////////////////////////////////////////////////////////
    # 
    #      * Checks whether a code indicates a request.
    #      * 
    #      * @param code the code to check
    #      * @return True if the code indicates a request

    @classmethod
    def isRequest(cls, code_):
        return (code_ >= 1) and (code_ <= 31)

    @classmethod
    def isResponse(cls, code_):
        return (code_ >= 64) and (code_ <= 191)

    @classmethod
    def isValid(cls, code_):
        #return (code >= 0) && (code <= 31)) || ((code >= 64) && (code <= 191)
        return (code_ >= 0) and (code_ <= 255)
        #  allow unknown custom codes

    @classmethod
    def responseClass(cls, code_):
        """
        Returns the response class of a code
        @param code the code to check
        @return The response class of the code
        """
        return (code_ >> 5) & 0x7

    @classmethod
    def getMessageClass(cls, code_):
        """ generated source for method getMessageClass """
        if cls.isRequest(code_):
            if code_ == cls.METHOD_GET:
                return GETRequest.__class__
            elif code_ == cls.METHOD_POST:
                return POSTRequest.__class__
            elif code_ == cls.METHOD_PUT:
                return PUTRequest.__class__
            elif code_ == cls.METHOD_DELETE:
                return DELETERequest.__class__
            else:
                return Request.__class__
        elif cls.isResponse(code_) or code_ == cls.EMPTY_MESSAGE:
            return Response.__class__
        else:
            return Message.__class__

    @classmethod
    def __str__(cls, code_):
        if code_ == cls.EMPTY_MESSAGE:
            return "Empty Message"
        elif code_ == cls.METHOD_GET:
            return "GET"
        elif code_ == cls.METHOD_POST:
            return "POST"
        elif code_ == cls.METHOD_PUT:
            return "PUT"
        elif code_ == cls.METHOD_DELETE:
            return "DELETE"
        elif code_ == cls.RESP_CREATED:
            return "2.01 Created"
        elif code_ == cls.RESP_DELETED:
            return "2.02 Deleted"
        elif code_ == cls.RESP_VALID:
            return "2.03 Valid"
        elif code_ == cls.RESP_CHANGED:
            return "2.04 Changed"
        elif code_ == cls.RESP_CONTENT:
            return "2.05 Content"
        elif code_ == cls.RESP_BAD_REQUEST:
            return "4.00 Bad Request"
        elif code_ == cls.RESP_UNAUTHORIZED:
            return "4.01 Unauthorized"
        elif code_ == cls.RESP_BAD_OPTION:
            return "4.02 Bad Option"
        elif code_ == cls.RESP_FORBIDDEN:
            return "4.03 Forbidden"
        elif code_ == cls.RESP_NOT_FOUND:
            return "4.04 Not Found"
        elif code_ == cls.RESP_METHOD_NOT_ALLOWED:
            return "4.05 Method Not Allowed"
        elif code_ == cls.RESP_NOT_ACCEPTABLE:
            return "4.06 Not Acceptable"
        elif code_ == cls.RESP_REQUEST_ENTITY_INCOMPLETE:
            return "4.08 Request Entity Incomplete"
        elif code_ == cls.RESP_PRECONDITION_FAILED:
            return "4.12 Precondition Failed"
        elif code_ == cls.RESP_REQUEST_ENTITY_TOO_LARGE:
            return "4.13 Request Entity Too Large"
        elif code_ == cls.RESP_UNSUPPORTED_MEDIA_TYPE:
            return "4.15 Unsupported Media Type"
        elif code_ == cls.RESP_INTERNAL_SERVER_ERROR:
            return "5.00 Internal Server Error"
        elif code_ == cls.RESP_NOT_IMPLEMENTED:
            return "5.01 Not Implemented"
        elif code_ == cls.RESP_BAD_GATEWAY:
            return "5.02 Bad Gateway"
        elif code_ == cls.RESP_SERVICE_UNAVAILABLE:
            return "5.03 Service Unavailable"
        elif code_ == cls.RESP_GATEWAY_TIMEOUT:
            return "5.04 Gateway Timeout"
        elif code_ == cls.RESP_PROXYING_NOT_SUPPORTED:
            return "5.05 Proxying Not Supported"
        if cls.isValid(code_):
            if cls.isRequest(code_):
                return "Unknown Request [code {:d}]".format(code_)
            elif cls.isResponse(code_):
                return "Unknown Response [code {:d}]".format(code_)
            else:
                return "Reserved [code {:d}]".format(code_)
        else:
            return "Invalid Message [code {:d}]".format(code_)
