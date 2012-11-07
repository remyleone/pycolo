# coding=utf-8
import logging
import random
from threading import Thread, Timer
from pycolo import DEFAULT_OVERALL_TIMEOUT
from pycolo.message import Message

class Layer:
    """
    An abstract Layer class that enforced a uniform interface for building
    a layered communications stack.
    """
    receivers = list()
    numMessagesSent = 0
    numMessagesReceived = 0

#    def __init__(self, name):
#        self.name = name

#    def __str__(self):
#        return self.name

    def sendMessage(self, msg):
        """
        :param msg:
        """
        if msg:
            self.doSendMessage(msg)
            self.numMessagesSent += 1

    def receiveMessage(self, msg):
        """
        :param msg:
        """
        if msg:
            self.numMessagesReceived += 1
            self.doReceiveMessage(msg)

    def doSendMessage(self, msg):
        """
        :param msg:
        """
        pass

    def doReceiveMessage(self, msg):
        """
        :param msg:
        """
        pass

    def deliverMessage(self, msg):
        """
        pass message to registered receivers
        :param msg:
        """
        raise NotImplementedError
#        if self.receivers:
#            for receiver in self.receivers:
#                receiver.receiveMessage(msg)

    def registerReceiver(self, receiver):
        """
        check for valid receiver
        :param receiver:
        """
        raise NotImplementedError
#        if receiver and receiver != self:
#            #  lazy creation of receiver list
#            if not self.receivers:
#                self.receivers = list()
#                #  add receiver to list
#            self.receivers.append(receiver)

    def unregisterReceiver(self, receiver):
        """
        remove receiver from list
        :param receiver:
        """
        raise NotImplementedError
#        if self.receivers:
#            self.receivers.remove(receiver)


class AdverseLayer(Layer):
    """
    This class describes the functionality of a layer that drops messages
    with a given probability in order to test retransmissions between
    MessageLayer and UDPLayer etc.
    """

    def __init__(self, txPacketLossProbability=0.0, rxPacketLossProbability=0.0):
        self.txPacketLossProbability = txPacketLossProbability
        self.rxPacketLossProbability = rxPacketLossProbability

    def doSendMessage(self, msg):
        """
        Send a message if the randomly picked number tell it so.
        :param msg:
        """
        raise NotImplementedError
#        if random.SystemRandom() >= self.txPacketLossProbability:
#            self.sendMessageOverLowerLayer(msg)
#        else:
#            logging.info("[%s] Outgoing message dropped: %s" % str(self), msg.key())

    def doReceiveMessage(self, msg):
        """
        Receive a message if the randomly picked number tell it so.
        :param msg:
        """
        raise NotImplementedError
#        if random.SystemRandom() >= self.rxPacketLossProbability:
#            self.deliverMessage(msg)
#        else:
#            logging.info("[%s] Incoming message dropped: %s", str(self), msg.key())

class MatchingLayer(Layer):
    """
    This class matches the request/response pairs using the token option. It
    must be below the TransferLayer, which requires set buddies for each
    message ({@link Response#getRequest()} and {@link Request#getResponse()}).
    """

    #pairs = dict()

    class RequestResponsePair:
        """ Entity class to keep state of transfers """
#        key = str()
#        request = request()

    def __init__(self):
        raise NotImplementedError
        # super(MatchingLayer, self).__init__()

    def doSendMessage(self, msg):
        raise NotImplementedError
#        if isinstance(msg, (request,)):
#            self.addOpenRequest(msg)
#        self.sendMessageOverLowerLayer(msg)

    def doReceiveMessage(self, msg):
        raise NotImplementedError
#        if isinstance(msg, (Response,)):
#            #  check for missing token
#            if not self.pair and len(self.length):
#                logging.info("Remote endpoint failed to echo token: {:s}".format(msg.key()))
#                #  TODO try to recover from peerAddress
#                #  let timeout handle the problem
#                return
#            if self.pair:
#                #  attach request and response to each other
#                self.response.setRequest(self.pair.request)
#                self.pair.request.setResponse(self.response)
#                logging.info("Matched open request: {:s}".format(self.response.sequenceKey()))
#                #  TODO: ObservingManager.getInstance().isObserving(msg.exchangeKey());
#                if msg.getFirstOption(OptionNumberRegistry.OBSERVE) is None:
#                    self.removeOpenRequest(self.response.sequenceKey())
#            else:
#                logging.info("Dropping unexpected response: {:s}".format(self.response.sequenceKey()))
#                return
#        self.deliverMessage(msg)

    def addOpenRequest(self, request):
        raise NotImplementedError
#        #  create new Transaction
#        exchange = self.RequestResponsePair()
#        exchange.key = request.sequenceKey()
#        exchange.request = request
#        logging.info("Storing open request: {:s}".format(exchange.key))
#        #  associate token with Transaction
#        self.pairs.put(exchange.key, exchange)
#        return exchange

    def getOpenRequest(self, key):
        raise NotImplementedError
#        return self.pairs.get(key)

    def removeOpenRequest(self, key):
        raise NotImplementedError
