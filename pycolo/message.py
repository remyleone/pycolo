# coding=utf-8
"""
test
"""
import logging
import math
from pycolo.codes import options, codes


class Message:
    """
    The Class Message provides the object representation of a CoAP message.
    Besides providing the corresponding setters and getters, the class is
    responsible for parsing and serializing the objects from/to byte arrays.
    """

    # number of bits used for the encoding of the CoAP version field
    VERSION_BITS = 2

    # number of bits used for the encoding of the message type field
    TYPE_BITS = 2

    # number of bits used for the encoding of the option count field
    OPTIONCOUNT_BITS = 4

    # number of bits used for the encoding of the request method/
    # response code field
    CODE_BITS = 8

    # number of bits used for the encoding of the transaction ID
    ID_BITS = 16

    # number of bits used for the encoding of the option delta
    OPTIONDELTA_BITS = 4

    # number of bits used for the encoding of the base option length field
    # if all bits in this field are set to one, the extended option length
    # field is additionally used to encode the option length
    OPTIONLENGTH_BASE_BITS = 4

    # number of bits used for the encoding of the extended option length field
    # this field is used when all bits in the base option length field
    # are set to one
    OPTIONLENGTH_EXTENDED_BITS = 8

    # The message's type which can have the following values:
    #
    # 0: Confirmable (CON)
    # 1: Non-Confirmable (NON)
    # 2: Acknowledgment (ACK)
    # 3: Reset (RST)

    msgType = {
        "CON" : 0,
        "NON" : 1,
        "ACK" : 2,
        "RST" : 3,
        "default" : 0
    }

    messageType = None

    # maximum option delta that can be encoded without using fencepost options
    MAX_OPTIONDELTA = (1 << OPTIONDELTA_BITS) - 1

    # maximum option length that can be encoded using
    # the base option length field only
    MAX_OPTIONLENGTH_BASE = (1 << OPTIONLENGTH_BASE_BITS) - 2

    # The receiver for this message.
    peerAddress = None


    # The message type (CON, NON, ACK, or RST).
    type = None

    # Message code :
    # 0: Empty
    # 1-31: Request
    # 64-191: Response
    code = 0

    # The message ID. Set according to request or handled by
    # {@link ch.ethz.inf.vs.californium.layers.TransactionLayer} when -1.
    # 16-bit message ID of this CoAP message.
    messageID = -1


    # URI
    uri = None

    # indicates if the message requires a token
    # this is required to handle implicit empty tokens (default value)
    requiresToken = True
    requiresBlockwise = False



    def __init__(self, address, msgType=msgType, code=code,  payload=None, timestamp=0, version=1):
        """
        Constructor for a new CoAP message
        @param uri the URI of the CoAP message
        @param type the type of the CoAP message
        @param payload the payload of the CoAP message
        @param code the code of the CoAP message (See class CodeRegistry)
        """
        raise NotImplementedError
#        self.URI = address
#        self.msgType = msgType
#        self.code = code
#        self.messageID = mid
#        self.token = None
#        self.payload = payload
#        self.retransmissioned = False
#        self.retransmissioned = 0
#        self.mid = mid
#
#        # A time stamp associated with the message.
#        self.timestamp = timestamp  # TODO: Attention aux initialisations.
#
#        # The list of header options set for the message.
#        self.options = dict()
#
#        # The CoAP version used. For now, this must be set to 1.
#        self.version = version



    def isConfirmable(self):
        return self.type == self.messageType["CON"]

    def isNonConfirmable(self):
        return self.type == self.messageType["NON"]

    def isAcknowledgement(self):
        return self.type == self.messageType["ACK"]

    def isReset(self):
        return self.type == self.messageType["RST"]

    def isReply(self):
        return self.isAcknowledgement() or self.isReset()

    def isEmptyACK(self):
        return self.isAcknowledgement() and self.code == codes.EMPTY_MESSAGE

    def hasOption(self, optionNumber):
        return optionNumber in self.options

    def newAccept(self):
        """
        Creates a new ACK message with peer address and MID matching to this message.
        @return A new ACK message
        """
        ack = Message(self.messageType.ACK, codes.EMPTY_MESSAGE)
        ack.peerAddress = self.peerAddress
        ack.MID = self.MID
        return ack

    def newReject(self):
        """
        Creates a new RST message with peer address and MID matching to this
        message.
        @return A new RST message
        """
        rst = Message(self.messageType.RST, codes.EMPTY_MESSAGE)
        rst.peerAddress = self.peerAddress
        rst.MID = self.MID
        return rst

    def newReply(self, ack):
        """
        This method creates a matching reply for requests. It is addressed to
        the peer and has the same message ID and token.
        @param ack set true to send ACK else RST
        @return A new {@link Message}
        TODO does not fit into Message class
        """
        raise NotImplementedError

