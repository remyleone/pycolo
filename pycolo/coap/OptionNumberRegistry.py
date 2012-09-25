# coding=utf-8


class OptionNumberRegistry():
    RESERVED_0 = 0
    CONTENT_TYPE = 1
    MAX_AGE = 2
    PROXY_URI = 3
    ETAG = 4
    URI_HOST = 5
    LOCATION_PATH = 6
    URI_PORT = 7
    LOCATION_QUERY = 8
    URI_PATH = 9
    OBSERVE = 10

    #  draft-IETF-core-observe
    TOKEN = 11
    ACCEPT = 12

    IF_MATCH = 13
    URI_QUERY = 15
    BLOCK2 = 17

    #  draft-IETF-core-block
    BLOCK1 = 19

    #  draft-IETF-core-block
    IF_NONE_MATCH = 21
    FENCEPOST_DIVISOR = 14
    TOKEN_LEN = 8

    #  Formats
    #  ///////////////////////////////////////////////////////////////////
    class optionFormats:
        """ generated source for enum optionFormats """
        INTEGER = 'INTEGER'
        STRING = 'STRING'
        OPAQUE = 'OPAQUE'
        UNKNOWN = 'UNKNOWN'
        ERROR = 'ERROR'

    @classmethod
    def isElective(cls, optionNumber):
        """ generated source for method isElective """
        return (optionNumber & 1) == 0

    @classmethod
    def isCritical(cls, optionNumber):
        """ generated source for method isCritical """
        return (optionNumber & 1) == 1

    @classmethod
    def isFencepost(cls, optionNumber):
        """ generated source for method isFencepost """
        return optionNumber % cls.FENCEPOST_DIVISOR == 0

    @classmethod
    def nextFencepost(cls, optionNumber):
        """
        Returns the next fencepost option number following a given option
        number
        @param optionNumber The option number
        @return The smallest fencepost option number larger than the given
        option number
        """
        return (optionNumber / cls.FENCEPOST_DIVISOR + 1) * cls.FENCEPOST_DIVISOR

    @classmethod
    def __str__(cls, optionNumber):
        """ generated source for method toString """
        if optionNumber == cls.RESERVED_0:
            return "Reserved (0)"
        elif optionNumber == cls.CONTENT_TYPE:
            return "Content-Type"
        elif optionNumber == cls.MAX_AGE:
            return "Max-Age"
        elif optionNumber == cls.PROXY_URI:
            return "Proxy-Uri"
        elif optionNumber == cls.ETAG:
            return "ETag"
        elif optionNumber == cls.URI_HOST:
            return "Uri-Host"
        elif optionNumber == cls.LOCATION_PATH:
            return "Location-Path"
        elif optionNumber == cls.URI_PORT:
            return "Uri-Port"
        elif optionNumber == cls.LOCATION_QUERY:
            return "Location-Query"
        elif optionNumber == cls.URI_PATH:
            return "Uri-Path"
        elif optionNumber == cls.OBSERVE:
            return "Observe"
        elif optionNumber == cls.TOKEN:
            return "Token"
        elif optionNumber == cls.ACCEPT:
            return "Accept"
        elif optionNumber == cls.IF_MATCH:
            return "If-Match"
        elif optionNumber == cls.URI_QUERY:
            return "Uri-Query"
        elif optionNumber == cls.BLOCK2:
            return "Block2"
        elif optionNumber == cls.BLOCK1:
            return "Block1"
        elif optionNumber == cls.IF_NONE_MATCH:
            return "If-None-Match"
        return "Unknown option [number {:d}]".format(optionNumber)

    @classmethod
    def getFormatByNr(cls, optionNumber):
        """
        Returns the option format based on the option number
        @param optionNumber The option number
        @return The option format corresponding to the option number
        """
        if optionNumber == cls.RESERVED_0:
            return cls.optionFormats.UNKNOWN
        elif optionNumber == cls.CONTENT_TYPE:
            return cls.optionFormats.INTEGER
        elif optionNumber == cls.PROXY_URI:
            return cls.optionFormats.STRING
        elif optionNumber == cls.ETAG:
            return cls.optionFormats.OPAQUE
        elif optionNumber == cls.URI_HOST:
            return cls.optionFormats.STRING
        elif optionNumber == cls.LOCATION_PATH:
            return cls.optionFormats.STRING
        elif optionNumber == cls.URI_PORT:
            return cls.optionFormats.INTEGER
        elif optionNumber == cls.LOCATION_QUERY:
            return cls.optionFormats.STRING
        elif optionNumber == cls.URI_PATH:
            return cls.optionFormats.STRING
        elif optionNumber == cls.TOKEN:
            return cls.optionFormats.OPAQUE
        elif optionNumber == cls.URI_QUERY:
            return cls.optionFormats.STRING
        else:
            return cls.optionFormats.ERROR
