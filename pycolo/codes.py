# -*- coding:utf-8 -*-

"""
Registry of all constant status code

:codes:
    describes the CoAP Code Registry

:mediaCodes:
    describes the CoAP Media Type Registry

:options:
    describes the CoAP Option Number Registry
"""

import math
from struct import pack, unpack
from pycolo import DEFAULT_PORT
from pycolo.structures import LookupDict

_msgType = {
    0: ("CON", "con", "confirmable",  "default"),
    1: ("NON", "non", "NonConfirmable"),
    2: ("ACK", "ack", "acknowledgment"),
    3: ("RST", "rst", "reset"),
}

_codes = {
    #  Constants
    0: ("EMPTY_MESSAGE", "empty"),

    #  CoAP method codes
    1: ("METHOD_GET", "get", "GET"),
    2: ("METHOD_POST", "post", "POST", "CLASS_SUCCESS", "ok"),
    3: ("METHOD_PUT", "put", "PUT"),
    4: ("METHOD_DELETE", "delete", "DELETE", "CLASS_CLIENT_ERROR", "client_error"),
    5: ("CLASS_SERVER_ERROR", "Server_Error"),

    #  class 2.xx
    65: ("RESP_CREATED", "2.01 Created", "created"),
    66: ("RESP_DELETED", "2.02 Deleted", "deleted"),
    67: ("RESP_VALID", "2.03 Valid", "valid"),
    68: ("RESP_CHANGED", "2.04 Changed", "changed"),
    69: ("RESP_CONTENT", "2.05 Content", "content"),

    #  class 4.xx
    128: ("RESP_BAD_REQUEST", "4.00 Bad Request"),
    129: ("RESP_UNAUTHORIZED", "4.01 Unauthorized"),
    130: ("RESP_BAD_OPTION", "4.02 Bad Option"),
    131: ("RESP_FORBIDDEN", "4.03 Forbidden"),
    132: ("RESP_NOT_FOUND", "4.04 Not Found"),
    133: ("RESP_METHOD_NOT_ALLOWED", "4.05 Method Not Allowed"),
    134: ("RESP_NOT_ACCEPTABLE", "4.06 Not Acceptable"),
    140: ("RESP_PRECONDITION_FAILED", "4.12 Precondition Failed"),
    141: ("RESP_REQUEST_ENTITY_TOO_LARGE", "4.13 Request Entity Too Large"),
    143: ("RESP_UNSUPPORTED_MEDIA_TYPE", "4.15 Unsupported Media Type"),

    #  class 5.xx
    160: ("RESP_INTERNAL_SERVER_ERROR", "5.00 Internal Server Error"),
    161: ("RESP_NOT_IMPLEMENTED", "5.01 Not Implemented"),
    162: ("RESP_BAD_GATEWAY", "5.02 Bad Gateway"),
    163: ("RESP_SERVICE_UNAVAILABLE", "5.03 Service Unavailable"),
    164: ("RESP_GATEWAY_TIMEOUT", "5.04 Gateway Timeout"),
    165: ("RESP_PROXYING_NOT_SUPPORTED", "5.05 Proxying Not Supported"),

    #  from draft-IETF-core-block
    136: ("RESP_REQUEST_ENTITY_INCOMPLETE", "incomplete"),
}

refCodes = _codes

_mediaCode = {
    0: ("TEXT_PLAIN", "plain", "txt", "text"),
    1: ("TEXT_XML", "xml"),
    2: ("TEXT_CSV", "csv"),
    3: ("TEXT_HTML", "html"),
    21: ("IMAGE_GIF", "gif"),
    22: ("IMAGE_JPEG", "jpeg", "jpg"),
    23: ("IMAGE_PNG", "png"),
    24: ("IMAGE_TIFF", "tiff"),
    25: ("AUDIO_RAW", "audio"),
    26: ("VIDEO_RAW", "video"),
    40: ("APPLICATION_LINK_FORMAT", "link"),
    41: ("APPLICATION_XML", "appXML"),
    42: ("APPLICATION_OCTET_STREAM", "stream"),
    43: ("APPLICATION_RDF_XML", "rdfXML"),
    44: ("APPLICATION_SOAP_XML", "soapXML"),
    45: ("APPLICATION_ATOM_XML", "atomXML"),
    46: ("APPLICATION_XMPP_XML", "xmppXML"),
    47: ("APPLICATION_EXI", "exi"),
    48: ("APPLICATION_FASTINFOSET", "fastInfoSet"),
    49: ("APPLICATION_SOAP_FASTINFOSET", "soapFastInfoSet"),
    50: ("APPLICATION_JSON", "json"),
    51: ("APPLICATION_X_OBIX_BINARY", "xObixBin"),
}