#        exchange = self.pairs.remove(key)
#        logging.info("Cleared open request: {:s}".format(exchange.key))

    def getStats(self):
        raise NotImplementedError
#        stats = dict()
#        stats["Open requests"] = self.pairs
#        stats["Messages sent"] = self.numMessagesSent
#        stats["Messages received"] = self.numMessagesReceived
#        return str(stats)



class UpperLayer(Layer):
    """ generated source for class UpperLayer """
    def sendMessageOverLowerLayer(self, msg):
#        """ generated source for method sendMessageOverLowerLayer """
#        #  check if lower layer assigned
#        if self.lowerLayer is not None:
#            self.lowerLayer.sendMessage(msg)
#        else:
#            logging.critical("[%s] ERROR: No lower layer present", self.getClass().__name__)
        raise NotImplementedError

    def setLowerLayer(self, layer):
        """ generated source for method setLowerLayer """
#        #  unsubscribe from old lower layer
#        if self.lowerLayer is not None:
#            self.lowerLayer.unregisterReceiver(self)
#            #  set new lower layer
#        lowerLayer = layer
#        #  subscribe to new lower layer
#        if lowerLayer is not None:
#            lowerLayer.registerReceiver(self)
        raise NotImplementedError

    def getLowerLayer(self):
        """ generated source for method getLowerLayer """
        #return self.lowerLayer
        raise NotImplementedError

    #lowerLayer = layers()

    class TransactionLayer(Layer):
        """
        The class TransactionLayer provides the functionality of the CoAP messaging
        layer as a subclass of {@link UpperLayer}. It introduces reliable transport
        of confirmable messages over underlying layers by making use of
        retransmissions and exponential backoff, matching of confirmables to their
        corresponding ACK / RST, detection and cancellation of duplicate messages,
        retransmission of ACK / RST messages upon receiving duplicate confirmable
        messages.
        """

    # The message ID used for newly generated messages.
    # currentMID = random.SystemRandom() * 0x10000

    def nextMessageID(self):
        """
        Returns the next message ID to use out of the consecutive 16 - bit
        range.
        @return the current message ID
        """
        raise NotImplementedError
#        self.currentMID += 1
#        self.currentMID %= 0x10000
#        return self.currentMID

    # The timer daemon to schedule retransmissions.
    # timer = Timer(true) # run as daemon

    # The Table to store the transactions of outgoing messages.
    # transactionTable = {}

    # The cache for duplicate detection.
    # dupCache = MessageCache()

    # Cache used to retransmit replies to incoming messages
    # replyCache = MessageCache()


    class Transaction:
        """
          Entity class to keep state of retransmissions.
          """
#        msg = Message()
#        retransmitTask = RestransmitTask()
#        numRetransmit = 0
#        timeout = 0 # to satisfy RESPONSE_RANDOM_FACTOR

    class MessageCache:
        """
        The MessageCache is a utility class used for duplicate detection and
        reply retransmissions. It is a ring buffer whose size is configured
        through the Californium properties file.
        """

        def removeEldestEntry(eldest):
            raise NotImplementedError
            # return size() > MESSAGE_CACHE_SIZE


#    class RetransmitTask(Timer):
#        """
#        Utility class to handle timeouts.
#        """

#        transaction = Transaction()
#
#        def RetransmitTask(transaction):
#            self.transaction = transaction
#
#        def run():
#            handleResponseTimeout(transaction)

    def initialTimeout(self):
        """
        Calculates the initial timeout for outgoing confirmable messages.
        :return: the timeout in milliseconds
        """
        raise NotImplementedError
#        min = RESPONSE_TIMEOUT
#        f = RESPONSE_RANDOM_FACTOR

        # return min + (min * (f - 1) * random.SystemRandom())


    def doSendMessage(msg):
        raise NotImplementedError
        # set message ID
#        if msg.getMID() < 0:
#            msg.setMID(self.nextMessageID())
#
#        # check if message needs confirmation, i.e., a reply is expected
#        if msg.isConfirmable():
#            # create new transmission context for retransmissions
#            self.addTransaction(msg)
#
#        elif msg.isReply():
#            # put message into ring buffer in case peer retransmits
#            self.replyCache.put(msg.transactionKey(), msg)
#
#        # send message over unreliable channel
#        self.sendMessageOverLowerLayer(msg)


    def doReceiveMessage(msg):
        raise NotImplementedError
