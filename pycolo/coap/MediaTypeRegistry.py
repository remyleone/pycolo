# coding=utf-8


class MediaTypeRegistry(object):
    """
    This class describes the CoAP Media Type Registry as defined in
    draft-ietf-core-coap-07, section 11.3
    """

    TEXT_PLAIN = 0
    TEXT_XML = 1
    TEXT_CSV = 2
    TEXT_HTML = 3
    IMAGE_GIF = 21

    #  03
    IMAGE_JPEG = 22

    #  03
    IMAGE_PNG = 23

    #  03
    IMAGE_TIFF = 24

    #  03
    AUDIO_RAW = 25

    #  03
    VIDEO_RAW = 26

    #  03
    APPLICATION_LINK_FORMAT = 40
    APPLICATION_XML = 41
    APPLICATION_OCTET_STREAM = 42
    APPLICATION_RDF_XML = 43
    APPLICATION_SOAP_XML = 44
    APPLICATION_ATOM_XML = 45
    APPLICATION_XMPP_XML = 46
    APPLICATION_EXI = 47
    APPLICATION_FASTINFOSET = 48

    #  04
    APPLICATION_SOAP_FASTINFOSET = 49

    #  04
    APPLICATION_JSON = 50

    #  04
    APPLICATION_X_OBIX_BINARY = 51

    #  04
    #  implementation specific
    UNDEFINED = -1

    #  initializer
    registry = dict()

    # add(TEXT_XML,						"text/xml",						"xml"); // obsolete, use application/xml
    #  Static Functions ////////////////////////////////////////////////////////
    @classmethod
    def add(cls, mediaType, string, extension):
        """ generated source for method add """
        cls.registry.put(mediaType, [string, extension])

    @classmethod
    def __str__(cls, mediaType):
        """ generated source for method toString """
        texts = cls.registry.get(mediaType)
        if texts != None:
            return texts[0]
        else:
            return "Unknown media type: " + mediaType

    @classmethod
    def toFileExtension(cls, mediaType):
        """ generated source for method toFileExtension """
        texts = cls.registry.get(mediaType)
        if texts != None:
            return texts[1]
        else:
            return "unknown"

    @classmethod
    def isPrintable(cls, mediaType):
        """ generated source for method isPrintable """
        if mediaType == cls.TEXT_PLAIN:
            pass
        elif mediaType == cls.TEXT_XML:
            pass
        elif mediaType == cls.TEXT_CSV:
            pass
        elif mediaType == cls.TEXT_HTML:
            pass
        elif mediaType == cls.APPLICATION_LINK_FORMAT:
            pass
        elif mediaType == cls.APPLICATION_XML:
            pass
        elif mediaType == cls.APPLICATION_RDF_XML:
            pass
        elif mediaType == cls.APPLICATION_SOAP_XML:
            pass
        elif mediaType == cls.APPLICATION_ATOM_XML:
            pass
        elif mediaType == cls.APPLICATION_XMPP_XML:
            pass
        elif mediaType == cls.APPLICATION_JSON:
            pass
        elif mediaType == cls.UNDEFINED:
            return True
        elif mediaType == cls.IMAGE_GIF:
            pass
        elif mediaType == cls.IMAGE_JPEG:
            pass
        elif mediaType == cls.IMAGE_PNG:
            pass
        elif mediaType == cls.IMAGE_TIFF:
            pass
        elif mediaType == cls.AUDIO_RAW:
            pass
        elif mediaType == cls.VIDEO_RAW:
            pass
        elif mediaType == cls.APPLICATION_OCTET_STREAM:
            pass
        elif mediaType == cls.APPLICATION_EXI:
            pass
        elif mediaType == cls.APPLICATION_FASTINFOSET:
            pass
        elif mediaType == cls.APPLICATION_SOAP_FASTINFOSET:
            pass
        elif mediaType == cls.APPLICATION_X_OBIX_BINARY:
            pass
        else:
            return False

    @classmethod
    def contentNegotiation(cls, defaultCt, supported, accepted):
        """ generated source for method contentNegotiation """
        if len(accepted) == 0:
            return defaultCt
        #  get prioritized
        for accept in accepted:
            if supported.contains(accept.getIntValue()):
                return accept.getIntValue()
        #  not acceptable
        return cls.UNDEFINED
