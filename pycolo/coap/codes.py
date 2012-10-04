# -*- coding:utf-8 -*-

from .structures import LookupDict

_codes = {
    #  Constants
    0 :("EMPTY_MESSAGE", "Empty Message"),

    #  CoAP method codes
    1 : ("METHOD_GET","get","GET"),
    2 : ("METHOD_POST", "post", "POST"),
    3 : ("METHOD_PUT", "put", "PUT"),
    4 : ("METHOD_DELETE", "delete", "DELETE"),

    #  CoAP response codes


#CLASS_SUCCESS = 2
#CLASS_CLIENT_ERROR = 4
#CLASS_SERVER_ERROR = 5

    #  class 2.xx
    65: ("RESP_CREATED", "2.01 Created", "created"),
    66: ("RESP_DELETED", "2.02 Deleted", "deleted"),
    67: ("RESP_VALID","2.03 Valid", "valid"),
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
    136: ("RESP_REQUEST_ENTITY_INCOMPLETE"),
}

_mediaCode = {
    0: ("TEXT_PLAIN", "plain", "txt"),
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

_options = {
    0: ("RESERVED", "Reserved (0)", "reserved"),
    1: ("CONTENT_TYPE", "content", "Content-Type"),
    2: ("MAX_AGE", "Max-Age"),
    3: ("PROXY_URI", "Proxy-Uri"),
    4: ("ETAG", "ETag"),
    5: ("URI_HOST", "Uri-Host"),
    6: ("LOCATION_PATH", "Location-Path"),
    7: ("URI_PORT", "Uri-Port"),
    8: ("LOCATION_QUERY", "Location-Query"),
    9: ("URI_PATH", "Uri-Path"),
    10: ("OBSERVE", "Observe", "observe"),

    #  draft-IETF-core-observe

    11: ("TOKEN", "Token", "token"),
    12: ("ACCEPT", "Accept", "accept"),
    13: ("IF_MATCH", "If-Match"),
    14: ("FENCEPOST_DIVISOR"),
    15: ("URI_QUERY", "Uri-Query"),
    17: ("BLOCK2", "Block2"),

    #  draft-IETF-core-block
    19: ("BLOCK1", "Block1"),
    21: ("IF_NONE_MATCH", "If-None-Match"),
    8: ("TOKEN_LEN")

}

def isCritical(cls, optionNumber):
    """ generated source for method isCritical """
    return (optionNumber & 1) == 1

def isFencepost(cls, optionNumber):
    """ generated source for method isFencepost """
    return optionNumber % cls.FENCEPOST_DIVISOR == 0


def nextFencepost(cls, optionNumber):
    """
    Returns the next fencepost option number following a given option
    number
    @param optionNumber The option number
    @return The smallest fencepost option number larger than the given
    option number
    """
    return (optionNumber / cls.FENCEPOST_DIVISOR + 1) * cls.FENCEPOST_DIVISOR


def isRequest(code):
    """
    Checks whether a code indicates a request.

    :param code: code the code to check
    :return: True if the code indicates a request
    """
    return 1 <= code <= 31

def isValid(cls, code_):
    #return (code >= 0) && (code <= 31)) || ((code >= 64) && (code <= 191)
    return 0 <= code_ <= 255

def isResponse(cls, code_):
    return 64 <= code_ <= 191

def isElective(cls, optionNumber):
    """ generated source for method isElective """
    return (optionNumber & 1) == 0


def responseClass(cls, code_):
    """
    Returns the response class of a code
    TODO: Check
    :param code: the code to check
    :return: The response class of the code
    """
    return (code_ >> 5) & 0x7


def _init(d):
    for (code, titles) in list(d.items()):
        for title in titles:
            setattr(codes, title, code)
            if not title.startswith('\\'):
                setattr(codes, title.upper(), code)

codes = LookupDict(name="status_code")
codes = _init(_codes)
mediaCodes = LookupDict(name="media_code")
mediaCodes = _init(_mediaCode)
options = LookupDict(name="options_code")
optionsCodes = _init(_options)