#        # check for duplicate
#        if msg.key() in dupCache:
#            # check for retransmitted Confirmable
#            if msg.isConfirmable():
#                # retrieve cached reply
#                reply = replyCache.get(msg.transactionKey())
#                if reply:
#                    # retransmit reply
#                    try:
#                        logging.info("Replied to duplicate confirmable: %s" % msg.key())
#                        self.sendMessageOverLowerLayer(reply)
#                    except IOException
#                    e:
#                    logging.severe("Replying to duplicate confirmable failed: %s\n%s", msg.key(), e.getMessage())
#                else:
#                    logging.info("Dropped duplicate confirmable without cached reply: %s" % msg.key())
#
#                # drop duplicate anyway
#                return
#
#            else:
#                # ignore duplicate
#                logging.info(String.format("Dropped duplicate: %s", msg.key()))
#                return
#
#        else:
#        # cache received message
#            dupCache.put(msg.key(), msg)
#
#
#        # check for reply to CON and remove transaction
#        if msg.isReply():
#            # retrieve transaction for the incoming message
#            Transaction
#            transaction = getTransaction(msg)
#
#            if transaction:
#                # transmission completed
#                removeTransaction(transaction)
#
#                if msg.isEmptyACK():
#                    # transaction is complete, no information for higher layers
#                    return
#
#                else
#                if (msg.getType() == Message.messageType.RST):
#                    handleIncomingReset(msg)
#                    return
#
#            elif (msg.getType() == Message.messageType.RST):
#                handleIncomingReset(msg)
#                return
#
#            else:
#                # ignore unexpected reply except RST, which could match to a NON sent by the endpoint
#                logging.warning("Dropped unexpected reply: %s", msg.key())
#                return
#
#        # Only accept Responses here, Requests must be handled at application level
#        if (msg instanceof Response & & msg.isConfirmable()) {
#        try:
#            logging.info("Accepted confirmable response: %s" % msg.key())
#            sendMessageOverLowerLayer(msg.newAccept())
#        except IOException as e:
#            logging.severe("Accepting confirmable failed: %s\n%s" % msg.key(), e.getMessage())
#            # pass message to registered receivers
#            deliverMessage(msg)

    def handleIncomingReset(msg):
        # remove possible observers
        raise NotImplementedError
        # ObservingManager.getInstance().removeObserver(msg.getPeerAddress().toString(), msg.getMID())


    def handleResponseTimeout(transaction):
        raise NotImplementedError

#        max = MAX_RETRANSMIT
#
#        # check if limit of retransmissions reached
#        if transaction.numRetransmit < max:
#            # retransmit message
#            transaction.msg.setRetransmissioned(transaction.numRetransmit)
#
#            logging.info("Retransmitting %s (%d of %d)" % transaction.msg.key(), transaction.numRetransmit, max)
#
#            try:
#                sendMessageOverLowerLayer(transaction.msg)
#            except IOException, e:
#
#            logging.severe("Retransmission failed: %s", e.getMessage())
#            removeTransaction(transaction)
#
#            # schedule next retransmission
#            scheduleRetransmission(transaction)
#
#            return
#
#        else:
#            # cancel transmission
#            removeTransaction(transaction)
#
#            # cancel observations
#            ObservingManager.getInstance().removeObserver(transaction.msg.getPeerAddress().toString())
#
#            # invoke event handler method
#            transaction.msg.handleTimeout()

    def addTransaction(msg):
        raise NotImplementedError
        # initialize new transmission context
#        transaction = Transaction()
#        transaction.msg = msg
#        transaction.numRetransmit = 0
#        transaction.retransmitTask = None
#
#        transactionTable.put(msg.transactionKey(), transaction)
#
#        # schedule first retransmission
#        self.scheduleRetransmission(transaction)
#
#        logging.info("Stored new transaction for %s" % msg.key())
#
#        return transaction


    def getTransaction(msg):
        raise NotImplementedError
        # return transactionTable.get(msg.transactionKey())


    def removeTransaction(transaction):
        # cancel any pending retransmission schedule
        raise NotImplementedError
#        transaction.retransmitTask.cancel()
#        transaction.retransmitTask = None
#
#        # remove transaction from table
#        self.transactionTable.remove(transaction.msg.transactionKey())
#
#        logging.info("Cleared transaction for %s" % transaction.msg.key())


    def scheduleRetransmission(transaction):
        raise NotImplementedError
    #    # cancel existing schedule (if any)
    #    if transaction.retransmitTask:
    #        transaction.retransmitTask.cancel()
    #
    #    # create new retransmission task
    #    transaction.retransmitTask = RetransmitTask(transaction)
    #
    #    # calculate timeout using exponential back - off
    #
    #    if transaction.timeout == 0:
    #        # use initial timeout
    #        transaction.timeout = self.initialTimeout()
    #    else:
    #        # double timeout
    #        transaction.timeout *= 2
    #
    #    # schedule retransmission task
    #    timer.schedule(transaction.retransmitTask, transaction.timeout)


    def __str__(self):
        raise NotImplementedError
    #    stats = dict()
    #    stats["Current message ID"] = self.currentMID
    #    stats["Open transactions"] = self.transactionTable.size()
    #    stats["Messages sent"] = self.numMessagesSent
    #    stats["Messages received"] = self.numMessagesReceived
    #    return str(stats)

class TransferLayer(Layer):
    """
    The class TransferLayer provides support for
    <http://tools.ietf.org/html/draft-ietf-core-block">blockwise transfers

    {@link #doSendMessage(Message)} and {@link #doReceiveMessage(Message)} do
    not distinguish between clients and server directly, but rather between
    incoming and outgoing transfers. This saves duplicate code, but introduces
    rather confusing Request/Response checks at various places.
    TODO: Explore alternative designs.
    """
    class TransferContext:

        #cache = Message()
        #uriPath = ""
        # current = BlockOption()

        #  TODO: timer
        #def __init__(self, msg):
        #    raise NotImplementedError