#        # TODO use this for Request.respond() or vice versa
#
#        reply = Message()
#
#        # set message type
#        if type == self.messageType.CON:
#            reply.type = ack ? messageType.ACK : messageType.RST
#        else:
#            reply.type = self.messageType.NON
#
#        # echo the message ID
#        reply.messageID = self.messageID
#
#        # set the receiver URI of the reply to the sender of this message
#        reply.peerAddress = self.peerAddress
#
#        # echo token
#        reply.setOption(getFirstOption(options.TOKEN))
#        reply.requiresToken = requiresToken
#
#        # create an empty reply by default
#        reply.code = codes.EMPTY_MESSAGE
#
#        return reply

    def dump(self):
        """
        Encodes the message into its raw binary representation
        as specified in draft-ietf-core-coap-05, section 3.1
        @return A byte array containing the CoAP encoding of the message
        """
        raise NotImplementedError

#        optionCount = 0
#        lastOptionNumber = 0
#        for opt in self.options:
#
#            # do not encode options with default values
#            if opt.isDefaultValue():
#                continue
#
#            # calculate option delta
#            optionDelta = opt.optionNumber - lastOptionNumber
#
#            # ensure that option delta value can be encoded correctly
#            while optionDelta > self.MAX_OPTIONDELTA:
#
#                # option delta is too large to be encoded:
#                # add fencepost options in order to reduce the option delta
#
#                # get fencepost option that is next to the last option
#                fencepostNumber = options.nextFencepost(lastOptionNumber)
#
#                # calculate fencepost delta
#                fencepostDelta = fencepostNumber - lastOptionNumber
#
#                # correctness assertions
#                # assert fencepostDelta > 0: "Fencepost liveness";
#                #assert fencepostDelta <= MAX_OPTIONDELTA: "Fencepost safety";
#
#                if fencepostDelta <= 0:
#                    logging.warning("Fencepost liveness violated: delta = %d" % fencepostDelta)
#
#                if fencepostDelta > options.MAX_OPTIONDELTA:
#                    logging.warning("Fencepost safety violated: delta = %d" % fencepostDelta)
#
#                # write fencepost option delta
#                optWriter.write(fencepostDelta, options.OPTIONDELTA_BITS)
#
#                # fencepost have an empty value
#                optWriter.write(0, OPTIONLENGTH_BASE_BITS)
#                logging.debug("DEBUG: %d\n", fencepostDelta)
#
#                # increment option count
#                ++optionCount
#
#                # update last option number
#                lastOptionNumber = fencepostNumber
#
#                # update option delta
#                optionDelta -= fencepostDelta
#
#
#            # write option delta
#            optWriter.write(optionDelta, options.OPTIONDELTA_BITS)
#
#            # write option length
#            length = opt.getLength()
#            if length <= options.MAX_OPTIONLENGTH_BASE:
#                # use option length base field only to encode
#                # option lengths less or equal than MAX_OPTIONLENGTH_BASE
#
#                optWriter.write(length, options.OPTIONLENGTH_BASE_BITS)
#
#            else:
#                # use both option length base and extended field
#                # to encode option lengths greater than MAX_OPTIONLENGTH_BASE
#
#                baseLength = options.MAX_OPTIONLENGTH_BASE + 1
#                optWriter.write(baseLength, options.OPTIONLENGTH_BASE_BITS)
#
#                extLength = length - baseLength
#                optWriter.write(extLength, options.OPTIONLENGTH_EXTENDED_BITS)
#
#            # write option value
#            optWriter.writeBytes(opt.getRawValue())
#
#            # increment option count
#            optionCount += 1
#
#            # update last option number
#            lastOptionNumber = opt.optionNumber
#
#        # create datagram writer to encode message data
#        DatagramWriter writer = new DatagramWriter()
#
#        # write fixed-size CoAP header
#        writer.write(version, options.VERSION_BITS)
#            writer.write(type.ordinal(), options.TYPE_BITS)
#            writer.write(optionCount, options.OPTIONCOUNT_BITS)
#            writer.write(code, options.CODE_BITS)
#            writer.write(messageID, options.ID_BITS)
#
#
#            # write options
#        writer.writeBytes(optWriter.toByteArray())
#
#        # write payload
#        writer.writeBytes(payload)
#
#        # return encoded message
#        return writer.toByteArray()

    def load(byteArray):
        """
        Decodes the message from the its binary representation
        as specified in draft-ietf-core-coap-05, section 3.1

        @param byteArray A byte array containing the CoAP encoding of the
        message
        """
        raise NotImplementedError

