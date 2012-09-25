# coding=utf-8

import logging

from pycolo.coap.OptionNumberRegistry import OptionNumberRegistry
from pycolo.coap import Request
from pycolo.coap import Response
from pycolo.layers import UpperLayer


class MatchingLayer(UpperLayer):
    """
    This class matches the request/response pairs using the token option. It
    must be below the {@link TransferLayer}, which requires set buddies for each
    message ({@link Response#getRequest()} and {@link Request#getResponse()}).
    """
    #  Members ////////////////////////////////////////////////////////////////
    pairs = dict()

    class RequestResponsePair(object):
        """ Entity class to keep state of transfers """
        key = str()
        request = Request()

    def __init__(self):
        """ generated source for method __init__ """
        super(MatchingLayer, self).__init__()

    #  I/O implementation /////////////////////////////////////////////////////
    def doSendMessage(self, msg):
        """ generated source for method doSendMessage """
        if isinstance(msg, (Request,)):
            self.addOpenRequest(msg)
        self.sendMessageOverLowerLayer(msg)

    def doReceiveMessage(self, msg):
        """ generated source for method doReceiveMessage """
        if isinstance(msg, (Response,)):
            #  check for missing token
            if self.pair == None and len(self.length):
                logging.info("Remote endpoint failed to echo token: {:s}".format(msg.key()))
                #  TODO try to recover from peerAddress
                #  let timeout handle the problem
                return
            if self.pair != None:
                #  attach request and response to each other
                self.response.setRequest(self.pair.request)
                self.pair.request.setResponse(self.response)
                logging.info("Matched open request: {:s}".format(self.response.sequenceKey()))
                #  TODO: ObservingManager.getInstance().isObserving(msg.exchangeKey());
                if msg.getFirstOption(OptionNumberRegistry.OBSERVE) == None:
                    self.removeOpenRequest(self.response.sequenceKey())
            else:
                logging.info("Dropping unexpected response: {:s}".format(self.response.sequenceKey()))
                return
        self.deliverMessage(msg)

    def addOpenRequest(self, request):
        """ generated source for method addOpenRequest """
        #  create new Transaction
        exchange = self.RequestResponsePair()
        exchange.key = request.sequenceKey()
        exchange.request = request
        logging.info("Storing open request: {:s}".format(exchange.key))
        #  associate token with Transaction
        self.pairs.put(exchange.key, exchange)
        return exchange

    def getOpenRequest(self, key):
        """ generated source for method getOpenRequest """
        return self.pairs.get(key)

    def removeOpenRequest(self, key):
        """ generated source for method removeOpenRequest """
        exchange = self.pairs.remove(key)
        logging.info("Cleared open request: {:s}".format(exchange.key))

    def getStats(self):
        """ generated source for method getStats """
        stats = str()
        stats.append("Open requests: ")
        stats.append(len(self.pairs))
        stats.append('\n')
        stats.append("Messages sent:     ")
        stats.append(self.numMessagesSent)
        stats.append('\n')
        stats.append("Messages received: ")
        stats.append(self.numMessagesReceived)
        return stats.__str__()
