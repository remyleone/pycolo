# coding=utf-8
from pycolo import Message
from pycolo.codes import codes


class Response(Message):

    #  TODO get rid off

    def __init__(self, status):
        """
        Instantiates a new response.
        @param method the status code of the message
        """
        super(Response, self).__init__()
        self.__init__(codes.RESP_VALID)
        super(Response, self).__init__()
        self.code(status)


    def getRTT(self):
        """
        Returns the round trip time in milliseconds (nano precision).
        @return RTT in ms
        """
        if request:
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
        return self.isAcknowledgement() and self.code != codes.EMPTY_MESSAGE

    request = Request()
