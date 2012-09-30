# coding=utf-8

import logging

from pycolo.coap import BlockOption
from pycolo.coap import CodeRegistry
from pycolo.coap import Message
from pycolo.coap.OptionNumberRegistry import OptionNumberRegistry
from pycolo.coap import Request
from pycolo.coap import Response
from pycolo.coap import Message
from pycolo.utils import Properties


class TransferLayer(UpperLayer):
    """
#  * The class TransferLayer provides support for
#  * <a href="http://tools.ietf.org/html/draft-ietf-core-block">blockwise transfers</a>.
#  * <p>
#  * {@link #doSendMessage(Message)} and {@link #doReceiveMessage(Message)} do not
#  * distinguish between clients and server directly, but rather between incoming
#  * and outgoing transfers. This saves duplicate code, but introduces rather
#  * confusing Request/Response checks at various places.<br/>
#  * TODO: Explore alternative designs.
    """
    class TransferContext(object):
        """ generated source for class TransferContext """
        cache = Message()
        uriPath = str()
        current = BlockOption()

        #  TODO: timer
        def __init__(self, msg):
            """ generated source for method __init__ """
            if isinstance(msg, (Request,)):
                self.cache = msg
                self.uriPath = msg.getUriPath()
                self.current = msg.getFirstOption(OptionNumberRegistry.BLOCK1)
            elif isinstance(msg, (Response,)):
                msg.requiresToken(False)
                #  FIXME check if still required after new TokenLayer
                self.cache = msg
                self.uriPath = msg.getRequest().getUriPath()
                self.current = msg.getFirstOption(OptionNumberRegistry.BLOCK2)
            logging.info("Created new transfer context for {:s}: {:s}".format(self.uriPath, msg.sequenceKey()))

    incoming = dict()
    outgoing = dict()
    defaultSZX = int()

    @overloaded
    def __init__(self, defaultBlockSize):
        """ generated source for method __init__ """
        super(TransferLayer, self).__init__()
        if defaultBlockSize == 0:
            defaultBlockSize = Properties.std.getInt("DEFAULT_BLOCK_SIZE")
        if defaultBlockSize > 0:
            self.defaultSZX = BlockOption.encodeSZX(defaultBlockSize)
            if not BlockOption.validSZX(self.defaultSZX):
                self.defaultSZX = 6 if defaultBlockSize > 1024 else BlockOption.encodeSZX(defaultBlockSize & 0x07f0)
                logging.warning("Unsupported block size {:d}, using {:d} instead".format(defaultBlockSize, BlockOption.decodeSZX(self.defaultSZX)))
        else:
            self.defaultSZX = -1

    @__init__.register(object)
    def __init___0(self):
        """ generated source for method __init___0 """
        super(TransferLayer, self).__init__()
        self.__init__(0)

    def doSendMessage(self, msg):
        """ generated source for method doSendMessage """
        sendSZX = self.defaultSZX
        sendNUM = 0
        if isinstance(msg, (Response,)) and msg.getRequest() != None:
            if self.buddyBlock:
                if self.buddyBlock.getSZX() < self.defaultSZX:
                    sendSZX = self.buddyBlock.getSZX()
                sendNUM = self.buddyBlock.getNUM()
        if msg.payloadSize() > BlockOption.decodeSZX(sendSZX):
            if self.msgBlock != None:
                if self.block1 != None and self.block1.getM() or block2 != None and self.block2.getM():
                    msg.setOption(self.block1)
                    msg.setOption(self.block2)
                    self.outgoing.put(msg.sequenceKey(), self.transfer)
                    logging.info("Caching blockwise transfer for NUM {:d}: {:s}".format(sendNUM, msg.sequenceKey()))
                else:
                    logging.info("Answering block request without caching: {:s} | {:s}".format(msg.sequenceKey(), block2))
                self.sendMessageOverLowerLayer(self.msgBlock)
            else:
                logging.info("Rejecting initial out-of-scope request: {:s} | NUM: {:d}, SZX: {:d} ({:d} bytes), M: n/a, {:d} bytes available".format(msg.sequenceKey(), sendNUM, sendSZX, BlockOption.decodeSZX(sendSZX), msg.payloadSize()))
                self.handleOutOfScopeError(msg.newReply(True))
        else:
            self.sendMessageOverLowerLayer(msg)

    def doReceiveMessage(self, msg):
        """ generated source for method doReceiveMessage """
        blockIn = None
        blockOut = None
        if isinstance(msg, (Request,)):
            blockIn = msg.getFirstOption(OptionNumberRegistry.BLOCK1)
            blockOut = msg.getFirstOption(OptionNumberRegistry.BLOCK2)
        elif isinstance(msg, (Response,)):
            blockIn = msg.getFirstOption(OptionNumberRegistry.BLOCK2)
            blockOut = msg.getFirstOption(OptionNumberRegistry.BLOCK1)
            if blockOut != None:
                blockOut.setNUM(blockOut.getNUM() + 1)
        else:
            LOG.warning("Unknown message type received: {:s}".format(msg.key()))
            return
        if blockIn == None and msg.requiresBlockwise():
            blockIn = BlockOption(OptionNumberRegistry.BLOCK1, 0, self.defaultSZX, True)
            handleIncomingPayload(msg, blockIn)
            return
        elif blockIn != None:
            handleIncomingPayload(msg, blockIn)
            return
        elif blockOut != None:
            LOG.finer("Received demand for next block: {:s} | {:s}".format(msg.sequenceKey(), blockOut))
            if self.transfer:
                if isinstance(msg, (Request,)) and not msg.getUriPath() == transfer.uriPath:
                    self.outgoing.remove(msg.sequenceKey())
                    LOG.fine("Freed blockwise transfer by client token reuse: {:s}".format(msg.sequenceKey()))
                else:
                    if isinstance(msg, (Request,)):
                        self.transfer.cache.setMID(msg.getMID())
                    if next != None:
                        try:
                            logging.info("Sending next block: {:s} | {:s}".format(next.sequenceKey(), blockOut))
                            sendMessageOverLowerLayer(next)
                        except IOException as e:
                            logging.critical("Failed to send block response: {:s}".format(e.getMessage()))
                        if not self.respBlock.getM() and isinstance(msg, (Request,)):
                            self.outgoing.remove(msg.sequenceKey())
                            logging.info("Freed blockwise download by completion: {:s}".format(next.sequenceKey()))
                        return
                    elif isinstance(msg, (Response,)) and not blockOut.getM():
                        self.outgoing.remove(msg.sequenceKey())
                        LOG.fine("Freed blockwise upload by completion: {:s}".format(msg.sequenceKey()))
                        msg.setRequest(self.transfer.cache)
                    else:
                        LOG.warning("Rejecting out-of-scope demand for cached transfer (freed): {:s} | {:s}, {:d} bytes available".format(msg.sequenceKey(), blockOut, transfer.cache.payloadSize()))
                        self.outgoing.remove(msg.sequenceKey())
                        self.handleOutOfScopeError(msg.newReply(True))
                        return
        elif isinstance(msg, (Response,)):
            if self.transfer:
                msg.setRequest(self.transfer.cache)
                self.outgoing.remove(msg.sequenceKey())
                logging.info("Freed outgoing transfer by client abort: {:s}".format(msg.sequenceKey()))
            transfer = self.incoming.get(msg.sequenceKey())
            if transfer != None:
                msg.setRequest(transfer.cache)
                self.incoming.remove(msg.sequenceKey())
                logging.info("Freed incoming transfer by client abort: {:s}".format(msg.sequenceKey()))
        self.deliverMessage(msg)

    def handleIncomingPayload(self, msg, blockOpt):
        """ generated source for method handleIncomingPayload """
        transfer = self.incoming.get(msg.sequenceKey())
        if blockOpt.getNUM() > 0 and transfer != None:
            if blockOpt.getNUM() * blockOpt.getSize() == (transfer.current.getNUM() + 1) * transfer.current.getSize():
                transfer.cache.appendPayload(msg.getPayload())
                transfer.cache.setMID(msg.getMID())
                logging.info("Received next block:  {:s} | {:s}".format(msg.sequenceKey(), blockOpt))
            else:
                LOG.info("Dropping wrong block: {:s} | {:s}".format(msg.sequenceKey(), blockOpt))
        elif blockOpt.getNUM() == 0 and msg.payloadSize() > 0:
            if msg.payloadSize() > blockOpt.getSize():
                blockOpt.setNUM(newNUM - 1)
                msg.setPayload(Arrays.copyOf(msg.getPayload(), newNUM))
            transfer = self.TransferContext(msg)
            self.incoming.put(msg.sequenceKey(), transfer)
            LOG.fine("Incoming blockwise transfer: {:s} | {:s}".format(msg.sequenceKey(), blockOpt))
        else:
            LOG.info("Rejecting out-of-order block: {:s} | {:s}".format(msg.sequenceKey(), blockOpt))
            handleIncompleteError(msg.newReply(True))
            return
        if blockOpt.getM():
            if demandSZX > self.defaultSZX:
                demandNUM = demandSZX / self.defaultSZX * demandNUM
                demandSZX = self.defaultSZX
            if isinstance(msg, (Response,)):
                reply = Request(CodeRegistry.METHOD_GET, not msg.isNonConfirmable())
                reply.setURI("coap://" + msg.getPeerAddress().__str__() + transfer.uriPath)
                demandNUM += 1
            elif isinstance(msg, (Request,)):
                reply = Response(CodeRegistry.RESP_VALID)
                reply.setType(messageType.ACK if msg.isConfirmable() else messageType.NON)
                reply.setPeerAddress(msg.getPeerAddress())
                if msg.isConfirmable():
                    reply.setMID(msg.getMID())
            else:
                LOG.severe("Unsupported message type: {:s}".format(msg.key()))
                return
            reply.setOption(msg.getFirstOption(OptionNumberRegistry.TOKEN))
            reply.setOption(next)
            try:
                LOG.fine("Demanding next block: {:s} | {:s}".format(reply.sequenceKey(), next))
                sendMessageOverLowerLayer(reply)
            except IOException as e:
                LOG.severe("Failed to request block: {:s}".format(e.getMessage()))
            transfer.current = blockOpt
        else:
            transfer.cache.setOption(blockOpt)
            LOG.fine("Finished blockwise transfer: {:s}".format(msg.sequenceKey()))
            self.incoming.remove(msg.sequenceKey())
            deliverMessage(transfer.cache)

    def handleOutOfScopeError(self, resp):
        """ generated source for method handleOutOfScopeError """
        resp.setCode(CodeRegistry.RESP_BAD_REQUEST)
        resp.setPayload("BlockOutOfScope")
        try:
            sendMessageOverLowerLayer(resp)
        except IOException as e:
            LOG.severe("Failed to send error message: {:s}".format(e.getMessage()))

    def handleIncompleteError(self, resp):
        """ generated source for method handleIncompleteError """
        resp.setCode(CodeRegistry.RESP_REQUEST_ENTITY_INCOMPLETE)
        resp.setPayload("Start with block num 0")
        try:
            sendMessageOverLowerLayer(resp)
        except IOException as e:
            LOG.severe("Failed to send error message: {:s}".format(e.getMessage()))

    @classmethod
    def getBlock(cls, msg, num, szx):
        """ generated source for method getBlock """
        blockSize = 1 << (szx + 4)
        payloadOffset = num * blockSize
        payloadLeft = msg.payloadSize() - payloadOffset
        if payloadLeft > 0:
            if isinstance(msg, (Request,)):
                block = Request(msg.getCode(), msg.isConfirmable())
            else:
                block = Response(msg.getCode())
                if num == 0 and msg.getType() == Message.messageType.CON:
                    block.setType(Message.messageType.CON)
                else:
                    block.setType(Message.messageType.NON if msg.isNonConfirmable() else Message.messageType.ACK)
                block.setMID(msg.getMID())
            block.setPeerAddress(msg.getPeerAddress())
            for opt in msg.getOptions():
                block.addOption(opt)
            if not m:
                blockSize = payloadLeft
            System.arraycopy(msg.getPayload(), payloadOffset, blockPayload, 0, blockSize)
            block.setPayload(blockPayload)
            if isinstance(msg, (Request,)):
                blockOpt = BlockOption(OptionNumberRegistry.BLOCK1, num, szx, m)
            else:
                blockOpt = BlockOption(OptionNumberRegistry.BLOCK2, num, szx, m)
            block.setOption(blockOpt)
            return block
        else:
            return None

    def getStats(self):
        """ generated source for method getStats """
        stats = StringBuilder()
        stats.append("Default block size: ")
        stats.append(BlockOption.decodeSZX(self.defaultSZX))
        stats.append('\n')
        stats.append("Outgoing cache size: ")
        stats.append(len(self.outgoing))
        stats.append('\n')
        stats.append("Incoming cache size: ")
        stats.append(len(self.incoming))
        stats.append('\n')
        stats.append("Messages sent:     ")
        stats.append(numMessagesSent)
        stats.append('\n')
        stats.append("Messages received: ")
        stats.append(numMessagesReceived)
        return stats.__str__()
