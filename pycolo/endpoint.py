# coding=utf-8
import logging
import urllib
from pycolo.codes import codes, options
from pycolo.message import Response
from pycolo.observe import addObserver, isObserved

from pycolo.resource import Resource
from pycolo import DEFAULT_PORT, resource


class Endpoint:
    """
    The class LocalEndpoint provides the functionality of a server endpoint
    as a subclass of {@link Endpoint}. A server implementation using pycolo will
    override this class to provide custom resources. Internally, the main
    purpose of this class is to forward received requests to the corresponding
    resource specified by the URI-Path option. Furthermore, it implements the
    root resource to return a brief server description to GET requests with
    empty URI-Path.


    The abstract class Endpoint is the basis for the server-sided
    {@link LocalEndpoint} and the client-sided {@link RemoteEndpoint} skeleton.
    """

    greetings = """
                               _
         _ __  _   _  ___ ___ | | ___
        | '_ \| | | |/ __/ _ \| |/ _ \
        | |_) | |_| | (_| (_) | | (_) |
        | .__/ \__, |\___\___/|_|\___/
        |_|    |___/

    https://github.com/sieben/pycolo.
    """


    def search(self):
        """
        Search engine on a endpoint. Provide a simple query mechanisms.

        The following are examples of valid query URIs:
        - ?href=/foo* matches a link-value that is anchored at a URI that
        starts with /foo
        - ?foo=bar matches a link-value that has a target attribute named
        foo with the exact value bar
        - ?foo=bar* matches a link-value that has a target attribute named
        foo, the value of which starts with bar, e.g., bar or barley
        - ?href=/foo matches a link-value that is anchored at /foo
        - ?foo=* matches a link-value that has a target attribute named foo

        :return:
        """
        raise NotImplementedError

    def execute(self, request):
#        #  check if request exists
#        if request is not None:
#            #  retrieve resource identifier
#            #  lookup resource
#            #  check if resource available
#            if resource is not None:
#                logging.info("Dispatching execution: {:s}".format(resourcePath))
#                #  invoke request handler of the resource
#                request.dispatch(resource)
#                #  check if resource did generate a response
#                if request.getResponse() is not None:
#                    #  check if resource is to be observed
#                    if resource.isObservable() and isinstance(request, (GETRequest,)) and codes.responseClass(request.getResponse().getCode()) == codes.CLASS_SUCCESS:
#                        if request.hasOption(options.OBSERVE):
#                            #  establish new observation relationship
#                            addObserver(request, resource)
#                        elif isObserved(request.getPeerAddress().__str__(), resource):
#                            #  terminate observation relationship on that resource
#                            removeObserver(request.getPeerAddress().__str__(), resource)
#                            #  send response here
#                    request.sendResponse()
#            elif isinstance(request, (PUTRequest,)):
#                #  allows creation of non-existing resources through PUT
#                self.createByPUT(request)
#            else:
#                #  resource does not exist
#                logging.info("Cannot find resource: {:s}".format(resourcePath))
#                request.respond(codes.RESP_NOT_FOUND)
#                request.sendResponse()
        raise NotImplementedError

    def resourceCount(self):
        # return self.rootResource.subResourceCount() + 1 if self.rootResource is not None else 0
        raise NotImplementedError

    def receiveMessage(self, msg):
        # msg.handleBy(self)
        raise NotImplementedError

    def performGET(self, request):
#        #  create response
#        response = Response(codes.RESP_CONTENT)
#        response.setPayload(self.ENDPOINT_INFO)
#        #  complete the request
#        request.respond(response)
#        pass
        raise NotImplementedError

    def performPUT(self, request):
#        """
#        Delegates a {@link PUTRequest} for a non-existing resource to the
#        {@link LocalResource#createSubResource(Request, String)} method of the
#        first existing resource up the path.
#        @param request - the PUT request
#        """
#        path = request.getUriPath()
#        #  always starts with "/"
#        #  find existing parent up the path
#        parentIdentifier = str(path)
#        newIdentifier = ""
#        parent = None
#        #  will end at rootResource ("")
#        while True:
#            newIdentifier = path.substring(parentIdentifier.lastIndexOf('/') + 1)
#            parentIdentifier = parentIdentifier.substring(0, parentIdentifier.lastIndexOf('/'))
#            if not parent
#            = getResource(parentIdentifier)) == var = None
#            :
#            break
#            parent.createSubResource(request, newIdentifier)
        raise NotImplementedError


    def addResource(self, resource):
        """
        Adds a resource to the root resource of the endpoint. If the resource
        identifier is actually a path, it is split up into multiple resources.
        @param resource - the resource to add to the root resource
        """
#        if rootResource is not None:
#            rootResource.add(resource)
        raise NotImplementedError

    def removeResource(self, resourceIdentifier):
        """ generated source for method removeResource """
#        if rootResource is not None:
#            rootResource.removeSubResource(resourceIdentifier)
        raise NotImplementedError


    def getRootResource(self):
        """
        Provides access to the root resource that contains all local resources,
        e.g., for the surrounding server code to register at an RD.
        @return the root resource
        """
        #return self.rootResource
        raise NotImplementedError

    def __init__(self, address="coap://localhost", quiet=False, port=DEFAULT_PORT):
        """
        Instantiates a new endpoint address using the default port.
        A convenience constructor that takes the address information from a
        URI object.
        :type address: address of the endpoint
        """
#        if not quiet:
#            print(Endpoint.greetings)
#        self.address = urllib.parse(address).netloc
#        self.port = port
#        self.rootResource = self.RootResource()
#        self.addResource(DiscoveryResource(self.rootResource))
#        Communicator.setupTransfer(defaultBlockSze)
#        rootResource = Resource("root")

        raise NotImplementedError

    def register(self, res):
        raise NotImplementedError