# Encoders

def string_once(min_size, max_size, default=None):
    return {
        "range": range(min_size, max_size),
        "repeat": False,
        "format": "str",
        "encoder": lambda x: b"" if x == default else x.encode("utf-8"),
        "decoder": lambda raw: raw.decode("utf-8")
    }

def string_many(min_size, max_size, default=None):
    return {
        "range": range(min_size, max_size),
        "repeat": True,
        "encoder": lambda x: b"" if x == default else x.encode("utf-8"),
        "decoder": lambda raw: raw.decode("utf-8")
    }

def opaque_256_many(min_size, max_size, default=None):
    return {
        "range": range(min_size, max_size),
        "repeat": True,
        "format": "opaque",
        "encoder": lambda x: b"" if x == default else pack("!H", x),
        "decoder": lambda  raw: raw
    }

def presence_once():
    return {
        "repeat": False,
        "format": None,
        "encoder": lambda x: b"",
        "decoder": lambda raw: True
    }

def uint_once(min_size, max_size, default=None):
    return {
        "range": range(min_size, max_size),
        "repeat": False,
        "encoder": lambda x: b"" if x == default else pack("!H", x),
        "decoder": lambda raw: unpack("!H", raw)
    }

def uint_many(min_size, max_size, default=None):
    return {
        "range": range(min_size, max_size),
        "repeat": True,
        "encoder": lambda x: b"" if x == default else pack("!H", x),
        "decoder": lambda raw: unpack("!H", raw)
    }

options = {
    1: opaque_256_many(0, 8).update(name="If-Match"),  # core-coap-12
    3: string_once(1, 255).update(name="Uri-Host"),  # core-coap-12
    4: opaque_256_many(1, 8).update(name="etag"),  # core-coap-12 !! once in rp
    5: presence_once().update(name="if_none_match"),  # core-coap-12
    6: uint_once(0, 3).update(name="observe"),  # core-observe-07
    7: uint_once(0, 2, DEFAULT_PORT).update(name="uri_port"),  # core-coap-12
    8: string_many(0, 255).update(name="location_path"), # core-coap-12
    11: string_many(0, 255).update(name="uri_path"),  # core-coap-12
    12: uint_once(0, 2).update(name="content_format"),  # core-coap-12
    14: uint_once(0, 4, 60).update(name="max_age"),  # core-coap-12
    15: string_many(0, 255).update(name="uri_query"),  # core-coap-12
    16: uint_many(0, 2).update(name="accept"), # core-coap-12
    20: string_many(0, 255).update(name="location_query"),  # core-coap-12
    23: uint_once(0, 3).update(name="block2"),  # core-block-10
    27: uint_once(0, 3).update(name="block1"),  # core-block-10
    28: uint_once(0, 4).update(name="size"),  # core-block-10
    35: string_many(1, 1034).update(name="proxy_uri")  # core-coap-12
}

opt_i = dict([v, k] for k, v in options.items())

def isRequest(code):
    """
    Checks whether a code indicates a request.

    :param code: code the code to check
    :return: True if the code indicates a request
    """
    return 1 <= code <= 31


def isValid(code):
    #return (code >= 0) && (code <= 31)) || ((code >= 64) && (code <= 191)
    """
    Checks whether a code indicates a valid.

    :param code: Code to test.
    :return: True if option number is valid, False otherwise.
    """
    return 0 <= code <= 255


def isResponse(code):
    """
    Checks whether a code indicates a response number.

    :param code: Code to test
    :return: True if option number is a valid response number, False otherwise.
    """
    return 64 <= code <= 191


def isElective(optionNumber):
    """
    Checks whether a code indicates an elective option number.

    :param optionNumber: Code to test
    :return: True if option number is a valid elective number, False otherwise.
    """
    return (optionNumber & 1) == 0


def responseClass(code):
    """
    Returns the response class of a code

    :param code: the code to check
    :return: The response class of the code
    """
    return (code >> 5) & 0x7


def _init(d, status):
    for (code, titles) in list(status.items()):
        for title in titles:
            setattr(d, title, code)
            if not title.startswith('\\'):
                setattr(d, title.upper(), code)

codes = LookupDict(name="status_code")
mediaCodes = LookupDict(name="media_code")
msgType = LookupDict(name="msgType")

_init(codes, _codes)
_init(mediaCodes, _mediaCode)
_init(msgType, _msgType)