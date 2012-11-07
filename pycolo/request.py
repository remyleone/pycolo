# coding=utf-8
import logging
import queue
import sys

from pycolo.message import Response, Message
from pycolo.codes import codes

class request(Message):
    """
    The Class Request describes the functionality of a CoAP Request as a subclass
    of a CoAP Message. It provides operations to answer a request by a Response
    using respond(Response). There are different ways to handle incoming
    responses:

        - by overriding the protected method {@link #handleResponse(Response)}, e.g.,
          using anonymous inner classes
        - by registering a handler using {@link #registerResponseHandler(ResponseHandler)}
        - by calling the blocking method {@link #receiveResponse()}

    """

    #  The Constant TIMEOUT_RESPONSE.
    #  TODO better solution?
    # TIMEOUT_RESPONSE = Response()

    #  The time when a request was issued to calculate Observe counter.
    # startTime = sys.currentTimeMillis()

    #  The list of response handlers that are notified about incoming responses
    # responseHandlers = list()

    #  The response queue filled by {@link #receiveResponse()}.
    # responseQueue = queue.Queue()
    # currentResponse = None

    #  The number of responses to this request.
    # responseCount = 0

    def __init__(self, method, confirmable=True):
        """
        Instantiates a new request.
        @param method The method code of the message
        @param confirmable True if the request is to be sent as a confirmable
        """
        raise NotImplementedError
#        self.confirmable = confirmable

    def execute(self):
        """
        Executes the request on the endpoint specified by the message's URI
        @throws IOException Signals that an I/O exception has occurred.
        """
        raise NotImplementedError
#        self.send()
#        #  TODO: LocalEndPoint stubs?

    def accept(self):
        """
        Overrides {@link Message#accept()} to keep track of the response
        count which is required to manage MIDs for exchanges over multiple
        transactions.
        """
        raise NotImplementedError
#        self.responseCount += 1
#        self.accept()

    def respond(self, response):
        """
        Issues a new response to this request
        @param response The response buddy for this request
        """
        raise NotImplementedError
#        #  assign response to this request
#        response.setRequest(self)
#        response.setPeerAddress(self.getPeerAddress())
#        #  set matching MID for replies
#        if self.responseCount == 0 and self.isConfirmable():
#            response.setMID(self.getMID())
#        #  set matching type
#        if response.getType() is None:
#            if self.responseCount == 0 and self.isConfirmable():
#                #  use piggy-backed response
#                response.setType(self.messageType.ACK)
#            else:
#                #  use separate response:
#                #  Confirmable response to confirmable request,
#                #  Non-confirmable response to non-confirmable request
#                response.setType(self.getType())
#        if response.getCode() != codes.EMPTY_MESSAGE:
#            #  Reflect token
#            response.setToken(self.getToken())
#            #  echo block1 option
#            if self.block1:
#                #  TODO: block1.setM(false); maybe in TransferLayer
#                response.addOption(self.block1)
#        else:
#            logging.critical("FIXME: Called with EMPTY MESSAGE")
#            #  FIXME Unsure about execution path, check
#        self.responseCount += 1
#        #  Endpoint will call sendResponse();
#        self.setResponse(response)

    def respond_0(self, code_, message, contentType):
        """
        Respond this request.
        @param code the status code
        @param message a string message
        @param contentType the Content-Type of the response
        """
        raise NotImplementedError
#        response = Response(code_)
#        if message:
#            response.setPayload(message)
#            response.setContentType(contentType)
#            logging.info("Responding with Content-Type {:d}: {:d} bytes".format(contentType, len(message)))
#        self.respond(response)


    def sendResponse(self):
        raise NotImplementedError
#        if self.currentResponse is not None:
#            if self.getPeerAddress() is not None:
#                self.currentResponse.send()
#            else:
#                #  handle locally
#                self.handleResponse(self.currentResponse)
#        else:
#            logging.warning("Missing response to send: Request {:s} for {:s}" % self.key(), self.getUriPath())


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
        raise NotImplementedError
#        #  response queue required to perform this operation
#        if not self.responseQueueEnabled():
#            logging.warning("Missing enableResponseQueue(true) call, responses may be lost")
#            self.enableResponseQueue(True)
#        #  take response from queue
#        response = self.responseQueue.take()
#        #  return null if request timed out
#        return response if response != self.TIMEOUT_RESPONSE else None


    def registerResponseHandler(self, handler):
        """
        Registers a handler for responses to this request.
        @param handler the handler to be added
        """
        raise NotImplementedError
#        if handler is not None:
#            #  lazy creation of response handler list
#            if self.responseHandlers is None:
#                self.responseHandlers = ArrayList()
#            self.responseHandlers.add(handler)


    def unregisterResponseHandler(self, handler):
        """
        Unregister response handler.
        @param handler the handler to be removed
        """
        raise NotImplementedError
#        if handler is not None and self.responseHandlers is not None:
#            self.responseHandlers.remove(handler)


    def enableResponseQueue(self, enable):
        """
        Enables or disables the response queue
        NOTE: The response queue needs to be enabled BEFORE any possible calls
        to {@link #receiveResponse()}.
        @param enable true to enable, false to disable
        """
        raise NotImplementedError
#        if enable != responseQueueEnabled():
#            self.responseQueue = LinkedBlockingQueue() if enable else None


    def responseQueueEnabled(self):
        """
        Checks if the response queue is enabled.
        @return true, if response queue is enabled
        """
        raise NotImplementedError
        # return self.responseQueue is not None


    def handleResponse(self, response):
        """
        This method is called whenever a response was placed to this request.
        Subclasses can override this method in order to handle responses.
        @param response the response
        """
        raise NotImplementedError
        #  enqueue response
#        if self.responseQueueEnabled():
#            if not self.responseQueue.offer(response):
#                logging.critical("ERROR: Failed to enqueue response to request")
#        #  notify response handlers
#        if self.responseHandlers is not None:
#            for handler in responseHandlers:
#                handler.handleResponse(response)


    def dispatch(self, handler):
        """
        Direct subclasses need to override this method in order to invoke the
        according method of the provided RequestHandler (visitor pattern)
        @param handler A handler for this request
        """
        raise NotImplementedError
        # logging.info("Cannot dispatch: {:s}".format(codes.toString(self.getCode())))

    def handleBy(self, handler):
        raise NotImplementedError
        # handler.handleRequest(self)

    def handleTimeout(self):
        """
        Message#handleTimeout()
        """
        raise NotImplementedError
#        if self.responseQueueEnabled():
#            self.responseQueue.offer(self.TIMEOUT_RESPONSE)


    def __str__(self):
        raise NotImplementedError
#        res = dict()
#        res["code"] = self.code
#        res["MID"] = self.MID
#        res["type"] = self.type
#        res["Content-Type"] = self.contentType


    def get(cls, param):
        """
        Shortcut to have a request GET
        :param cls:
        :param param:
        :return:
        """
        raise NotImplementedError


    def delete(self):
        """

        :raise:
        """
        raise NotImplementedError


    def put(self):
        """

        :raise:
        """
        raise NotImplementedError

    def post(self):
        """
        :raise:
        """
        raise NotImplementedError