#
#            if isinstance(msg, (request,)):
#                self.cache = msg
#                self.uriPath = msg.getUriPath()
#                self.current = msg.getFirstOption(options.BLOCK1)
#            elif isinstance(msg, (Response,)):
#                msg.requiresToken(False)
#                #  FIXME check if still required after new TokenLayer
#                self.cache = msg
#                self.uriPath = msg.getRequest().getUriPath()
#                self.current = msg.getFirstOption(options.BLOCK2)
#            logging.info("Created new transfer context for {:s}: {:s}".format(self.uriPath, msg.sequenceKey()))

        incoming = dict()
        outgoing = dict()
        defaultSZX = int()

    def __init__(self, defaultBlockSize):
        raise NotImplementedError
#        super(TransferLayer, self).__init__()
#        if defaultBlockSize == 0:
#            defaultBlockSize = Properties.std.getInt("DEFAULT_BLOCK_SIZE")
#        if defaultBlockSize > 0:
#            self.defaultSZX = BlockOption.encodeSZX(defaultBlockSize)
#            if not BlockOption.validSZX(self.defaultSZX):
#                self.defaultSZX = 6 if defaultBlockSize > 1024 else BlockOption.encodeSZX(defaultBlockSize & 0x07f0)
#                logging.warning("Unsupported block size {:d}, using {:d} instead".format(defaultBlockSize, BlockOption.decodeSZX(self.defaultSZX)))
#        else:
#            self.defaultSZX = -1


    def doSendMessage(self, msg):
        raise NotImplementedError
#        sendSZX = self.defaultSZX
#        sendNUM = 0
#        if isinstance(msg, (Response,)) and msg.getRequest() is not None:
#            if self.buddyBlock:
#                if self.buddyBlock.getSZX() < self.defaultSZX:
#                    sendSZX = self.buddyBlock.getSZX()
#                sendNUM = self.buddyBlock.getNUM()
#        if msg.payloadSize() > BlockOption.decodeSZX(sendSZX):
#            if self.msgBlock is not None:
#                if self.block1 is not None and self.block1.getM() or block2 is not None and self.block2.getM():
#                    msg.setOption(self.block1)
#                    msg.setOption(self.block2)
#                    self.outgoing.put(msg.sequenceKey(), self.transfer)
#                    logging.info("Caching blockwise transfer for NUM {:d}: {:s}".format(sendNUM, msg.sequenceKey()))
#                else:
#                    logging.info("Answering block request without caching: {:s} | {:s}".format(msg.sequenceKey(), block2))
#                self.sendMessageOverLowerLayer(self.msgBlock)
#            else:
#                logging.info("Rejecting initial out-of-scope request: {:s} | NUM: {:d}, SZX: {:d} ({:d} bytes), M: n/a, {:d} bytes available".format(msg.sequenceKey(), sendNUM, sendSZX, BlockOption.decodeSZX(sendSZX), msg.payloadSize()))
#                self.handleOutOfScopeError(msg.newReply(True))
#        else:
#            self.sendMessageOverLowerLayer(msg)

    def doReceiveMessage(self, msg):
        raise NotImplementedError
#        blockIn = None
#        blockOut = None
#        if isinstance(msg, (request,)):
#            blockIn = msg.getFirstOption(options.BLOCK1)
#            blockOut = msg.getFirstOption(options.BLOCK2)
#        elif isinstance(msg, (Response,)):
#            blockIn = msg.getFirstOption(options.BLOCK2)
#            blockOut = msg.getFirstOption(options.BLOCK1)
#            if blockOut is not None:
#                blockOut.setNUM(blockOut.getNUM() + 1)
#        else:
#            logging.warning("Unknown message type received: {:s}".format(msg.key()))
#            return
#        if blockIn is None and msg.requiresBlockwise():
#            blockIn = BlockOption(options.BLOCK1, 0, self.defaultSZX, True)
#            self.handleIncomingPayload(msg, blockIn)
#            return
#        elif blockIn is not None:
#            self.handleIncomingPayload(msg, blockIn)
#            return
#        elif blockOut is not None:
#            logging.info("Received demand for next block: {:s} | {:s}".format(msg.sequenceKey(), blockOut))
#            if self.transfer:
#                if isinstance(msg, (request,)) and not msg.getUriPath() == transfer.uriPath:
#                    self.outgoing.remove(msg.sequenceKey())
#                    logging.info("Freed blockwise transfer by client token reuse: {:s}".format(msg.sequenceKey()))
#                else:
#                    if isinstance(msg, (request,)):
#                        self.transfer.cache.setMID(msg.getMID())
#                    if next is not None:
#                        try:
#                            logging.info("Sending next block: {:s} | {:s}".format(next.sequenceKey(), blockOut))
#                            self.sendMessageOverLowerLayer(next)
#                        except IOException as e:
#                            logging.critical("Failed to send block response: {:s}".format(e.getMessage()))
#                        if not self.respBlock.getM() and isinstance(msg, (request,)):
#                            self.outgoing.remove(msg.sequenceKey())
#                            logging.info("Freed blockwise download by completion: {:s}".format(next.sequenceKey()))
#                        return
#                    elif isinstance(msg, (Response,)) and not blockOut.getM():
#                        self.outgoing.remove(msg.sequenceKey())
#                        logging.info("Freed blockwise upload by completion: {:s}".format(msg.sequenceKey()))
#                        msg.setRequest(self.transfer.cache)
#                    else:
#                        logging.warning("Rejecting out-of-scope demand for cached transfer (freed): {:s} | {:s}, {:d} bytes available".format(msg.sequenceKey(), blockOut, transfer.cache.payloadSize()))
#                        self.outgoing.remove(msg.sequenceKey())
#                        self.handleOutOfScopeError(msg.newReply(True))
#                        return
#        elif isinstance(msg, (Response,)):
#            if self.transfer:
#                msg.setRequest(self.transfer.cache)
#                self.outgoing.remove(msg.sequenceKey())
#                logging.info("Freed outgoing transfer by client abort: {:s}".format(msg.sequenceKey()))
#            transfer = self.incoming.get(msg.sequenceKey())
#            if transfer is not None:
#                msg.setRequest(transfer.cache)
#                self.incoming.remove(msg.sequenceKey())
#                logging.info("Freed incoming transfer by client abort: {:s}".format(msg.sequenceKey()))
#        self.deliverMessage(msg)
        raise NotImplementedError

    def handleIncomingPayload(self, msg, blockOpt):
        raise NotImplementedError
