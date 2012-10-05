# -*- coding:utf-8 -*-
import logging
from pycolo import TransactionLayer, UpperLayer, UDPLayer, TransferLayer, MatchingLayer, AdverseLayer, TokenLayer

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

    singleton = None
    udpPort = 0
    runAsDaemon = True

    transferBlockSize = 0

    tokenLayer = TokenLayer()
    transferLayer = TransferLayer()
    matchingLayer = MatchingLayer()
    transactionLayer = TransactionLayer()
    adverseLayer = AdverseLayer()
    udpLayer = UDPLayer()

    def __init__(self):
        """
        Constructor for a new Communicator
        @param port The local UDP port to listen for incoming messages
        @param daemon True if receiver thread should terminate with main thread
        @param defaultBlockSize The default block size used for block-wise transfers
        or -1 to disable outgoing block-wise transfers
        """
        #  initialize layers
        self.tokenLayer = TokenLayer()
        self.transferLayer = TransferLayer(self.transferBlockSize)
        self.matchingLayer = MatchingLayer()
        self.transactionLayer = TransactionLayer()
        self.adverseLayer = AdverseLayer()
        self.udpLayer = UDPLayer(self.udpPort, self.runAsDaemon)
        #  connect layers
        self.buildStack()

    # 	public static Communicator getInstance() {
    # 		if (singleton==null) {
    # 				if (singleton==null) {
    # 					try {
    # 						singleton = new Communicator();
    # 					} catch (SocketException e) {
    # 						LOG.severe(String.format("Failed to create Communicator: %s\n", e.getMessage()));
    # 						System.exit(-1);
    # 					}
    # 				}
    # 			}
    # 		}
    # 		return singleton;
    # 	}
    def setupPort(port):
        if port != self.udpPort and not singleton:
            if not singleton:
                udpPort = port;
                logging.config("Custom port: %d", udpPort)
            else:
                logging.severe("Communicator already initialized, setup failed")

    def setupTransfer(defaultBlockSize):
        if (defaultBlockSize!=transferBlockSize && singleton==null):
            if (singleton==null):
                transferBlockSize = defaultBlockSize
                logging.config(String.format("Custom block size: %d", transferBlockSize))
            else:
                logging.severe("Communicator already initialized, setup failed");

    def setupDeamon(daemon):
        if daemon != self.runAsDaemon and not singleton:
            if not singleton:
                self.runAsDaemon = daemon
                logging.config("Custom daemon option: %b" % runAsDaemon)
            else:
                logging.critical("Communicator already initialized, setup failed")

    def buildStack(self):
        """
        This method connects the layers in order to build the communication stack
        It can be overridden by subclasses in order to add further layers, e.g.
        for introducing a layer that drops or duplicates messages by a
        probabilistic model in order to evaluate the implementation.
        """
        self.setLowerLayer(self.tokenLayer)
        self.tokenLayer.setLowerLayer(self.transferLayer)
        self.transferLayer.setLowerLayer(self.matchingLayer)
        self.matchingLayer.setLowerLayer(self.transactionLayer)
        self.transactionLayer.setLowerLayer(self.udpLayer)
        # transactionLayer.setLowerLayer(adverseLayer);
        # adverseLayer.setLowerLayer(udpLayer);

    def doSendMessage(self, msg):
        """ generated source for method doSendMessage """
        #  defensive programming before entering the stack, lower layers should assume a correct message.
        if msg != None:
            #  check message before sending through the stack
            if msg.getPeerAddress().getAddress() == None:
                raise "Remote address not specified"
            #  delegate to first layer
            self.sendMessageOverLowerLayer(msg)

    def doReceiveMessage(self, msg):
        """ generated source for method doReceiveMessage """
        if isinstance(msg, (Response,)):
            #  initiate custom response handling
            if response.getRequest() != None:
                response.getRequest().handleResponse(response)
        #  pass message to registered receivers
        self.deliverMessage(msg)
