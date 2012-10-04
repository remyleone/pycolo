# coding=utf-8

import logging


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

    messageType = None

    # maximum option delta that can be encoded without using fencepost options
    MAX_OPTIONDELTA = (1 << OPTIONDELTA_BITS) - 1

    # maximum option length that can be encoded using
    # the base option length field only
    MAX_OPTIONLENGTH_BASE = (1 << OPTIONLENGTH_BASE_BITS) - 2

    # The receiver for this message.
    peerAddress = None

    # The message's payload.
    payload = None

    # The CoAP version used. For now, this must be set to 1.
    version = 1

    # The message type (CON, NON, ACK, or RST).
    type = None

    # Message code :
    # 0: Empty
    # 1-31: Request
    # 64-191: Response
    code = 0

    # The message ID. Set according to request or handled by
    # {@link ch.ethz.inf.vs.californium.layers.TransactionLayer} when -1.
    messageID = -1

    # The list of header options set for the message.
    optionMap = dict()

    # A time stamp associated with the message.
    timestamp = None

    retransmissioned = 0

    # indicates if the message requires a token
    # this is required to handle implicit empty tokens (default value)
    requiresToken = True
    requiresBlockwise = False

    msgType = {
            "CON" : 0,
            "NON" : 1,
            "ACK" : 2,
            "RST" : 3,
            "default" : 0
            }

    def __init__(self, address, msgType, code, mid, payload):
        """
        Constructor for a new CoAP message
        @param uri the URI of the CoAP message
        @param type the type of the CoAP message
        @param payload the payload of the CoAP message
        @param code the code of the CoAP message (See class CodeRegistry)
        """
        self.URI = address
        self.msgType = msgType
        self.code = code
        self.messageID = mid
        self.payload = payload

    def dump(self):
        """
        Encodes the message into its raw binary representation
        as specified in draft-ietf-core-coap-05, section 3.1
        @return A byte array containing the CoAP encoding of the message
        """

        optionCount = 0
        lastOptionNumber = 0
        for opt in self.options:

            # do not encode options with default values
            if opt.isDefaultValue():
                continue

            # calculate option delta
            optionDelta = opt.optionNumber - lastOptionNumber

            # ensure that option delta value can be encoded correctly
            while optionDelta > self.MAX_OPTIONDELTA:

                # option delta is too large to be encoded:
                # add fencepost options in order to reduce the option delta

                # get fencepost option that is next to the last option
                int fencepostNumber = OptionNumberRegistry.nextFencepost(lastOptionNumber)

                # calculate fencepost delta
                fencepostDelta = fencepostNumber - lastOptionNumber

                # correctness assertions
                # assert fencepostDelta > 0: "Fencepost liveness";
                #assert fencepostDelta <= MAX_OPTIONDELTA: "Fencepost safety";

                if fencepostDelta <= 0:
                    logging.warning("Fencepost liveness violated: delta = %d" % fencepostDelta)

                if fencepostDelta > MAX_OPTIONDELTA:
                    logging.warning("Fencepost safety violated: delta = %d" % fencepostDelta)

                # write fencepost option delta
                optWriter.write(fencepostDelta, OPTIONDELTA_BITS)

                # fencepost have an empty value
                optWriter.write(0, OPTIONLENGTH_BASE_BITS)
                logging.debug("DEBUG: %d\n", fencepostDelta)

                # increment option count
                ++optionCount

                # update last option number
                lastOptionNumber = fencepostNumber

                # update option delta
                optionDelta -= fencepostDelta


            # write option delta
            optWriter.write(optionDelta, OPTIONDELTA_BITS)

            # write option length
            length = opt.getLength()
            if length <= MAX_OPTIONLENGTH_BASE:
                # use option length base field only to encode
                # option lengths less or equal than MAX_OPTIONLENGTH_BASE

                optWriter.write(length, OPTIONLENGTH_BASE_BITS)

            else:
                # use both option length base and extended field
                # to encode option lengths greater than MAX_OPTIONLENGTH_BASE

                int baseLength = MAX_OPTIONLENGTH_BASE + 1;
                optWriter.write(baseLength, OPTIONLENGTH_BASE_BITS);

                int extLength = length - baseLength;
                optWriter.write(extLength, OPTIONLENGTH_EXTENDED_BITS);

            }

            # write option value
            optWriter.writeBytes(opt.getRawValue());

            # increment option count
            ++optionCount;

            # update last option number
            lastOptionNumber = opt.optionNumber
        }

        # create datagram writer to encode message data
        DatagramWriter writer = new DatagramWriter()

        # write fixed-size CoAP header
        writer.write(version, VERSION_BITS);
        writer.write(type.ordinal(), TYPE_BITS);
        writer.write(optionCount, OPTIONCOUNT_BITS);
        writer.write(code, CODE_BITS);
        writer.write(messageID, ID_BITS);


        # write options
        writer.writeBytes(optWriter.toByteArray())

        # write payload
        writer.writeBytes(payload)

        # return encoded message
        return writer.toByteArray()

    def load(byteArray):
        """
        Decodes the message from the its binary representation
        as specified in draft-ietf-core-coap-05, section 3.1

        @param byteArray A byte array containing the CoAP encoding of the
        message
        """
        #Initialize DatagramReader
        DatagramReader datagram = new DatagramReader(byteArray);

        #Read current version
        int version = datagram.read(VERSION_BITS); # non-blocking

        #Read current type
        messageType type = getTypeByValue(datagram.read(TYPE_BITS));

        #Read number of options
        int optionCount = datagram.read(OPTIONCOUNT_BITS);

        #Read code
        int code = datagram.read(CODE_BITS);
        if not CodeRegistry.isValid(code):
            logging.info("Received invalid message code: %d", code))
            return None

        # create new message with subtype according to code number
        Message msg;
        try:
            msg = CodeRegistry.getMessageClass(code).newInstance();
        catch (e):
            logging.severe("Cannot instantiate Message class %d", code,                       e.getMessage()))
            return None

        msg.version = version;
        msg.type = type;
        msg.code = code;

        #Read message ID
        msg.messageID = datagram.read(ID_BITS);

        #Current option nr initialization
        int currentOption = 0;

        #Loop over all options
        for i in range(optionCount):

            #Read option delta bits
            int optionDelta = datagram.read(OPTIONDELTA_BITS);

            currentOption += optionDelta;
            logging.debug("DEBUG MSG: %d\n" % optionDelta)
            if OptionNumberRegistry.isFencepost(currentOption):

                #Read number of options
                datagram.read(OPTIONLENGTH_BASE_BITS);

            else:
                #Read option length
                int length = datagram.read(OPTIONLENGTH_BASE_BITS)

                if (length > MAX_OPTIONLENGTH_BASE):
                    #Read extended option length
                    #length = datagram.read(OPTIONLENGTH_EXTENDED_BITS)
                    #         - (MAX_OPTIONLENGTH_BASE + 1);

                    length += datagram.read(OPTIONLENGTH_EXTENDED_BITS);

                #Read option
                #Option opt = new Option (datagram.readBytes(length), currentOption);
                Option opt = Option.fromNumber(currentOption);
                opt.setValue(datagram.readBytes(length));

                #Add option to message
                msg.addOption(opt)

        # Get payload
        msg.payload = datagram.readBytesLeft()

        # incoming message already have a token, including implicit empty token
        msg.requiresToken = false

        return msg

    def send():
        try:
            Communicator.getInstance().sendMessage(this);
        catch (IOException e):
            logging.severe("Could not respond to message: %s%s", key(), e.getMessage()))

    def accept():
        """
        Accepts this message with an empty ACK. Use this method only at
        application level, as the ACK will be sent through the whole stack.
        Within the stack use {@link #newAccept()} and send it through the
        corresponding {@link UpperLayer#sendMessageOverLowerLayer(Message)}.
        """
        if self.isConfirmable():
            Message ack = newAccept()
            ack.send()

    def newAccept():
        """
        Creates a new ACK message with peer address and MID matching to this message.
        @return A new ACK message
        """
        Message ack = new Message(messageType.ACK, CodeRegistry.EMPTY_MESSAGE);

        ack.setPeerAddress( self.getPeerAddress() )
        ack.setMID( self.getMID() )
        return ack

    def reject():
        """
        Rejects this message with an empty RST. Use this method only at
        application level, as the RST will be sent through the whole stack.
        Within the stack use {@link #newAccept()} and send it through the
        corresponding {@link UpperLayer#sendMessageOverLowerLayer(Message)}.
        """
        Message rst = newReject()
        rst.send()

    def newReject():
        """
        Creates a new RST message with peer address and MID matching to this
        message.
        @return A new RST message
        """

        Message rst = new Message(messageType.RST, CodeRegistry.EMPTY_MESSAGE);

        rst.setPeerAddress( getPeerAddress() )
        rst.setMID( self.getMID() )
        return rst

    def newReply(ack):
        """
        This method creates a matching reply for requests. It is addressed to
        the peer and has the same message ID and token.
        @param ack set true to send ACK else RST
        @return A new {@link Message}
        TODO does not fit into Message class
        """

        # TODO use this for Request.respond() or vice versa

        reply = Message()

        # set message type
        if type == messageType.CON:
            reply.type = ack ? messageType.ACK : messageType.RST
        else:
            reply.type = messageType.NON

        # echo the message ID
        reply.messageID = self.messageID

        # set the receiver URI of the reply to the sender of this message
        reply.peerAddress = self.peerAddress

        # echo token
        reply.setOption(getFirstOption(OptionNumberRegistry.TOKEN))
        reply.requiresToken = requiresToken

        # create an empty reply by default
        reply.code = CodeRegistry.EMPTY_MESSAGE

        return reply

    def handleBy(MessageHandler handler):
        """
        This method is overridden by subclasses according to the Visitor
        Pattern
        @param handler the handler for this message
        """
        pass



    def getMID():
        """
        This function returns the 16-bit message ID of this CoAP message.
        @return the message ID
        """
        return this.messageID

    def setMID(mid):
        """
        This method sets the 16-bit message ID of this CoAP message.
        @param mid the MID to set to
        """
        this.messageID = mid

    def getPeerAddress():
        return this.peerAddress

    def setPeerAddress(a):
        this.peerAddress = a

    def setURI(uri):
        """
        This is a convenience method to set peer address and Uri-* options
        via URI string.
        @param uri the URI string defining the target resource
        """
        try {
            setURI(new URI(uri));
            return true;
        } catch (URISyntaxException e) {
            logging.warning(String.format("Failed to set URI: %s", e.getMessage()))
            return false;
        }
    }

    def setURI(URI uri):
        """
        This is a convenience method to set peer address and Uri options via
        URI object.
        @param uri the URI defining the target resource
        """

        if (this instanceof Request) {

            # TODO URI-Host option
            /*
            String host = uri.getHost();
            if (host != null !isAddress...) {
                setOption(new Option(host, OptionNumberRegistry.URI_HOST));
            }
            */

            # set URI-Path options
            String path = uri.getPath();
            if (path != null && path.length() > 1) {
                List<Option> uriPath = Option.split(OptionNumberRegistry.URI_PATH, path, "/");
                setOptions(uriPath);
            }

            # set URI-Query options
            String query = uri.getQuery();
            if (query != null) {
                List<Option> uriQuery = Option.split(OptionNumberRegistry.URI_QUERY, query, "&");
                setOptions(uriQuery);
            }

        }
        this.setPeerAddress(new EndpointAddress(uri));
    }

    def getUriPath():
        return Option.join(getOptions(OptionNumberRegistry.URI_PATH), "/")

    def getQuery():
        return Option.join(getOptions(OptionNumberRegistry.URI_QUERY), "&")

    def getContentType():
        Option opt = getFirstOption(OptionNumberRegistry.CONTENT_TYPE)
        return opt != null ? opt.getIntValue() : MediaTypeRegistry.UNDEFINED

    def setContentType(ct):
        if (ct != MediaTypeRegistry.UNDEFINED):
            setOption(new Option(ct, OptionNumberRegistry.CONTENT_TYPE))
        else:
            removeOptions(OptionNumberRegistry.CONTENT_TYPE)

    def getFirstAccept():
        Option opt = getFirstOption(OptionNumberRegistry.ACCEPT)
        return opt != null ? opt.getIntValue() : MediaTypeRegistry.UNDEFINED

    def setAccept(ct):
        if (ct != MediaTypeRegistry.UNDEFINED):
            addOption(new Option(ct, OptionNumberRegistry.ACCEPT))
        else:
            removeOptions(OptionNumberRegistry.ACCEPT)

    def getToken():
        Option opt = getFirstOption(OptionNumberRegistry.TOKEN)
        return opt != null ? opt.getRawValue() : TokenManager.emptyToken

    def getTokenString():
        return Option.hex(getToken())

    def setToken(byte[] token):
        setOption(new Option(token, OptionNumberRegistry.TOKEN))

    def getMaxAge():
        Option opt = getFirstOption(OptionNumberRegistry.MAX_AGE)
        return opt != null ? opt.getIntValue() : Option.DEFAULT_MAX_AGE

    def setMaxAge(int timeInSec):
        setOption(new Option(timeInSec, OptionNumberRegistry.MAX_AGE))

    def getLocationPath():
        return Option.join(getOptions(OptionNumberRegistry.LOCATION_PATH), "/")

    def setLocationPath(locationPath):
        setOptions(Option.split(OptionNumberRegistry.LOCATION_PATH, locationPath, "/"))

    def getPayloadString():
        """
        This function returns the payload of this CoAP message as String.
        @return the payload
        """
        try:
            return payload != null ? new String(payload, "UTF-8") : null
        except Exception e:
            e.printStackTrace()
            return None
        }
    }

    def setPayload(byte[] payload):
        """
        This method sets a payload of this CoAP message replacing any existing
        one.
        @param payload the payload to set to
        """
        this.payload = payload

    /**
     * Appends data to this message's payload.
     * 
     * @param block the byte array containing the data to append
     */ 
    public synchronized void appendPayload(byte[] block) {

        if block:
            if payload:
                byte[] oldPayload = payload
                payload = new byte[oldPayload.length + block.length];
                System.arraycopy(oldPayload, 0, payload, 0,
                    oldPayload.length);
                System.arraycopy(block, 0, payload, oldPayload.length,
                    block.length);
            else:
                payload = block.clone()
            # wake up threads waiting in readPayload()
            notifyAll()
            # call notification method
            payloadAppended(block);

    def setPayload(String payload):
        self.setPayload(payload, MediaTypeRegistry.UNDEFINED)

    def setPayload(payload, mediaType):
        if payload:
            try:
                # set internal byte array
                self.setPayload(payload.getBytes("UTF-8"))
            except UnsupportedEncodingException e:
                e.printStackTrace()
                return

            # set content type option
            if mediaType != MediaTypeRegistry.UNDEFINED:
                setOption(new Option(mediaType, OptionNumberRegistry.CONTENT_TYPE))

    def payloadSize():
        return payload != null ? payload.length : 0

    def key():
        """
        Returns a string that is assumed to uniquely identify a message.
        @return A string identifying the message
        """
        return String.format("%s|%d|%s", peerAddress != null ? peerAddress.toString() : "local", messageID, typeString());

    def transactionKey():
        """
        Returns a string that is assumed to uniquely identify a transaction.
        A transaction matches two buddies that have the same message ID between
        one this and the peer endpoint.
        @return A string identifying the transaction
        """
        return str.format("%s|%d", peerAddress != null\
                         ? peerAddress.toString()\
                         : "local", messageID)

    def sequenceKey():
        """
        Returns a string that is assumed to uniquely identify a transfer. A
        transfer exceeds matching message IDs, as multiple transactions are
        involved, e.g., for separate responses or blockwise transfers.
        The transfer matching is done using the token (including the empty
        default token.
        @return A string identifying the transfer
        """
        return String.format("%s#%s", peerAddress != null\
                             ? peerAddress.toString()\
                             : "local", getTokenString())

    def messageType getType():
        """
        This function returns the type of this CoAP message
        (CON, NON, ACK, or RST).
        @return the current type
        """
        return this.type

    def addOption(option):
        """
        This method adds an option to the list of options of this CoAP message.
        @param option the option which should be added to the list of options
        of the current CoAP message
        """
        if not option:
            raise("Error")

        int optionNumber = option.optionNumber
        List < Option > list = optionMap.get(optionNumber);

        if (list == null) {
            list = new ArrayList < Option > ();
            optionMap.put(optionNumber, list);
        }

        list.add(option);

        if (optionNumber == OptionNumberRegistry.TOKEN) {
            requiresToken = false;
        }
    }

    def removeOptions(int optionNumber):
        """
        This method removes all options of the given number from this CoAP
        message
        @param optionNumber the number of the options to remove
        """
        optionMap.remove(optionNumber)

    def getOptions(optionNumber):
        """
        This function returns all options with the given option number.
        @param optionNumber the option number
        @return A list containing the options with the given number
        """
        List < Option > ret = optionMap.get(optionNumber);
        if ret:
            return ret;
        else:
            return list()

    def setOption(option):
        """
        Sets this option and overwrites all options with the same number
        @param option
        """
        # check important to allow convenient setting of options that might
        # be null (e.g., Token)
        if option:
            removeOptions(option.optionNumber)
            addOption(option)

    def setOptions(options):
        """
        Sets all given options and overwrites all options with the same numbers
        @param option the list of the options
        """
        for option in options:
            removeOptions(option.optionNumber)
        addOptions(options)

    def addOptions(options):
        """
        Adds all given options
        @param option the list of the options
        """
        for option in options:
            addOption(option)

    def getFirstOption(optionNumber):
        """
        A convenience method that returns the first option with the specified
        option number. Also used for options that MUST occur only once.
        @param optionNumber the option number
        @return The first option with the specified number, or null
        """
        List < Option > list = getOptions(optionNumber);
        return list != null && ! list.isEmpty() ? list.get(0) : null


    def getOptions():
        """
        Returns a sorted list of all included options.
        @return A sorted list of all options (copy)
        """
        for option in self.optionMap.values():
            list.append(option)
        return list

    def getOptionCount():
        """
        This function returns the number of options of this CoAP message.
        @return The current number of options
        """
        return getOptions().size()

    def getTimestamp():
        """
        Returns the timestamp associated with this message.
        @return The timestamp of the message, in milliseconds
        """
        return this.timestamp

    def setTimestamp(timestamp):
        """
        Sets the timestamp associated with this message.
        @param timestamp the new timestamp, in milliseconds
        """
        this.timestamp = timestamp

    def getRetransmissioned():
        return self.retransmissioned;

    def setRetransmissioned(retransmissioned):
        self.retransmissioned = retransmissioned

    def handleTimeout():
        """
        Notification method that is called when the transmission of this
        message was cancelled due to timeout.
        Subclasses may override this method to add custom handling code.
        """
        pass

    def payloadAppended(byte[] block):
        """
        Notification method that is called whenever payload was appended
        using the appendPayload() method.
        Subclasses may override this method to add custom handling code.
        @param block A byte array containing the data that was appended
        """
        pass

    def isConfirmable():
        return this.type == messageType.CON

    def isNonConfirmable():
        return this.type == messageType.NON

    def isAcknowledgement():
        return this.type == messageType.ACK

    def isReset():
        return self.type == messageType.RST

    def isReply():
        return self.isAcknowledgement() || isReset()

    def isEmptyACK():
        return isAcknowledgement() && getCode() == CodeRegistry.EMPTY_MESSAGE

    def hasOption(optionNumber):
        return getFirstOption(optionNumber) != null

    def requiresToken():
        return requiresToken && this.getCode() != CodeRegistry.EMPTY_MESSAGE;

    def requiresToken(value):
        requiresToken = value

    def requiresBlockwise(value):
        requiresBlockwise = value

    @Override
    def __str__(self):
        typeStr = "???"
        if type:
            switch (type) {
            case CON     : typeStr = "CON"; break;
            case NON : typeStr = "NON"; break;
            case ACK : typeStr = "ACK"; break;
            case RST           : typeStr = "RST"; break;
            default              : typeStr = "???"; break;
        }
        payloadStr = payload != null ? new String(payload) : null;
        return str.format("%s: [%s] %s '%s'(%d)",
            key(), typeStr, CodeRegistry.toString(code),
            payloadStr, payloadSize());


    def typeString():
        if type:
            switch (type) {
            case CON : return "CON";
            case NON : return "NON";
            case ACK : return "ACK";
            case RST : return "RST";
            default  : return "???";
        }
        return null

    def __str__():
        String kind = "MESSAGE ";
        if (this instanceof Request) {
            kind = "REQUEST ";
        } else if (this instanceof Response) {
            kind = "RESPONSE";
        }
        logging.info("==[ CoAP %s ]=================================\n", kind)

        options = self.options

        logging.info("Address: %s\n", peerAddress.toString());
        logging.info("MID    : %d\n", messageID);
        logging.info("Type   : %s\n", typeString());
        logging.info("Code   : %s\n", CodeRegistry.toString(code));
        logging.info("Options: %d\n", options.size());
        for opt in options:
            logging.info("  * %s: %s (%d Bytes)\n",
                opt.name, str(opt), len(opt)
            )

        logging.info("Payload: %d Bytes\n", payloadSize());
        if payloadSize() > 0 && MediaTypeRegistry.isPrintable(getContentType()):
             logging.info("--------------------------------------------------")
              logging.info(getPayloadString());
        logging.info("=======================================================")
    }
}