#        transfer = self.incoming.get(msg.sequenceKey())
#        if blockOpt.getNUM() > 0 and transfer is not None:
#            if blockOpt.getNUM() * blockOpt.getSize() == (transfer.current.getNUM() + 1) * transfer.current.getSize():
#                transfer.cache.appendPayload(msg.getPayload())
#                transfer.cache.setMID(msg.getMID())
#                logging.info("Received next block:  {:s} | {:s}".format(msg.sequenceKey(), blockOpt))
#            else:
#                logging.info("Dropping wrong block: {:s} | {:s}".format(msg.sequenceKey(), blockOpt))
#        elif blockOpt.getNUM() == 0 and msg.payloadSize() > 0:
#            if msg.payloadSize() > blockOpt.getSize():
#                blockOpt.setNUM(newNUM - 1)
#                msg.setPayload(Arrays.copyOf(msg.getPayload(), newNUM))
#            transfer = self.TransferContext(msg)
#            self.incoming.put(msg.sequenceKey(), transfer)
#            logging.info("Incoming blockwise transfer: {:s} | {:s}".format(msg.sequenceKey(), blockOpt))
#        else:
#            logging.info("Rejecting out-of-order block: {:s} | {:s}".format(msg.sequenceKey(), blockOpt))
#            self.handleIncompleteError(msg.newReply(True))
#            return
#        if blockOpt.getM():
#            if self.demandSZX > self.defaultSZX:
#                demandNUM = self.demandSZX / self.defaultSZX * self.demandNUM
#                demandSZX = self.defaultSZX
#            if isinstance(msg, (Response,)):
#                reply = request(codes.METHOD_GET, not msg.isNonConfirmable())
#                reply.setURI("coap://" + msg.getPeerAddress().__str__() + transfer.uriPath)
#                demandNUM += 1
#            elif isinstance(msg, (request,)):
#                reply = Response(codes.RESP_VALID)
#                reply.setType(self.messageType.ACK if msg.isConfirmable() else self.messageType.NON)
#                reply.setPeerAddress(msg.getPeerAddress())
#                if msg.isConfirmable():
#                    reply.setMID(msg.getMID())
#            else:
#                logging.critical("Unsupported message type: {:s}".format(msg.key()))
#                return
#            reply.setOption(msg.getFirstOption(options.TOKEN))
#            reply.setOption(next)
#            try:
#                logging.info("Demanding next block: {:s} | {:s}".format(reply.sequenceKey(), next))
#                sendMessageOverLowerLayer(reply)
#            except IOException as e:
#                logging.critical("Failed to request block: {:s}".format(e.getMessage()))
#            transfer.current = blockOpt
#        else:
#            transfer.cache.setOption(blockOpt)
#            logging.info("Finished blockwise transfer: {:s}".format(msg.sequenceKey()))
#            self.incoming.remove(msg.sequenceKey())
#            self.deliverMessage(transfer.cache)

    def handleOutOfScopeError(self, resp):
        raise NotImplementedError
#        """ generated source for method handleOutOfScopeError """
#        resp.setCode(codes.RESP_BAD_REQUEST)
#        resp.setPayload("BlockOutOfScope")
#        try:
#            sendMessageOverLowerLayer(resp)
#        except IOException as e:
#            logging.critical("Failed to send error message: {:s}".format(e.getMessage()))

    def handleIncompleteError(self, resp):
        raise NotImplementedError
#        """ generated source for method handleIncompleteError """
#        resp.setCode(codes.RESP_REQUEST_ENTITY_INCOMPLETE)
#        resp.setPayload("Start with block num 0")
#        try:
#            sendMessageOverLowerLayer(resp)
#        except IOException as e:
#            logging.critical("Failed to send error message: {:s}".format(e.getMessage()))

    def getBlock(cls, msg, num, szx):
        raise NotImplementedError
