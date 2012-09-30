#!/usr/bin/env python
""" generated source for module Communicator """
# package: ch.ethz.inf.vs.californium.coap
import java.io.IOException

import java.net.SocketException

import ch.ethz.inf.vs.californium.layers.AdverseLayer

import ch.ethz.inf.vs.californium.layers.TokenLayer

import ch.ethz.inf.vs.californium.layers.TransactionLayer

import ch.ethz.inf.vs.californium.layers.MatchingLayer

import ch.ethz.inf.vs.californium.layers.TransferLayer

import ch.ethz.inf.vs.californium.layers.UDPLayer

import ch.ethz.inf.vs.californium.layers.UpperLayer

# 
#  * The class Communicator provides the message passing system and builds the
#  * communication stack through which messages are sent and received. As a
#  * subclass of {@link UpperLayer} it is actually a composite layer that contains
#  * the subsequent layers in the order defined in {@link #buildStack()}.
#  * <p>
#  * Endpoints must register as a receiver using {@link #registerReceiver(MessageReceiver)}.
#  * Prior to that, they should configure the Communicator using @link {@link #setup(int, boolean)}.
#  * A client only using {@link Request}s are not required to do any of that.
#  * Here, {@link Message}s will create the required instance automatically.
#  * <p>
#  * The Communicator implements the Singleton pattern, as there should only be
#  * one stack per endpoint and it is required in different contexts to send a
#  * message. It is not using the Enum approach because it still needs to inherit
#  * from {@link UpperLayer}.
#  * 
#  * @author Dominique Im Obersteg, Daniel Pauli, and Matthias Kovatsch
#  
class Communicator(UpperLayer):
    """ generated source for class Communicator """
    #  Static Attributes ///////////////////////////////////////////////////////////
    singleton = None
    udpPort = 0
    runAsDaemon = True

    #  JVM will shut down if no user threads are running
    transferBlockSize = 0

    #  Members /////////////////////////////////////////////////////////////////////
    tokenLayer = TokenLayer()
    transferLayer = TransferLayer()
    matchingLayer = MatchingLayer()
    transactionLayer = TransactionLayer()
    adverseLayer = AdverseLayer()
    udpLayer = UDPLayer()

    #  Constructors ////////////////////////////////////////////////////////////////
    # 
    # 	 * Constructor for a new Communicator
    # 	 * 
    # 	 * @param port The local UDP port to listen for incoming messages
    # 	 * @param daemon True if receiver thread should terminate with main thread
    # 	 * @param defaultBlockSize The default block size used for block-wise transfers
    # 	 *        or -1 to disable outgoing block-wise transfers
    # 	 
    def __init__(self):
        """ generated source for method __init__ """
        super(Communicator, self).__init__()
        #  initialize layers
        self.tokenLayer = TokenLayer()
        self.transferLayer = TransferLayer(self.transferBlockSize)
        self.matchingLayer = MatchingLayer()
        self.transactionLayer = TransactionLayer()
        self.adverseLayer = AdverseLayer()
        self.udpLayer = UDPLayer(self.udpPort, self.runAsDaemon)
        #  connect layers
        buildStack()

    # 	
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
    # 	public static void setupPort(int port) {
    # 		if (port!=udpPort && singleton==null) {
    # 				if (singleton==null) {
    # 					udpPort = port;
    # 					LOG.config(String.format("Custom port: %d", udpPort));
    # 				} else {
    # 					LOG.severe("Communicator already initialized, setup failed");
    # 				}
    # 			}
    # 		}
    # 	}
    # 	public static void setupTransfer(int defaultBlockSize) {
    # 		if (defaultBlockSize!=transferBlockSize && singleton==null) {
    # 				if (singleton==null) {
    # 					transferBlockSize = defaultBlockSize;
    # 					LOG.config(String.format("Custom block size: %d", transferBlockSize));
    # 				} else {
    # 					LOG.severe("Communicator already initialized, setup failed");
    # 				}
    # 			}
    # 		}
    # 	}
    # 
    # 	public static void setupDeamon(boolean daemon) {
    # 		if (daemon!=runAsDaemon && singleton==null) {
    # 				if (singleton==null) {
    # 					runAsDaemon = daemon;
    # 					LOG.config(String.format("Custom daemon option: %b", runAsDaemon));
    # 				} else {
    # 					LOG.severe("Communicator already initialized, setup failed");
    # 				}
    # 			}
    # 		}
    # 	}
    # 
    #  Internal ////////////////////////////////////////////////////////////////
    # 
    # 	 * This method connects the layers in order to build the communication stack
    # 	 * 
    # 	 * It can be overridden by subclasses in order to add further layers, e.g.
    # 	 * for introducing a layer that drops or duplicates messages by a
    # 	 * probabilistic model in order to evaluate the implementation.
    # 	 
    def buildStack(self):
        """ generated source for method buildStack """
        self.setLowerLayer(self.tokenLayer)
        self.tokenLayer.setLowerLayer(self.transferLayer)
        self.transferLayer.setLowerLayer(self.matchingLayer)
        self.matchingLayer.setLowerLayer(self.transactionLayer)
        self.transactionLayer.setLowerLayer(self.udpLayer)
        # transactionLayer.setLowerLayer(adverseLayer);
        # adverseLayer.setLowerLayer(udpLayer);

    #  I/O implementation //////////////////////////////////////////////////////
    def doSendMessage(self, msg):
        """ generated source for method doSendMessage """
        #  defensive programming before entering the stack, lower layers should assume a correct message.
        if msg != None:
            #  check message before sending through the stack
            if msg.getPeerAddress().getAddress() == None:
                raise IOException("Remote address not specified")
            #  delegate to first layer
            sendMessageOverLowerLayer(msg)

    def doReceiveMessage(self, msg):
        """ generated source for method doReceiveMessage """
        if isinstance(msg, (Response, )):
            #  initiate custom response handling
            if response.getRequest() != None:
                response.getRequest().handleResponse(response)
        #  pass message to registered receivers
        deliverMessage(msg)

    #  Queries /////////////////////////////////////////////////////////////////
    def port(self):
        """ generated source for method port """
        return self.udpLayer.getPort()

    def getTokenLayer(self):
        """ generated source for method getTokenLayer """
        return self.tokenLayer

    def getTransferLayer(self):
        """ generated source for method getTransferLayer """
        return self.transferLayer

    def getMatchingLayer(self):
        """ generated source for method getMatchingLayer """
        return self.matchingLayer

    def getTransactionLayer(self):
        """ generated source for method getTransactionLayer """
        return self.transactionLayer

    def getUDPLayer(self):
        """ generated source for method getUDPLayer """
        return self.udpLayer

Communicator.# 			synchronized (Communicator.class) {

Communicator.# 			synchronized (Communicator.class) {

Communicator.# 			synchronized (Communicator.class) {

Communicator.# 			synchronized (Communicator.class) {