#        #Read current version
#        version = datagram.read(codes.VERSION_BITS) # non-blocking
#
#        #Read current type
#        messageType type = getTypeByValue(datagram.read(options.TYPE_BITS))
#
#        #Read number of options
#        optionCount = datagram.read(codes.OPTIONCOUNT_BITS)
#
#        #Read code
#        code = datagram.read(CODE_BITS)
#        if not CodeRegistry.isValid(code):
#            logging.info("Received invalid message code: %d", code))
#            return None
#
#        # create new message with subtype according to code number
#        Message msg
#        try:
#            msg = codes.getMessageClass(code).newInstance()
#        except Exception, e:
#            logging.severe("Cannot instantiate Message class %d", code, e.getMessage())
#            return None
#
#        msg.version = version
#        msg.type = type
#        msg.code = code
#
#        #Read message ID
#        msg.messageID = datagram.read(ID_BITS)
#
#        #Current option nr initialization
#        currentOption = 0
#
#        #Loop over all options
#        for i in range(optionCount):
#
#            #Read option delta bits
#            optionDelta = datagram.read(codes.OPTIONDELTA_BITS)
#
#            currentOption += optionDelta
#            logging.debug("DEBUG MSG: %d\n" % optionDelta)
#            if OptionNumberRegistry.isFencepost(currentOption):
#
#                #Read number of options
#                datagram.read(codes.OPTIONLENGTH_BASE_BITS)
#
#            else:
#                #Read option length
#                length = datagram.read(codes.OPTIONLENGTH_BASE_BITS)
#
#                if length > codes.MAX_OPTIONLENGTH_BASE:
#                    #Read extended option length
#                    #length = datagram.read(OPTIONLENGTH_EXTENDED_BITS)
#                    #         - (MAX_OPTIONLENGTH_BASE + 1);
#
#                    length += datagram.read(codes.OPTIONLENGTH_EXTENDED_BITS)
#
#                #Read option
#                #Option opt = new Option (datagram.readBytes(length), currentOption);
#                Option opt = Option.fromNumber(currentOption)
#                opt.setValue(datagram.readBytes(length))
#
#                #Add option to message
#                msg.addOption(opt)
#
#        # Get payload
#        msg.payload = datagram.readBytesLeft()
#
#        # incoming message already have a token, including implicit empty token
#        msg.requiresToken = False
#
#        return msg

    def send(self):
        raise NotImplementedError
#        try:
#            Communicator.getInstance().sendMessage(self)
#        except IOException as e:
#            logging.severe("Could not respond to message: %s%s", key(), e.getMessage())

    def accept(self):
        """
        Accepts this message with an empty ACK. Use this method only at
        application level, as the ACK will be sent through the whole stack.
        Within the stack use {@link #newAccept()} and send it through the
        corresponding {@link UpperLayer#sendMessageOverLowerLayer(Message)}.
        """
        raise NotImplementedError
#        if self.isConfirmable():
#            Message ack = newAccept()
#            ack.send()


    def appendPayload(self, block):
        """
        Appends data to this message's payload.
        :param block: the byte array containing the data to append
        :return:
        """
        raise NotImplementedError

#        if block:
#            if self.payload:
#                oldPayload = self.payload
#                payload = new byte[oldPayload.length + block.length]
#                System.arraycopy(oldPayload, 0, payload, 0, oldPayload.length)
#                System.arraycopy(block, 0, payload, oldPayload.length, block.length)
#            else:
#                payload = block.clone()
#            # wake up threads waiting in readPayload()
#            self.notifyAll()
#            # call notification method
#            payloadAppended(block);


    def key(self):
        """
        Returns a string that is assumed to uniquely identify a message.
        @return A string identifying the message
        """
        raise NotImplementedError
        # return str.format("%s|%d|%s", peerAddress != null ? peerAddress.toString() : "local", messageID, typeString())

    def transactionKey(self):
        """
        Returns a string that is assumed to uniquely identify a transaction.
        A transaction matches two buddies that have the same message ID between
        one this and the peer endpoint.
        @return A string identifying the transaction
        """
        raise NotImplementedError
#        return str.format("%s|%d", peerAddress != None\
#                         ? peerAddress.toString()\
#                         : "local", messageID)

    def sequenceKey(self):
        """
        Returns a string that is assumed to uniquely identify a transfer. A
        transfer exceeds matching message IDs, as multiple transactions are
        involved, e.g., for separate responses or blockwise transfers.
        The transfer matching is done using the token (including the empty
        default token.
        @return A string identifying the transfer
        """
        raise NotImplementedError
