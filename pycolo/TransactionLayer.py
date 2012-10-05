import logging
import random
from pycolo import ObservingManager, Message, Response, UpperLayer, MAX_RETRANSMIT, RESPONSE_TIMEOUT, RESPONSE_RANDOM_FACTOR
from pycolo import MESSAGE_CACHE_SIZE
from pycolo import Transaction

class TransactionLayer(UpperLayer):
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
    currentMID = random.SystemRandom() * 0x10000

    def nextMessageID():
    	"""
    	Returns the next message ID to use out of the consecutive 16 - bit
    	range.
    	@return the current message ID
    	"""
        self.currentMID += 1
        self.currentMID %= 0x10000
        return self.currentMID
    
    # The timer daemon to schedule retransmissions.
    timer = Timer(true) # run as daemon

    # The Table to store the transactions of outgoing messages.
    transactionTable = {}

    # The cache for duplicate detection.
    dupCache = MessageCache()

    # Cache used to retransmit replies to incoming messages
    replyCache = MessageCache()


    class Transaction:
    	"""
    	Entity class to keep state of retransmissions.
    	"""
        msg = Message()
        retransmitTask = RestransmitTask()
        numRetransmit = 0
        timeout = 0 # to satisfy RESPONSE_RANDOM_FACTOR

    class MessageCache:
        """
        The MessageCache is a utility class used for duplicate detection and
        reply retransmissions. It is a ring buffer whose size is configured
        through the Californium properties file.
        """

        def removeEldestEntry(eldest):
            return size() > MESSAGE_CACHE_SIZE


    class RetransmitTask(TimerTask):
        """
        Utility class to handle timeouts.
        """

        transaction = Transaction()

        def RetransmitTask(transaction):
            self.transaction = transaction

        def run():
            handleResponseTimeout(transaction)

    def initialTimeout():
        """
        Calculates the initial timeout for outgoing confirmable messages.
        :return: the timeout in milliseconds
        """
        
        min = RESPONSE_TIMEOUT
        f = RESPONSE_RANDOM_FACTOR
        
        return min + (min * (f - 1) * random.SystemRandom())
    

    def doSendMessage(msg):

        # set message ID
        if msg.getMID() < 0:
            msg.setMID(self.nextMessageID())
        
        # check if message needs confirmation, i.e., a reply is expected
        if msg.isConfirmable():

            # create new transmission context for retransmissions
            self.addTransaction(msg)

        elif msg.isReply():

            # put message into ring buffer in case peer retransmits
            self.replyCache.put(msg.transactionKey(), msg)

        # send message over unreliable channel
        self.sendMessageOverLowerLayer(msg)


    def doReceiveMessage(msg):

        # check for duplicate
        if msg.key() in dupCache:

            # check for retransmitted Confirmable
            if msg.isConfirmable():

                # retrieve cached reply
                reply = replyCache.get(msg.transactionKey())
                if reply:
                    # retransmit reply
                    try:
                        logging.info("Replied to duplicate confirmable: %s" % msg.key())
                        self.sendMessageOverLowerLayer(reply)
                    except IOException e:
                        logging.severe("Replying to duplicate confirmable failed: %s\n%s", msg.key(), e.getMessage())
                else:
                    logging.info("Dropped duplicate confirmable without cached reply: %s"% msg.key())

                # drop duplicate anyway
                return

            else:
                # ignore duplicate
                logging.info(String.format("Dropped duplicate: %s", msg.key()));
                return;

        else:
            # cache received message
            dupCache.put(msg.key(), msg);


        # check for reply to CON and remove transaction
        if msg.isReply():

            # retrieve transaction for the incoming message
            Transaction transaction = getTransaction(msg);

            if transaction:

                # transmission completed
                removeTransaction(transaction);
                
                if msg.isEmptyACK():
                    
                    # transaction is complete, no information for higher layers
                    return;
                    
                else if (msg.getType() == Message.messageType.RST):
                    
                    handleIncomingReset(msg);
                    return;
                
            elif (msg.getType() == Message.messageType.RST):
                
                handleIncomingReset(msg);
                return;

            else:
                
                # ignore unexpected reply except RST, which could match to a NON sent by the endpoint
                logging.warning("Dropped unexpected reply: %s", msg.key())
                return;

        # Only accept Responses here, Requests must be handled at application level 
        if (msg instanceof Response && msg.isConfirmable()) {
            try:
                logging.info("Accepted confirmable response: %s" % msg.key())
                sendMessageOverLowerLayer(msg.newAccept())
            except (IOException e)
                logging.severe("Accepting confirmable failed: %s\n%s" % msg.key(), e.getMessage())

        # pass message to registered receivers
        deliverMessage(msg)

    def handleIncomingReset(msg):
        
        # remove possible observers
        ObservingManager.getInstance().removeObserver(msg.getPeerAddress().toString(), msg.getMID())

    def handleResponseTimeout(Transaction transaction):

        max = MAX_RETRANSMIT
        
        # check if limit of retransmissions reached
        if transaction.numRetransmit < max:

            # retransmit message
            transaction.msg.setRetransmissioned(transaction.numRetransmit)

            logging.info("Retransmitting %s (%d of %d)" % transaction.msg.key(), transaction.numRetransmit, max)

            try:
                sendMessageOverLowerLayer(transaction.msg);
            except IOException e:

                logging.severe("Retransmission failed: %s", e.getMessage())
                removeTransaction(transaction);

                return;

            # schedule next retransmission
            scheduleRetransmission(transaction)

        else:

            # cancel transmission
            removeTransaction(transaction)
            
            # cancel observations
            ObservingManager.getInstance().removeObserver(transaction.msg.getPeerAddress().toString())

            # invoke event handler method
            transaction.msg.handleTimeout()

    def addTransaction(msg):

        # initialize new transmission context
        transaction = Transaction()
        transaction.msg = msg
        transaction.numRetransmit = 0
        transaction.retransmitTask = None

        transactionTable.put(msg.transactionKey(), transaction)

        # schedule first retransmission
        self.scheduleRetransmission(transaction)
        
        logging.info("Stored new transaction for %s" % msg.key())

        return transaction

    def getTransaction(msg):
        return transactionTable.get(msg.transactionKey())

    def removeTransaction(transaction):

        # cancel any pending retransmission schedule
        transaction.retransmitTask.cancel()
        transaction.retransmitTask = None

        # remove transaction from table
        self.transactionTable.remove(transaction.msg.transactionKey())
        
        logging.info("Cleared transaction for %s" % transaction.msg.key())

    def scheduleRetransmission(transaction):

        # cancel existing schedule (if any)
        if transaction.retransmitTask:
            transaction.retransmitTask.cancel()

        # create new retransmission task
        transaction.retransmitTask = RetransmitTask(transaction)

        # calculate timeout using exponential back - off

        if transaction.timeout == 0:
            # use initial timeout
            transaction.timeout = self.initialTimeout()
        else:
            # double timeout
            transaction.timeout *= 2

        # schedule retransmission task
        timer.schedule(transaction.retransmitTask, transaction.timeout)

    def __str__():
        stats = dict()
        stats["Current message ID"] = currentMID
        stats["Open transactions"] = transactionTable.size()
        stats["Messages sent"] = numMessagesSent
        stats["Messages received"] = numMessagesReceived
        return str(stats)
