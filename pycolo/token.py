# -*- coding:utf-8 -*-

"""
The TokenManager stores all tokens currently used in transfers. New
transfers can acquire unique tokens from the manager.
"""

import logging
import random

acquiredTokens = set()
currentToken = random.randint(1, 2 ** 16)
emptyToken = 0


def nextToken():
    """
    Returns the next message ID to use out of the consecutive 16 - bit range.

    :return: the current message ID
    """
    global currentToken
    currentToken = (currentToken + 1) % 16
    logging.info("Token value: %d" % currentToken)

    return currentToken


def acquireToken(preferEmptyToken=False):
    """
    Returns an unique token.

    :param preferEmptyToken: If set to true, the caller will receive the empty token if it is available.

    This is useful for reducing
    datagram sizes in transactions that are expected to complete
    in short time. On the other hand, empty tokens are not preferred
    in block - wise transfers, as the empty token is then not available
    for concurrent transactions.
    """
    global token
    if preferEmptyToken and emptyToken not in acquiredTokens:
        token = emptyToken
    else:
        while token in acquiredTokens:
            token = nextToken()
        acquiredTokens.add(token)

    return token


def releaseToken(token):
    """
    Releases an acquired token and makes it available for reuse.

    :param token: The token to release
    """
    if token in acquiredTokens:
        acquiredTokens.remove(token)
    else:
        logging.warning("Token to release is not acquired: %s", hex(token))


def isAcquired(token):
    """
    Checks if a token is acquired by this manager.

    :param token: The token to check
    :return: True iff the token is currently in use
    """
    return token in acquiredTokens