#        return str.format("%s#%s", peerAddress != null\
#                             ? peerAddress.toString()\
#                             : "local", getTokenString())


    def requiresToken(self):
        raise NotImplementedError
        # return requiresToken and self.code != codes.EMPTY_MESSAGE

    def __str__(self):
        raise NotImplementedError
#        kind = "MESSAGE"
#        if (this instanceof Request):
#            kind = "REQUEST "
#        elif (this instanceof Response):
#            kind = "RESPONSE"
#
#        logging.info("==[ CoAP %s ]=================================", kind)
#
#        info = dict()
#        info["address"] = self.peerAddress
#        info["id"] = self.messageID
#        info["type"] = self.type
#        info["code"] = self.code
#        info["Options Size"] = self.options.size()
#        logging.info(str(info))
#        for opt in self.options:
#            logging.info("%s: %s (%d Bytes)", opt.name, str(opt), len(opt))
#
#        logging.info("Payload: %d Bytes", self.payloadSize)
#        if payload and isPrintable(self.contentType):
#              logging.info(getPayloadString())
#        logging.info("=======================================================")


class Response(Message):

    def __init__(self, contentType=None, status=codes.RESP_VALID):
        """
        Instantiates a new response.
        @param method the status code of the message
        """
        raise NotImplementedError
        # self.code = status


    def getRTT(self):
        """
        Returns the round trip time in milliseconds (nano precision).
        @return RTT in ms
        """
        raise NotImplementedError
#        if request:
#            return float((self.getTimestamp() - request.getTimestamp())) / 1000000
#        else:
#            return -1

    def isPiggyBacked(self):
        raise NotImplementedError
        # return self.isAcknowledgement() and self.code != codes.EMPTY_MESSAGE


class Option:
    """
    This class describes the functionality of the CoAP header options.
    """
    DEFAULT_MAX_AGE = 60
    optionNr = int()   # The option number defining the option type.

    def fromNumber(cls, nr):
        """
        This method creates a new Option object with dynamic type corresponding
        to its option number.
        @param nr the option number
        @return A new option whose type matches the given number
        """
        raise NotImplementedError
#        if nr == options.BLOCK1:
#            pass
#        elif nr == options.BLOCK2:
#            return BlockOption(nr)
#        else:
#            return Option(nr)

    def __str__(self):
        """
        Returns a human-readable string representation of the option's value
        @Return The option value represented as a string
        """
        raise NotImplementedError

    def encode(cls, num, szx, m):
        value = 0
        value |= (szx & 0x7)
        value |= (1 if m else 0) << 3
        value |= num << 4
        return value

    def setValue(self, num, szx, m):
        self.setIntValue(self.encode(num, szx, m))

    def getNUM(self):
        return self.getIntValue() >> 4

    def setNUM(self, num):
        self.setValue(num, self.getSZX(), self.getM())

    def getSZX(self):
        return self.getIntValue() & 0x7

    def setSZX(self, szx):
        self.setValue(self.getNUM(), szx, self.getM())

    def getSize(self):
        return self.decodeSZX(self.getIntValue() & 0x7)

    def setSize(self, size):
        self.setValue(self.getNUM(), self.encodeSZX(size), self.getM())

    def getM(self):
        return (self.getIntValue() >> 3 & 0x1) != 0

    def setM(self, m):
        self.setValue(self.getNUM(), self.getSZX(), m)

    def decodeSZX(cls, szx):
        """
        Decodes a 3-bit SZX value into a block size as specified by
        draft-IETF-core-block-03, section-2.1:
        0 --> 2^4 = 16 bytes
        ...
        6 --> 2^10 = 1024 bytes
        """
        return 1 << (szx + 4)

    def encodeSZX(cls, blockSize):
        """
        Encodes a block size into a 3-bit SZX value as specified by
        draft-ietf-core-block-03, section-2.1:
        16 bytes = 2^4 --> 0
        ...
        1024 bytes = 2^10 -> 6
        """
        return int((math.log(blockSize) / math.log(2))) - 4

    def validSZX(cls, szx):
        return 0 <= szx <= 6

    def __str__(self):
        # TODO: Ne pas oublier de parser les options pour les rendre compréhensibles.
        # les options reconnues auront leur titre standard et les inconnues seront recopiées tel quel.
        """
        Serializer
        :return:
        """
        s = dict()
        s["NUM"] = self.getNUM()
        s["SZX"] = self.SZX
        s["bytes"] = self.size
        s["Message ID"] = self.MID
        return str(s)
