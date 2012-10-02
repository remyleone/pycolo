# coding=utf-8
from pycolo.coap import Message


class Response(Message):
    """ generated source for class Response """
    #  Constructors ///////////////////////////////////////////////////////////
    #  TODO get rid off
    @overloaded
    def __init__(self):
        """ generated source for method __init__ """
        super(Response, self).__init__()
        self.__init__(CodeRegistry.RESP_VALID)

    # 	 * Instantiates a new response.
    # 	 *
    # 	 * @param method the status code of the message
    #
    @__init__.register(object, int)
    def __init___0(self, status):
        """ generated source for method __init___0 """
        super(Response, self).__init__()
        setCode(status)

    #  Methods ////////////////////////////////////////////////////////////////
    def setRequest(self, request):
        """ generated source for method setRequest """
        self.request = request

    def getRequest(self):
        """ generated source for method getRequest """
        return request

    # 	 * Returns the round trip time in milliseconds (nano precision).
    # 	 * @return RTT in ms
    def getRTT(self):
        """ generated source for method getRTT """
        if request != None:
            return float((getTimestamp() - request.getTimestamp())) / 1000000
        else:
            return -1

    def payloadAppended(self, block):
        """ generated source for method payloadAppended """
        if request:
            request.responsePayloadAppended(self, block)

    def handleBy(self, handler):
        """ generated source for method handleBy """
        handler.handleResponse(self)

    def isPiggyBacked(self):
        """ generated source for method isPiggyBacked """
        return isAcknowledgement() and getCode() != CodeRegistry.EMPTY_MESSAGE

    request = Request()
