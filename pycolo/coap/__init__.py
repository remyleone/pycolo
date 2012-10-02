# coding=utf-8

# CoAP Protocol constants

# default CoAP port as defined in draft-ietf-core-coap-05, section 7.1:
# MUST be supported by a server for resource discovery and
# SHOULD be supported for providing access to other resources.

DEFAULT_PORT = 5683

# CoAP URI scheme name as defined in draft-ietf-core-coap-05, section 11.4:

URI_SCHEME_NAME = "coap"

# constants to calculate initial timeout for confirmable messages,
# used by the exponential backoff mechanism

RESPONSE_TIMEOUT = 2000  # [milliseconds]
RESPONSE_RANDOM_FACTOR = 1.5

# maximal number of retransmissions before the attempt
# to transmit a message is canceled

MAX_RETRANSMIT = 4

# Implementation-specific

# buffer size for incoming datagrams, in bytes
# TODO find best value

RX_BUFFER_SIZE = 4 * 1024  # [bytes]


# capacity for caches used for duplicate detection and retransmissions

MESSAGE_CACHE_SIZE = 32  # [messages]

# time limit for transactions to complete,
# used to avoid infinite waits for replies to non-confirmables
# and separate responses

DEFAULT_OVERALL_TIMEOUT = 60000  # [milliseconds]

# the default block size for block-wise transfers
# must be power of two between 16 and 1024

DEFAULT_BLOCK_SIZE = 512  # [bytes]

# the number of notifications until a CON notification will be used

OBSERVING_REFRESH_INTERVAL = 10

# Media Type Registry
# This dict describes the CoAP Media Type Registry as defined in
# draft-ietf-core-coap-07, section 11.3

mediaTypeRegistry = {
    "TEXT_PLAIN": 0,
    "TEXT_XML": 1,
    "TEXT_CSV": 2,
    "TEXT_HTML": 3,
    "IMAGE_GIF": 21,
    "IMAGE_JPEG": 22,
    "IMAGE_PNG": 23,
    "IMAGE_TIFF": 24,
    "AUDIO_RAW": 25,
    "VIDEO_RAW": 26,
    "APPLICATION_LINK_FORMAT": 40,
    "APPLICATION_XML": 41,
    "APPLICATION_OCTET_STREAM": 42,
    "APPLICATION_RDF_XML": 43,
    "APPLICATION_SOAP_XML": 44,
    "APPLICATION_ATOM_XML": 45,
    "APPLICATION_XMPP_XML": 46,
    "APPLICATION_EXI": 47,
    "APPLICATION_FASTINFOSET": 48,
    "APPLICATION_SOAP_FASTINFOSET": 49,
    "APPLICATION_JSON": 50,
    "APPLICATION_X_OBIX_BINARY": 51,
    "UNDEFINED": (-1)
}

# Printable Media Type Registry

printableMediaType = ["TEXT_PLAIN", "TEXT_XML", "TEXT_CSV", "TEXT_HTML",
"APPLICATION_LINK_FORMAT", "APPLICATION_XML", "APPLICATION_RDF_XML",
"APPLICATION_SOAP_XML", "APPLICATION_ATOM_XML", "APPLICATION_XMPP_XML",
"APPLICATION_JSON", "UNDEFINED", "IMAGE_GIF", "IMAGE_JPEG", "IMAGE_PNG",
"IMAGE_TIFF", "AUDIO_RAW", "VIDEO_RAW", "APPLICATION_OCTET_STREAM",
"APPLICATION_EXI", "APPLICATION_FASTINFOSET", "APPLICATION_SOAP_FASTINFOSET",
"APPLICATION_X_OBIX_BINARY"]
