# coding=utf-8
"""
test
"""
import logging
import math
from struct import unpack, pack, calcsize
from pycolo import PROTOCOL_VERSION as v
from pycolo.codes import options as refOptions, opt_i, msgType
from pycolo.codes import codes as refCodes
from pycolo.codes import msgType as refType
from pycolo.request import request


class Message:
    """
    The Class Message provides the object representation of a CoAP message.
    The class is responsible for parsing and serializing the objects from/to
    byte arrays.

    :param VERSION_BITS:
        number of bits used for the encoding of the CoAP version field
    :param TYPE_BITS:
        number of bits used for the encoding of the message type field
    :param OPTION_COUNT_BITS:
        number of bits used for the encoding of the option count field
    :param CODE_BITS:
        number of bits used for the encoding of the request method/response code field
    :param ID_BITS:
        number of bits used for the encoding of the transaction ID
    :param OPTION_DELTA_BITS:
        number of bits used for the encoding of the option delta
    :param OPTION_LENGTH_BASE_BITS:
        number of bits used for the encoding of the base option length field
        if all bits in this field are set to one, the extended option length
        field is additionally used to encode the option length
    :param OPTION_LENGTH_EXTENDED_BITS:
        number of bits used for the encoding of the extended option length field
        this field is used when all bits in the base option length field
        are set to one
    :param MAX_OPTION_DELTA:
        maximum option delta that can be encoded without using fencepost
        options
    :param MAX_OPTION_LENGTH_BASE:
        maximum option length that can be encoded using the base option
        length field only
    :param code: Message code
    """

    VERSION_BITS = 2
    TYPE_BITS = 2
    OPTION_COUNT_BITS = 4
    CODE_BITS = 8
    ID_BITS = 16
    OPTION_DELTA_BITS = 4
    OPTION_LENGTH_BASE_BITS = 4
    OPTION_LENGTH_EXTENDED_BITS = 8
    MAX_OPTION_DELTA = (1 << OPTION_DELTA_BITS) - 1
    MAX_OPTION_LENGTH_BASE = (1 << OPTION_LENGTH_BASE_BITS) - 2

    # The receiver for this message.
    peerAddress = None

    # URI
    uri = None

    # indicates if the message requires a token
    # this is required to handle implicit empty tokens (default value)
    requiresToken = True
    requiresBlockwise = False


    def __init__(self,
                 msg_type=refType.con,
                 status_code=refCodes.empty,
                 payload=None,
                 peerAddress=None,
                 timestamp=0,
                 message_id=None,
                 options={},
                 version=1):
        """
        Constructor for a new CoAP message
        :param uri: the URI of the CoAP message
        :param type: the type of the CoAP message
        :param payload: the payload of the CoAP message
        :param code: the code of the CoAP message (See class CodeRegistry)
        :param version: The CoAP version used. For now, this must be set to 1.
        :param options: The list of header options set for the message.
        """
        self.msg_type = msg_type
        self.version = version
        self.options = options
        self.status_code = status_code
        self.msg_type = msg_type
        self.message_id = message_id
        self.payload = payload
        self.peerAddress= peerAddress
#        self.retransmissioned = False
#        self.retransmissioned = 0

