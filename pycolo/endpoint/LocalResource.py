# coding=utf-8
from pycolo.coap.CodeRegistry import CodeRegistry
from pycolo.endpoint import Resource


class LocalResource(Resource):
    """
    The class LocalResource provides the functionality of a CoAP server
    resource as a subclass of {@link Resource}. Implementations will inherit
    this class in order to provide custom resources by overriding some the
    following methods:
    <ul>
    <li>{@link #performGET(GETRequest)}
    <li>{@link #performPOST(POSTRequest)}
    <li>{@link #performPUT(PUTRequest)}
    <li>{@link #performDELETE(DELETERequest)}
    </ul>
    These methods are defined by the {@link RequestHandler} interface and have
    a default implementation in this class that responds with
    "4.05 Method Not Allowed."
     """

    @overloaded
    def __init__(self, hidden):
        super(LocalResource, self).__init__(hidden)

    @__init__.register(object, str)
    def __init___0(self):
        super(LocalResource, self).__init__(False)

    def changed(self):
        """
        Calling this method will notify all registered observers. Resources
        that use this method must also call {@link #isObservable(true)} so that
        clients will be registered after a successful GET with Observe option.
        """
        self.ObservingManager.getInstance().notifyObservers(self)

    def performGET(self, request):
        """ generated source for method performGET """
        request.respond(CodeRegistry.RESP_METHOD_NOT_ALLOWED)

    def performPUT(self, request):
        """ generated source for method performPUT """
        request.respond(CodeRegistry.RESP_METHOD_NOT_ALLOWED)

    def performPOST(self, request):
        """ generated source for method performPOST """
        request.respond(CodeRegistry.RESP_METHOD_NOT_ALLOWED)

    def performDELETE(self, request):
        """ generated source for method performDELETE """
        request.respond(CodeRegistry.RESP_METHOD_NOT_ALLOWED)

    def createSubResource(self, request):
        """
        Generally forbid the creation of new sub-resources.
        Override and define checks to allow creation.
        """
        request.respond(CodeRegistry.RESP_FORBIDDEN)
        request.sendResponse()