#        """ generated source for method getBlock """
#        blockSize = 1 << (szx + 4)
#        payloadOffset = num * blockSize
#        payloadLeft = msg.payloadSize() - payloadOffset
#        if payloadLeft > 0:
#            if isinstance(msg, (request,)):
#                block = request(msg.getCode(), msg.isConfirmable())
#            else:
#                block = Response(msg.getCode())
#                if num == 0 and msg.getType() == Message.messageType.CON:
#                    block.setType(Message.messageType.CON)
#                else:
#                    block.setType(Message.messageType.NON if msg.isNonConfirmable() else Message.messageType.ACK)
#                block.setMID(msg.getMID())
#            block.setPeerAddress(msg.getPeerAddress())
#            for opt in msg.getOptions():
#                block.addOption(opt)
#            if not m:
#                blockSize = payloadLeft
#            System.arraycopy(msg.getPayload(), payloadOffset, blockPayload, 0, blockSize)
#            block.setPayload(blockPayload)
#            if isinstance(msg, (request,)):
#                blockOpt = BlockOption(OptionNumberRegistry.BLOCK1, num, szx, m)
#            else:
#                blockOpt = BlockOption(OptionNumberRegistry.BLOCK2, num, szx, m)
#            block.setOption(blockOpt)
#            return block
#        else:
#            return None

    def getStats(self):
        raise NotImplementedError
#        stats = {"Default block size": BlockOption.decodeSZX(self.defaultSZX),
#                 "Outgoing cache size": len(self.outgoing), "Incoming cache size": len(self.incoming),
#                 "Messages sent": self.numMessagesSent, "Messages received": self.numMessagesReceived}
#        return str(stats)


class TokenLayer(UpperLayer):
    """
    This class takes care of unique tokens for each sequence of request/response
    exchanges.
    Additionally, the TokenLayer takes care of an overall timeout for each
    request/response exchange.
    """

    #exchanges = dict()

    # A timer for scheduling overall request timeouts.
    #timer = Timer(True)

    # The time to wait for requests to complete, in milliseconds.
    #sequenceTimeout = 0


    class RequestResponseSequence:
        """
        Entity class to keep state of transfers
        """

#    public String key public Request request
#    public
#    TimerTask
#    timeoutTask


class TimeoutTask:  # from TimerTask
#    """
#    Utility class to provide transaction timeouts
#    """

    def run(self, sequence):
        raise NotImplementedError
        #self.transferTimedOut(sequence)


    def __init__(self, sequence, sequenceTimeout=DEFAULT_OVERALL_TIMEOUT):
        raise NotImplementedError
        # member initialization
#        self.sequenceTimeout = sequenceTimeout
#        self.sequence = sequence


    def doSendMessage(msg):
        raise NotImplementedError
#        # set token option if required
#        if msg.requiresToken():
#            msg.setToken(TokenManager.getInstance().acquireToken(true))
#
#        # use overall timeout for clients (e.g., server crash after separate response ACK)
#        if msg is Request:
#            logging.info(String.format("Requesting response for %s: %s", ((Request)
#            msg).getUriPath(), msg.sequenceKey()));
#            addExchange((Request)
#            msg);
#            elif (msg.getCode() == codes.EMPTY_MESSAGE):
#            logging.info(String.format("Accepting request: %s", msg.key()))
#        else:
#            logging.info(String.format("Responding request: %s", msg.sequenceKey()))
#
#        self.sendMessageOverLowerLayer(msg)


    def doReceiveMessage(msg):
        raise NotImplementedError
#        if (msg
#        instanceof
#        Response) {
#
#            response = (Response)
#        msg
#
#        RequestResponseSequence
#        sequence = getExchange(msg.sequenceKey())
#
#        # check for missing token
#        if (not sequence and not response.getToken()):
#        logging.warning("Remote endpoint failed to echo token: %s" % msg.key())
#
#        # TODO try to recover from peerAddress
#
#
#        if sequence:
#            # cancel timeout
#            sequence.timeoutTask.cancel()
#
#            # TODO separate observe registry
#            if msg.getFirstOption(options.OBSERVE) == null:
#                removeExchange(msg.sequenceKey())
#
#            logging.info("Incoming response from %s: %s # RTT: %fms", ((Response)
#            msg).getRequest().getUriPath(), msg.sequenceKey(), ((Response)
#            msg).getRTT()));
#            deliverMessage(msg)
#
#        else:
#            logging.warning("Dropping unexpected response: %s", response.sequenceKey())
#
#        elif msg is Request:
#            logging.info("Incoming request: %s" % msg.sequenceKey())
#
#        self.deliverMessage(msg)

    def addExchange(request):
        raise NotImplementedError
        # be aware when manually setting tokens, as request/response will be replace
