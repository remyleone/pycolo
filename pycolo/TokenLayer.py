# coding=utf-8
import logging
from threading import Timer
from pycolo import DEFAULT_OVERALL_TIMEOUT
from pycolo.codes import codes


class TokenLayer(UpperLayer):
    """
    This class takes care of unique tokens for each sequence of request/response
    exchanges.
    Additionally, the TokenLayer takes care of an overall timeout for each
    request/response exchange.
    """
	
	exchanges = dict()

	# A timer for scheduling overall request timeouts.
	timer = Timer(true);
	
	# The time to wait for requests to complete, in milliseconds.
	sequenceTimeout = 0

	
	class RequestResponseSequence:
        """
        Entity class to keep state of transfers
        """
		public String key
		public Request request
		public TimerTask timeoutTask
	
	class TimeoutTask(TimerTask):
        """
        Utility class to provide transaction timeouts
        """
		
		private RequestResponseSequence sequence;

		public TimeoutTask(RequestResponseSequence sequence) {
			this.sequence = sequence;
		}
		
		@Override
		def run():
			transferTimedOut(sequence)


	
	def __init__(self, sequenceTimeout=DEFAULT_OVERALL_TIMEOUT):
		# member initialization
		self.sequenceTimeout = sequenceTimeout

	def doSendMessage(msg):
		
		# set token option if required
		if msg.requiresToken():
			msg.setToken( TokenManager.getInstance().acquireToken(true) )
		
		# use overall timeout for clients (e.g., server crash after separate response ACK)
		if msg is Request:
			logging.info(String.format("Requesting response for %s: %s",  ((Request) msg).getUriPath(), msg.sequenceKey()));
			addExchange((Request) msg);
		elif (msg.getCode()== codes.EMPTY_MESSAGE):
			logging.info(String.format("Accepting request: %s", msg.key()));
		else:
			logging.info(String.format("Responding request: %s", msg.sequenceKey()));
		
		self.sendMessageOverLowerLayer(msg)
	
	@Override
	def doReceiveMessage(msg):

		if (msg instanceof Response) {

			response = (Response) msg;
			
			RequestResponseSequence sequence = getExchange(msg.sequenceKey());

			# check for missing token
			if (not sequence and not response.getToken()):
				
				logging.warning("Remote endpoint failed to echo token: %s" % msg.key())
				
				# TODO try to recover from peerAddress
				
				# let timeout handle the problem
				return
			
			if sequence:
				
				# cancel timeout
				sequence.timeoutTask.cancel();
				
				# TODO separate observe registry
				if msg.getFirstOption(OptionNumberRegistry.OBSERVE)==null:
					removeExchange(msg.sequenceKey())

				logging.info(String.format("Incoming response from %s: %s # RTT: %fms", ((Response) msg).getRequest().getUriPath(), msg.sequenceKey(), ((Response) msg).getRTT()));
				deliverMessage(msg)
				
			else:
			
				logging.warning(String.format("Dropping unexpected response: %s", response.sequenceKey()))
			
		elif msg is Request:
			
			logging.info("Incoming request: %s" % msg.sequenceKey())
			
			self.deliverMessage(msg)

	def addExchange(request):
		
		# be aware when manually setting tokens, as request/response will be replace
		self.removeExchange(request.sequenceKey());
		
		# create new Transaction
		RequestResponseSequence sequence = new RequestResponseSequence();
		sequence.key = request.sequenceKey();
		sequence.request = request;
		sequence.timeoutTask = new TimeoutTask(sequence);
		
		# associate token with Transaction
		exchanges.put(sequence.key, sequence);
		
		timer.schedule(sequence.timeoutTask, sequenceTimeout);

		logging.fine("Stored new exchange: %s" % sequence.key)
		
		return sequence
	
	def getExchange(key):
		return exchanges.get(key)
	
	def removeExchange(key):
		
		exchange = exchanges.remove(key)
		
		if exchange:
			
			exchange.timeoutTask.cancel()
			TokenManager.getInstance().releaseToken(exchange.request.getToken())
			logging.finer(String.format("Cleared exchange: %s", exchange.key))

	def transferTimedOut(exchange):
		
		# cancel transaction
		self.removeExchange(exchange.key)
		
		logging.warning("Request/Response exchange timed out: %s" % exchange.request.sequenceKey())
		
		# call event handler
		exchange.request.handleTimeout()
	
	def getStats():
        stats = {}
		stats["Request-Response exchanges"] = self.exchanges.size()
		stats["Messages sent"] = self.numMessagesSent
		stats["Messages received"] = self.numMessagesReceived
		
		return str(stats)