#        # A time stamp associated with the message.
#        self.timestamp = timestamp  # TODO: Attention aux initialisations.

    def is_reply(self):
        """

        :return:
        """
        return self.msg_type == refType.ack or self.isReset()

    def is_emptyACK(self):
        """

        :return:
        """
        return self.msg_type == refType.ack and self.status_code == refCodes.empty

    def new_accept(self):
        """
        Creates a new ACK message with peer address and MID matching to this message.

        :return: A new ACK message
        """
        return Message(
            peerAddress=self.peerAddress,
            msg_type=refType.ack,
            status_code=refCodes.empty,
            messageID=self.message_id)

    def new_reject(self):
        """
        Creates a new RST message with peer address and MID matching to this
        message.

        :return: A new RST message
        """
        return Message(
            msg_type=refType.rst,
            status_code=refCodes.empty,
            messageID=self.message_id,
            peerAddress=self.peerAddress)

    def new_reply(self, ack):
        """
        This method creates a matching reply for requests. It is addressed to
        the peer and has the same message ID and token.
        :param ack set true to send ACK else RST
        :param ack:
        """

        reply = Message(
            messageID=self.message_id,
            status_code=refCodes.empty,
            peerAddress=self.peerAddress
        )

        if self.msg_type == self.messageType.CON:
            reply.msg_type = self.message_type.ACK  if msgType.ack  else msgType.RST
        else:
            reply.msg_type = self.messageType.NON

        return reply


    def _encode_header(self):
        header_format = "!BBH"
        token_format = ""
        if hasattr(self, "token"):
            tkl, token = len(self.token), self.token
            token_format =  tkl * "B"
        else:
            tkl, token = 0, b""
        msg_type = self.msg_type if hasattr(self, "msg_type") else 0
        version_msgType_tkl = v << 6 & 192 | msg_type << 4 & 48 | tkl & 15
        header = [pack(header_format, version_msgType_tkl, self.status_code, self.message_id)]
        if token_format:
            header.append(pack("!" + token_format, token))
        return b"".join(header)

    def _encode_options(self):
        """
        This function is used to dump byte array representation of
        a options dictionary.

        :return: Encoded bytes array representing options
        """
        lastOptionNumber = 0
        list_encoded_options = []
        for option_number in sorted(self.options):
            delta = self.options[option_number]["num"] - lastOptionNumber
            list_encoded_options.append(
                self.options[option_number]["encoder"](delta, self.options[option_number]))
            lastOptionNumber = self.options[option_number]["num"]

        return b"".join(list_encoded_options)

    def _encode_payload(self):
        if hasattr(self, "payload"):
            if hasattr(self.payload, "encode"):
                return b"\xff" + self.payload.encode("utf-8")
            else:
                return b""
        else:
            return b""

    def to_raw(self):
        """
        Encodes the message into its raw binary representation
        as specified in draft from IETF

        :return A byte array containing the CoAP encoding of the message
        """
        return b"".join([self._encode_header(), self._encode_options(), self._encode_payload()])

    def from_raw(self, raw):
        """
        Decodes the message from the its binary representation

        :param byteArray: CoAP binary form message
        """
        PAYLOAD_MARKER = b"\xff"
        pointer, last_option = 0, 0

        # Header decoding

        ver_t_tkl_pattern = "!B"
        ver_t_tkl = unpack(ver_t_tkl_pattern, raw[pointer: pointer + calcsize(ver_t_tkl_pattern)])
        ver_t_tkl = ver_t_tkl[0]
        self.version = ver_t_tkl & 192 >> 6
        self.message_type = ver_t_tkl & 48 >> 4
        tkl = ver_t_tkl & 15
        pointer += calcsize(ver_t_tkl_pattern)

        code_pattern = "!B"
        code = unpack(code_pattern, raw[pointer: pointer + calcsize(code_pattern)])
        self.status_code = code[0]
        pointer += calcsize(code_pattern)

        message_id_pattern = "!H"
        message_id = unpack(message_id_pattern, raw[pointer: pointer + calcsize(message_id_pattern)])
        self.message_id = message_id[0]
        pointer += calcsize(message_id_pattern)

        # Token decoding
        if tkl:
            token_pattern = "!" + (tkl * "B")
            token = unpack(token_pattern, raw[pointer + calcsize(token_pattern)])
            self.token = token[0]
            pointer += calcsize(token_pattern)

        # Options decoding

        payload_marker_pattern = "!B"
        while raw[pointer: pointer + calcsize(payload_marker_pattern)] != PAYLOAD_MARKER and len(raw[pointer:]):
            common_option_pattern = "!B"
            option_header = unpack(common_option_pattern, raw[pointer: pointer + calcsize(common_option_pattern)])
            raw_delta, raw_length = option_header & 240, option_header & 15
            pointer += calcsize(common_option_pattern)

            # Delta decoding

            if 0 <= raw_delta <= 12:
                option_num = raw_delta + last_option
                last_option = option_num
            elif raw_delta == 13:
                delta_pattern_1byte = "!B"
                option_num = unpack(delta_pattern_1byte, raw[pointer:pointer + calcsize(delta_pattern_1byte)])  - 13
                last_option = option_num
                pointer += calcsize(delta_pattern_1byte)
            elif raw_delta == 14:
                delta_pattern_2bytes = "!2B"
                option_num = unpack(delta_pattern_2bytes, raw[pointer:pointer + calcsize(delta_pattern_2bytes)]) - 269
                last_option = option_num
                pointer += calcsize(delta_pattern_2bytes)
            elif raw_delta == 15:
                logging.error("Message delta encoding : 15. Reserved for future use.")
                return None

            # Length decoding

            if 0 <= raw_length <= 12:
                length = raw_length
            elif raw_length == 13:
                length_pattern_1byte = "!B"
                length = unpack(length_pattern_1byte, raw[pointer:pointer + calcsize(length_pattern_1byte)]) - 13
                pointer += calcsize(length_pattern_1byte)
            elif raw_length == 14:
                length_pattern_2bytes = "!2B"
                length = unpack(length_pattern_2bytes, raw[pointer:pointer + calcsize(length_pattern_2bytes)]) - 269
                pointer += calcsize(length_pattern_2bytes)
            elif raw_length == 15:
                logging.error("Message Length encoding : 15. Reserved for future use.")
                return None

            if length not in opt_i[option_num]["range"]:
                logging.error("Option too big. Encoding error")
                return None

            if not opt_i[option_num]["repeat"]:
                self.options[opt_i[option_num]] = opt_i[option_num]["decoder"](raw[pointer:pointer + length])
            else:
                self.options.setdefault(opt_i[option_num], [])\
                .append(opt_i[option_num]["decoder"](raw[pointer:pointer + length]))

            pointer += length

        # Payload decoding

        if len(raw[pointer:]) and raw[pointer] == b"\xff"[0]:
            self.payload = raw[pointer + 1:].decode("utf-8")
        else:
            self.payload = None
        return self

    def send(self):
        """

        :raise:
        """
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


    def key(self):
        """
        Returns a string that is assumed to uniquely identify a message.

        :return: A string identifying the message
        """
        return "%s|%d|%s" % (
            self.peerAddress if self.peerAddress else "local",
            self.message_id,
            self.msg_type)

    def transactionKey(self):
        """
        Returns a string that is assumed to uniquely identify a transaction.
        A transaction matches two buddies that have the same message ID between
        one this and the peer endpoint.

        :return: A string identifying the transaction
        """
        return "%s|%d" % (
            self.peerAddress if self.peerAddress else "local",
            self.message_id
        )

    def sequenceKey(self):
        """
        Returns a string that is assumed to uniquely identify a transfer. A
        transfer exceeds matching message IDs, as multiple transactions are
        involved, e.g., for separate responses or blockwise transfers.
        The transfer matching is done using the token (including the empty
        default token.

        :return: A string identifying the transfer
        """
        return "%s#%s" % (
            self.peerAddress if self.peerAddress else "local",
            self.token)

    def __str__(self):

        header = "==[ CoAP Message ]================================="
        info = {
            "address": self.peerAddress,
            "message ID": self.message_id,
            "msg type": self.msg_type,
            "status code": self.status_code,
        }
        # options pprint.pformat(options) <= from pprint import pformat
        # Known options will be displayed with their common name attributes.
        #        for opt in self.options:
        #            logging.info("%s: %s (%d Bytes)", opt.name, str(opt), len(opt))
        #
        #        logging.info("Payload: %d Bytes", self.payloadSize)
        #        if payload and isPrintable(self.contentType):
        #              logging.info(getPayloadString())

        footer = "======================================================="

        return "".join([header, "\n", str(info), "\n", footer])