#        self.removeExchange(request.sequenceKey())
#
#        # create new Transaction
#        RequestResponseSequence
#        sequence = new
#        RequestResponseSequence()
#        sequence.key = request.sequenceKey()
#        sequence.request = request
#        sequence.timeoutTask = new
#        TimeoutTask(sequence)
#
#        # associate token with Transaction
#        exchanges.put(sequence.key, sequence)
#
#        timer.schedule(sequence.timeoutTask, sequenceTimeout)
#
#        logging.fine("Stored new exchange: %s" % sequence.key)
#
#        return sequence


    def getExchange(key):
        raise NotImplementedError
        # return exchanges.get(key)


    def removeExchange(key):
        raise NotImplementedError
#        exchange = exchanges.remove(key)
#
#        if exchange:
#            exchange.timeoutTask.cancel()
#            TokenManager.getInstance().releaseToken(exchange.request.getToken())
#            logging.finer(String.format("Cleared exchange: %s", exchange.key))


    def transferTimedOut(exchange):
        raise NotImplementedError
        # cancel transaction
#        self.removeExchange(exchange.key)
#
#        logging.warning("Request/Response exchange timed out: %s" % exchange.request.sequenceKey())
#
#        exchange.request.handleTimeout()  # call event handler


    def getStats(self):
        raise NotImplementedError
#        stats = dict()
#
#        stats["Request-Response exchanges"] = self.exchanges.size()
#        stats["Messages sent"] = self.numMessagesSent
#        stats["Messages received"] = self.numMessagesReceived
#
#        return str(stats)



class UDPLayer(Layer):
    """
    The class UDPLayer exchanges CoAP messages with remote endpoints using UDP
    datagrams. It is an unreliable channel and thus datagrams may arrive out of
    order, appear duplicated, or are lost without any notice, especially on
    lossy physical layers.

    The UDPLayer is the base layer of the stack, sub-calssing {@link Layer}.
    Any {@link UpperLayer} can be stacked on top, using a Communicator as
    stack builder.
    """
    #  The UDP socket used to send and receive datagrams
    #  TODO Use MulticastSocket
    #socket = DatagramSocket()

    #  The thread that listens on the socket for incoming datagrams
    #receiverThread = ReceiverThread()

    #  Inner Classes //////////////////////////////////////////////////////////
    class ReceiverThread(Thread):
        """ generated source for class ReceiverThread """
        def __init__(self):
            raise NotImplementedError
#            """ generated source for method __init__ """
#            super(ReceiverThread, self).__init__("ReceiverThread")

        def run(self):
            """ generated source for method run """
            #  always listen for incoming datagrams
#            while True:
#                #  allocate buffer
#                #  +1 to check for > RX_BUFFER_SIZE
#                #  initialize new datagram
#                #  receive datagram
#                try:
#                    self.socket.receive(datagram)
#                except IOException as e:
#                    logging.critical("Could not receive datagram: %s" % e.getMessage())
#                    continue
#                    #  TODO: Dispatch to worker thread
#                self.datagramReceived(self.datagram)

    def __init__(self, port, daemon):
        """
        Constructor for a new UDP layer
        @param port The local UDP port to listen for incoming messages
        @param daemon True if receiver thread should terminate with main thread
        """
        raise NotImplementedError
#        super(UDPLayer, self).__init__()
#        #  initialize members
#        self.socket = DatagramSocket(port)
#        self.receiverThread = self.ReceiverThread()
#        #  decide if receiver thread terminates with main thread
#        self.receiverThread.setDaemon(daemon)
#        #  start listening right from the beginning
#        self.receiverThread.start()


    def setDaemon(self, on):
        """
        Decides if the listener thread persists after the main thread
        terminates
        @param on True if the listener thread should stay alive after the main
        thread terminates. This is useful for e.g. server applications
        """
        raise NotImplementedError
        # self.receiverThread.setDaemon(on)

    def doSendMessage(self, msg):
        raise NotImplementedError
#        payload = msg.toByteArray()  # retrieve payload
#        #  create datagram
#        datagram = DatagramPacket(payload, msg.getPeerAddress().getAddress(), msg.getPeerAddress().getPort(),)
#        #  remember when this message was sent for the first time
#        #  set timestamp only once in order
#        #  to handle retransmissions correctly
#        if msg.getTimestamp() == -1:
#            msg.setTimestamp(System.nanoTime())
#            #  send it over the UDP socket
#        self.socket.send(datagram)

    def doReceiveMessage(self, msg):
        raise NotImplementedError
        #  pass message to registered receivers
        # self.deliverMessage(msg)


    def datagramReceived(self, datagram):
        raise NotImplementedError

#        if datagram.getLength() > 0:
#            #  get current time
#            #  extract message data from datagram
#            #  create new message from the received data
#            if self.msg is not None:
#                #  remember when this message was received
#                self.msg.setTimestamp(timestamp)
#                self.msg.setPeerAddress(EndpointAddress(datagram.getAddress(), datagram.getPort()))
#                if datagram.getLength() > Properties.std.getInt("RX_BUFFER_SIZE"):
#                    logging.info("Marking large datagram for blockwise transfer: {:s}".format(msg.key()))
#                    self.msg.requiresBlockwise(True)
#                    #  protect against unknown exceptions
#                try:
#                    #  call receive handler
#                    receiveMessage(msg)
#                except Exception as e:
#                    e.with_traceback()
#                    logging.critical(self.builder.__str__())
#            else:
#                logging.critical("Illegal datagram received:\n%s" % data.__str__())
#        else:
#            logging.info("Dropped empty datagram from: {:s}:{:d}".format(datagram.getAddress().getHostName(), datagram.getPort()))

    def isDaemon(self):
        """
        Checks whether the listener thread persists after the main thread
        terminates

        @return True if the listener thread stays alive after the main thread
        terminates. This is useful for e.g. server applications
        """
        raise NotImplementedError
        #return self.receiverThread.isDaemon()

    def getPort(self):
        raise NotImplementedError
        # return self.socket.getLocalPort()

    def getStats(self):
        raise NotImplementedError
