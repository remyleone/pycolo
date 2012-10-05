# coding=utf-8
import logging
import java.io.IOException
import java.util.ArrayList

import java.util.concurrent.BlockingQueue
import java.util.concurrent.LinkedBlockingQueue
from pycolo import Message, codes
from pycolo.Response import Response


class request(Message):
    """
    The Class Request describes the functionality of a CoAP Request as a subclass
    of a CoAP {@link Message}. It provides operations to answer a request by a {@link Response}
    using {@link #respond(Response)}. There are different ways to handle incoming
    responses:
    <ol>
    <li>by overriding the protected method {@link #handleResponse(Response)}, e.g.,
    using anonymous inner classes
    <li>by registering a handler using {@link #registerResponseHandler(ResponseHandler)}
    <li>by calling the blocking method {@link #receiveResponse()}
    </ol>
    """
    #  The Constant TIMEOUT_RESPONSE.
    #  TODO better solution?
    TIMEOUT_RESPONSE = Response()

    #  The time when a request was issued to calculate Observe counter.
    startTime = System.currentTimeMillis()

    #  The list of response handlers that are notified about incoming responses
    responseHandlers = list()

    #  The response queue filled by {@link #receiveResponse()}.
    responseQueue = BlockingQueue()
    currentResponse = None

    #  The number of responses to this request. 
    responseCount = 0

    def __init__(self, method, confirmable):
        """
        Instantiates a new request.
        @param method The method code of the message
        @param confirmable True if the request is to be sent as a confirmable
        """
        super(Request, self).__init__(method)

    def execute(self):
        """
        Executes the request on the endpoint specified by the message's URI
        @throws IOException Signals that an I/O exception has occurred.
        """
        self.send()
        #  TODO: LocalEndPoint stubs?

    def accept(self):
        """
        Overrides {@link Message#accept()} to keep track of the response
        count which is required to manage MIDs for exchanges over multiple
        transactions.
        """
        self.responseCount += 1
        super(Request, self).accept()

    def getResponse(self):
        return self.currentResponse

    def setResponse(self, response):
        self.currentResponse = response

    def respond(self, response):
        """
        Issues a new response to this request
        @param response The response buddy for this request
        """
        #  assign response to this request
        response.setRequest(self)
        response.setPeerAddress(self.getPeerAddress())
        #  set matching MID for replies
        if self.responseCount == 0 and self.isConfirmable():
            response.setMID(self.getMID())
        #  set matching type
        if response.getType() == None:
            if self.responseCount == 0 and self.isConfirmable():
                #  use piggy-backed response
                response.setType(self.messageType.ACK)
            else:
                #  use separate response:
                #  Confirmable response to confirmable request,
                #  Non-confirmable response to non-confirmable request
                response.setType(self.getType())
        if response.getCode() != codes.EMPTY_MESSAGE:
            #  Reflect token
            response.setToken(self.getToken())
            #  echo block1 option
            if self.block1:
                #  TODO: block1.setM(false); maybe in TransferLayer
                response.addOption(self.block1)
        else:
            logging.critical("FIXME: Called with EMPTY MESSAGE")
            #  FIXME Unsure about execution path, check
        self.responseCount += 1
        #  Endpoint will call sendResponse();
        self.setResponse(response)

    @respond.register(object, int, str, int)
    def respond_0(self, code_, message, contentType):
        """
        Respond this request.
        @param code the status code
        @param message a string message
        @param contentType the Content-Type of the response
        """
        response = Response(code_)
        if message:
            response.setPayload(message)
            response.setContentType(contentType)
            logging.info("Responding with Content-Type {:d}: {:d} bytes".format(contentType, len(message)))
        self.respond(response)

    @respond.register(object, int, str)
    def respond_1(self, code_, message):
        """
        Respond this request.
        @param code the status code
        @param message a string message
        """
        response = Response(code_)
        if message:
            response.setPayload(message)
        self.respond(response)

    @respond.register(object, int)
    def respond_2(self, code_):
        """
        Respond this request.
        @param code the status code
        """
        self.respond(code_, None)

    def sendResponse(self):
        if self.currentResponse != None:
            if self.getPeerAddress() != None:
                self.currentResponse.send()
            else:
                #  handle locally
                self.handleResponse(self.currentResponse)
        else:
            logging.warning("Missing response to send: Request {:s} for {:s}" % self.key(), self.getUriPath())

    def receiveResponse(self):
        """
        Returns a response that was placed using {@link #respond()} and blocks
        until such a response is available.
        NOTE: In order to safely use this method, the call
        {@link #enableResponseQueue(true)} is required BEFORE any possible
        {@link #respond()} calls take place.
        @return the next response in the queue
        @throws InterruptedException the interrupted exception
        """
        #  response queue required to perform this operation
        if not self.responseQueueEnabled():
            logging.warning("Missing enableResponseQueue(true) call, responses may be lost")
            self.enableResponseQueue(True)
        #  take response from queue
        response = self.responseQueue.take()
        #  return null if request timed out
        return response if response != self.TIMEOUT_RESPONSE else None

    def registerResponseHandler(self, handler):
        """
        Registers a handler for responses to this request.
        @param handler the handler to be added
        """
        if handler != None:
            #  lazy creation of response handler list
            if self.responseHandlers == None:
                self.responseHandlers = ArrayList()
            self.responseHandlers.add(handler)

    def unregisterResponseHandler(self, handler):
        """
        Unregister response handler.
        @param handler the handler to be removed
        """
        if handler != None and self.responseHandlers != None:
            self.responseHandlers.remove(handler)

    def enableResponseQueue(self, enable):
        """
        Enables or disables the response queue
        NOTE: The response queue needs to be enabled BEFORE any possible calls
        to {@link #receiveResponse()}.
        @param enable true to enable, false to disable
        """
        if enable != responseQueueEnabled():
            self.responseQueue = LinkedBlockingQueue() if enable else None

    def responseQueueEnabled(self):
        """
        Checks if the response queue is enabled.
        @return true, if response queue is enabled
        """
        return self.responseQueue != None

    def handleResponse(self, response):
        """
        This method is called whenever a response was placed to this request.
        Subclasses can override this method in order to handle responses.
        @param response the response
        """
        #  enqueue response
        if self.responseQueueEnabled():
            if not self.responseQueue.offer(response):
                logging.critical("ERROR: Failed to enqueue response to request")
        #  notify response handlers
        if self.responseHandlers != None:
            for handler in responseHandlers:
                handler.handleResponse(response)

    def responsePayloadAppended(self, response, block):
        """
        Response payload appended.
        @param response the response
        @param block the block
        """
        pass

    def responseCompleted(self, response):
        """
        do nothing
        """
        pass

    def dispatch(self, handler):
        """
        Direct subclasses need to override this method in order to invoke the
        according method of the provided RequestHandler (visitor pattern)
        @param handler A handler for this request
        """
        logging.info("Cannot dispatch: {:s}".format(CodeRegistry.toString(self.getCode())))

    def handleBy(self, handler):
        """ generated source for method handleBy """
        handler.handleRequest(self)

    def handleTimeout(self):
        """
        Message#handleTimeout()
        """
        if self.responseQueueEnabled():
            self.responseQueue.offer(self.TIMEOUT_RESPONSE)
