package ch.ethz.inf.vs.californium.coap;

import java.io.IOException;
import java.net.SocketException;

import ch.ethz.inf.vs.californium.layers.AdverseLayer;
import ch.ethz.inf.vs.californium.layers.TokenLayer;
import ch.ethz.inf.vs.californium.layers.TransactionLayer;
import ch.ethz.inf.vs.californium.layers.MatchingLayer;
import ch.ethz.inf.vs.californium.layers.TransferLayer;
import ch.ethz.inf.vs.californium.layers.UDPLayer;
import ch.ethz.inf.vs.californium.layers.UpperLayer;

/**
 * The class Communicator provides the message passing system and builds the
 * communication stack through which messages are sent and received. As a
 * subclass of {@link UpperLayer} it is actually a composite layer that contains
 * the subsequent layers in the order defined in {@link #buildStack()}.
 * <p>
 * Endpoints must register as a receiver using {@link #registerReceiver(MessageReceiver)}.
 * Prior to that, they should configure the Communicator using @link {@link #setup(int, boolean)}.
 * A client only using {@link Request}s are not required to do any of that.
 * Here, {@link Message}s will create the required instance automatically.
 * <p>
 * The Communicator implements the Singleton pattern, as there should only be
 * one stack per endpoint and it is required in different contexts to send a
 * message. It is not using the Enum approach because it still needs to inherit
 * from {@link UpperLayer}.
 * 
 * @author Dominique Im Obersteg, Daniel Pauli, and Matthias Kovatsch
 */
public class Communicator extends UpperLayer {
	
// Static Attributes ///////////////////////////////////////////////////////////
	
	private volatile static Communicator singleton = null;
	private static int udpPort = 0;
	private static boolean runAsDaemon = true; // JVM will shut down if no user threads are running
	private static int transferBlockSize = 0;

// Members /////////////////////////////////////////////////////////////////////

	protected TokenLayer tokenLayer;
	protected TransferLayer transferLayer;
	protected MatchingLayer matchingLayer;
	protected TransactionLayer transactionLayer;
	protected AdverseLayer adverseLayer;
	protected UDPLayer udpLayer;
	
// Constructors ////////////////////////////////////////////////////////////////

	/*
	 * Constructor for a new Communicator
	 * 
	 * @param port The local UDP port to listen for incoming messages
	 * @param daemon True if receiver thread should terminate with main thread
	 * @param defaultBlockSize The default block size used for block-wise transfers
	 *        or -1 to disable outgoing block-wise transfers
	 */	
	private Communicator() throws SocketException {
		
		// initialize layers
		tokenLayer = new TokenLayer();
		transferLayer = new TransferLayer(transferBlockSize);
		matchingLayer = new MatchingLayer();
		transactionLayer = new TransactionLayer();
		adverseLayer = new AdverseLayer();
		udpLayer = new UDPLayer(udpPort, runAsDaemon);

		// connect layers
		buildStack();
		
	}
	
	public static Communicator getInstance() {
		
		if (singleton==null) {
			synchronized (Communicator.class) {
				if (singleton==null) {
					try {
						singleton = new Communicator();
					} catch (SocketException e) {
						LOG.severe(String.format("Failed to create Communicator: %s\n", e.getMessage()));
						System.exit(-1);
					}
				}
			}
		}
		return singleton;
	}
	
	public static void setupPort(int port) {
		if (port!=udpPort && singleton==null) {
			synchronized (Communicator.class) {
				if (singleton==null) {

					udpPort = port;
					LOG.config(String.format("Custom port: %d", udpPort));
					
				} else {
					LOG.severe("Communicator already initialized, setup failed");
				}
			}
		}
	}
	public static void setupTransfer(int defaultBlockSize) {
		if (defaultBlockSize!=transferBlockSize && singleton==null) {
			synchronized (Communicator.class) {
				if (singleton==null) {
					
					transferBlockSize = defaultBlockSize;
					LOG.config(String.format("Custom block size: %d", transferBlockSize));
					
				} else {
					LOG.severe("Communicator already initialized, setup failed");
				}
			}
		}
	}
	public static void setupDeamon(boolean daemon) {
		if (daemon!=runAsDaemon && singleton==null) {
			synchronized (Communicator.class) {
				if (singleton==null) {
					
					runAsDaemon = daemon;
					LOG.config(String.format("Custom daemon option: %b", runAsDaemon));
					
				} else {
					LOG.severe("Communicator already initialized, setup failed");
				}
			}
		}
	}

	// Internal ////////////////////////////////////////////////////////////////

	/*
	 * This method connects the layers in order to build the communication stack
	 * 
	 * It can be overridden by subclasses in order to add further layers, e.g.
	 * for introducing a layer that drops or duplicates messages by a
	 * probabilistic model in order to evaluate the implementation.
	 */
	private void buildStack() {

		this.setLowerLayer(tokenLayer);
		tokenLayer.setLowerLayer(transferLayer);
		transferLayer.setLowerLayer(matchingLayer);
		matchingLayer.setLowerLayer(transactionLayer);
		transactionLayer.setLowerLayer(udpLayer);
		
		//transactionLayer.setLowerLayer(adverseLayer);
		//adverseLayer.setLowerLayer(udpLayer);

	}

	// I/O implementation //////////////////////////////////////////////////////

	@Override
	protected void doSendMessage(Message msg) throws IOException {

		// defensive programming before entering the stack, lower layers should assume a correct message.
		if (msg != null) {
		
			// check message before sending through the stack
			if (msg.getPeerAddress().getAddress()==null) {
				throw new IOException("Remote address not specified");
			}
			
			// delegate to first layer
			sendMessageOverLowerLayer(msg);
		}
	}

	@Override
	protected void doReceiveMessage(Message msg) {

		if (msg instanceof Response) {
			Response response = (Response) msg;

			// initiate custom response handling
			if (response.getRequest() != null) {
				response.getRequest().handleResponse(response);
			}
		}

		// pass message to registered receivers
		deliverMessage(msg);

	}

	// Queries /////////////////////////////////////////////////////////////////

	public int port() {
		return udpLayer.getPort();
	}

	public TokenLayer getTokenLayer() {
		return this.tokenLayer;
	}
	
	public TransferLayer getTransferLayer() {
		return this.transferLayer;
	}
	
	public MatchingLayer getMatchingLayer() {
		return this.matchingLayer;
	}
	
	public TransactionLayer getTransactionLayer() {
		return this.transactionLayer;
	}
	
	public UDPLayer getUDPLayer() {
		return this.udpLayer;
	}
}