#        stats = dict()
#        stats["UDP port"] = self.port
#        stats["Messages sent"] = self.numMessagesSent
#        stats["Messages received"] = self.numMessagesReceived
#        return str(stats)

class Communicator(UpperLayer):
    """
    The class Communicator provides the message passing system and builds the
    communication stack through which messages are sent and received. As a
    subclass of {@link UpperLayer} it is actually a composite layer that contains
    the subsequent layers in the order defined in {@link #buildStack()}.

    Endpoints must register as a receiver using {@link #registerReceiver(MessageReceiver)}.
    Prior to that, they should configure the Communicator using @link {@link #setup(int, boolean)}.
    A client only using {@link Request}s are not required to do any of that.
    Here, {@link Message}s will create the required instance automatically.

    The Communicator implements the Singleton pattern, as there should only be
    one stack per endpoint and it is required in different contexts to send a
    message. It is not using the Enum approach because it still needs to inherit
    from {@link UpperLayer}.
    """

#    singleton = None
#    udpPort = 0
#    runAsDaemon = True
#
#    transferBlockSize = 0
#
#    tokenLayer = TokenLayer()
#    transferLayer = TransferLayer()
#    matchingLayer = MatchingLayer()
#    transactionLayer = TransactionLayer()
#    adverseLayer = AdverseLayer()
#    udpLayer = UDPLayer()

    def __init__(self):
        """
        Constructor for a new Communicator
        @param port The local UDP port to listen for incoming messages
        @param daemon True if receiver thread should terminate with main thread
        @param defaultBlockSize The default block size used for block-wise transfers
        or -1 to disable outgoing block-wise transfers
        """
        raise NotImplementedError
        #  initialize layers
#        self.tokenLayer = TokenLayer()
#        self.transferLayer = TransferLayer(self.transferBlockSize)
#        self.matchingLayer = MatchingLayer()
#        self.transactionLayer = TransactionLayer()
#        self.adverseLayer = AdverseLayer()
#        self.udpLayer = UDPLayer(self.udpPort, self.runAsDaemon)
#        #  connect layers
#        self.buildStack()


    def setupPort(port):
        raise NotImplementedError
#        if port != self.udpPort and not singleton:
#            if not singleton:
#                udpPort = port
#                logging.config("Custom port: %d", udpPort)
#            else:
#                logging.severe("Communicator already initialized, setup failed")

    def setupTransfer(defaultBlockSize):
        raise NotImplementedError
#        if (defaultBlockSize!=transferBlockSize && singleton==null):
#            if (singleton==null):
#                transferBlockSize = defaultBlockSize
#                logging.config("Custom block size: %d" % transferBlockSize)
#            else:
#                logging.severe("Communicator already initialized, setup failed")

    def setupDeamon(daemon):
        raise NotImplementedError
#        if daemon != self.runAsDaemon and not singleton:
#            if not singleton:
#                self.runAsDaemon = daemon
#                logging.config("Custom daemon option: %b" % self.runAsDaemon)
#            else:
#                logging.critical("Communicator already initialized, setup failed")

    def buildStack(self):
        """
        This method connects the layers in order to build the communication stack
        It can be overridden by subclasses in order to add further layers, e.g.
        for introducing a layer that drops or duplicates messages by a
        probabilistic model in order to evaluate the implementation.
        """
        raise NotImplementedError
#        self.setLowerLayer(self.tokenLayer)
#        self.tokenLayer.setLowerLayer(self.transferLayer)
#        self.transferLayer.setLowerLayer(self.matchingLayer)
#        self.matchingLayer.setLowerLayer(self.transactionLayer)
#        self.transactionLayer.setLowerLayer(self.udpLayer)
#        # transactionLayer.setLowerLayer(adverseLayer);
#        # adverseLayer.setLowerLayer(udpLayer);

    def doSendMessage(self, msg):
        """
        defensive programming before entering the stack, lower layers should assume a correct message.
        """
        raise NotImplementedError

#        if msg:
#            #  check message before sending through the stack
#            if msg.getPeerAddress().getAddress() is None:
#                Exception("Remote address not specified")
#                #  delegate to first layer
#            self.sendMessageOverLowerLayer(msg)

    def doReceiveMessage(self, msg):
        raise NotImplementedError
#        if isinstance(msg, (Response,)):
#            #  initiate custom response handling
#            if response.getRequest() is not None:
#                response.getRequest().handleResponse(response)
#            #  pass message to registered receivers
#        self.deliverMessage(msg)

