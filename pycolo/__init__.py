# -*- coding: utf-8 -*-

"""
CoAP Protocol constants

:DEFAULT_PORT:
    default CoAP port as defined in draft-ietf-core-coap-05, section
    7.1: MUST be supported by a server for resource discovery and SHOULD be
    supported for providing access to other resources.

:URI_SCHEME_NAME:
    CoAP URI scheme name as defined in draft-ietf-core-coap-05,
    section 11.4.

:MAX_RETRANSMIT:
    maximal number of retransmissions before the attempt to
    transmit a message is canceled

:OBSERVING_REFRESH_INTERVAL:
    the number of notifications until a CON notification will be used

:DEFAULT_BLOCK_SIZE:
    the default block size for block-wise transfers must be
    power of two between 16 and 1024 bytes.

:MESSAGE_CACHE_SIZE: capacity (in messages) for caches.
    Used for duplicate detection and retransmissions.

:RX_BUFFER_SIZE:
    buffer size for incoming datagrams, in bytes

:DEFAULT_OVERALL_TIMEOUT: time (in milliseconds)
    for transaction to complete.
    Used to avoid infinite waits for replies to non-confirmables and separate
    responses

:RESPONSE_TIMEOUT & RESPONSE_RANDOM_FACTOR:
    constants to calculate initial timeout for confirmable messages,
    used by the exponential backoff mechanism

:TODO: Find a better value for RX_BUFFER_SIZE
"""

__title__ = 'pycolo'
__author__ = 'Rémy Léone'
__version__ = '0.0.1'

MESSAGE_CACHE_SIZE = 32
DEFAULT_BLOCK_SIZE = 512
DEFAULT_PORT = 5683
URI_SCHEME_NAME = "coap"
MAX_RETRANSMIT = 4
OBSERVING_REFRESH_INTERVAL = 10
RESPONSE_TIMEOUT = 2000  # [milliseconds]
RESPONSE_RANDOM_FACTOR = 1.5
RX_BUFFER_SIZE = 4 * 1024
DEFAULT_OVERALL_TIMEOUT = 60000
