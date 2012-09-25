# coding=utf-8
import logging


class Properties(java, util, Properties):
    """
    This class implements Californium's property registry.

    It is used to manage CoAP- and Californium-specific constants in a central
    place. The properties are initialized in the init() section and can be
    overridden by a user-defined .properties file. If the file does not exist
    upon initialization, it will be created so that a valid configuration always
    exists.
    """

    serialVersionUID = -8883688751651970877L  # generated to eliminate warning

    #  The header for Californium property files.
    HEADER = "Californium CoAP Properties file"

    #  The name of the default properties file.
    DEFAULT_FILENAME = "Californium.properties"

    def init(self):
        """ generated source for method init """
        #  CoAP Protocol constants 
        #  default CoAP port as defined in draft-ietf-core-coap-05, section 7.1:
        #  MUST be supported by a server for resource discovery and
        #  SHOULD be supported for providing access to other resources.
        set("DEFAULT_PORT", 5683)
        #  CoAP URI scheme name as defined in draft-ietf-core-coap-05, section 11.4:
        set("URI_SCHEME_NAME", "coap")
        #  constants to calculate initial timeout for confirmable messages,
        #  used by the exponential backoff mechanism
        set("RESPONSE_TIMEOUT", 2000)
        #  [milliseconds]
        set("RESPONSE_RANDOM_FACTOR", 1.5)
        #  maximal number of retransmissions before the attempt
        #  to transmit a message is canceled
        set("MAX_RETRANSMIT", 4)
        #  Implementation-specific
        #  buffer size for incoming datagrams, in bytes
        #  TODO find best value
        set("RX_BUFFER_SIZE", 4 * 1024)
        #  [bytes]
        #  capacity for caches used for duplicate detection and retransmissions
        set("MESSAGE_CACHE_SIZE", 32)
        #  [messages]
        #  time limit for transactions to complete,
        #  used to avoid infinite waits for replies to non-confirmables
        #  and separate responses
        set("DEFAULT_OVERALL_TIMEOUT", 60000)
        #  [milliseconds]
        #  the default block size for block-wise transfers
        #  must be power of two between 16 and 1024
        set("DEFAULT_BLOCK_SIZE", 512)
        #  [bytes]
        #  the number of notifications until a CON notification will be used
        set("OBSERVING_REFRESH_INTERVAL", 10)

    #  default properties used by the library
    std = Properties(DEFAULT_FILENAME)

    #  Constructors ////////////////////////////////////////////////////////////
    def __init__(self, fileName):
        """ generated source for method __init__ """
        super(Properties, self).__init__()
        self.init()
        initUserDefined(fileName)

    @overloaded
    def set(self, key, value):
        """ generated source for method set """
        setProperty(key, value)

    @set.register(object, str, int)
    def set_0(self, key, value):
        """ generated source for method set_0 """
        setProperty(key, String.valueOf(value))

    @set.register(object, str, float)
    def set_1(self, key, value):
        """ generated source for method set_1 """
        setProperty(key, String.valueOf(value))

    def getStr(self, key):
        """ generated source for method getStr """
        value = getProperty(key)
        if value == None:
            self.LOG.severe("Undefined string property: {:s}".format(key))
        return value

    def getInt(self, key):
        """ generated source for method getInt """
        value = getProperty(key)
        if value != None:
            try:
                return Integer.parseInt(value)
            except NumberFormatException as e:
                self.LOG.severe("Invalid integer property: {:s}={:s}".format(key, value))
        else:
            self.LOG.severe("Undefined integer property: {:s}".format(key))
        return 0

    def getDbl(self, key):
        """ generated source for method getDbl """
        value = getProperty(key)
        if value != None:
            try:
                return Double.parseDouble(value)
            except NumberFormatException as e:
                self.LOG.severe("Invalid double property: {:s}={:s}".format(key, value))
        else:
            self.LOG.severe("Undefined double property: {:s}".format(key))
        return 0.0

    def load(self, fileName):
        """ generated source for method load """
        in_ = FileInputStream(fileName)
        self.load(in_)

    def store(self, fileName):
        """ generated source for method store """
        out = FileOutputStream(fileName)
        self.store(out, self.HEADER)

    def initUserDefined(self, fileName):
        """ generated source for method initUserDefined """
        try:
            self.load(fileName)
        except IOException as e:
            #  file does not exist:
            #  write default properties
            try:
                self.store(fileName)
            except IOException as e1:
                logging.warning("Failed to create configuration file: {:s}".format(e1.getMessage()))
