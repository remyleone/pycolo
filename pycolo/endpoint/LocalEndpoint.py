# -*- coding:utf-8 -*-

from pycolo.coap.CodeRegistry import CodeRegistry
from pycolo.coap import Communicator
from pycolo.coap import GETRequest
from pycolo.coap import ObservingManage
from pycolo.coap.OptionNumberRegistry import OptionNumberRegistry
from pycolo.coap import PUTRequest
from pycolo.coap import Response
from pycolo.endpoint import Endpoint
from pycolo import DEFAULT_PORT


class LocalEndpoint(Endpoint):
    """
    The class LocalEndpoint provides the functionality of a server endpoint
    as a subclass of {@link Endpoint}. A server implementation using Cf will
    override this class to provide custom resources. Internally, the main
    purpose of this class is to forward received requests to the corresponding
    resource specified by the URI-Path option. Furthermore, it implements the
    root resource to return a brief server description to GET requests with
    empty URI-Path.
    """
    ENDPOINT_INFO = "************************************************************\n" + "This server is using the Californium (Cf) CoAP framework\n" + "developed by Dominique Im Obersteg, Daniel Pauli, and\n" + "Matthias Kovatsch.\n" + "Cf is available under BSD 3-clause license on GitHub:\n" + "https://github.com/mkovatsc/Californium\n" + "\n" + "(c) 2012, Institute for Pervasive Computing, ETH Zurich\n" + "Contact: Matthias Kovatsch <kovatsch@inf.ethz.ch>\n" + "************************************************************"

    class RootResource(LocalResource):
        """ generated source for class RootResource """
        def __init__(self):
            """ generated source for method __init__ """
            super(RootResource, self).__init__(True)

        def performGET(self, request):
            """ generated source for method performGET """
            #  create response
            response = Response(CodeRegistry.RESP_CONTENT)
            response.setPayload(self.ENDPOINT_INFO)
            #  complete the request
            request.respond(response)

    #TODO Constructor with custom root resource; check for resourceIdentifier==""
    @overloaded
    def __init__(self, port, defaultBlockSze, daemon):
        """ generated source for method __init__ """
        super(LocalEndpoint, self).__init__()
        #  initialize communicator
        Communicator.setupPort(port)
        Communicator.setupTransfer(defaultBlockSze)
        Communicator.setupDeamon(daemon)
        Communicator.getInstance().registerReceiver(self)
        #  initialize resources
        self.rootResource = self.RootResource()
        self.addResource(DiscoveryResource(self.rootResource))

    @__init__.register(object, int, int)
    def __init___0(self, port, defaultBlockSze):
        """ generated source for method __init___0 """
        super(LocalEndpoint, self).__init__()
        self.__init__(port, defaultBlockSze, False)
        #  no daemon, keep JVM running to handle requests

    @__init__.register(object, int)
    def __init___1(self, port):
        """ generated source for method __init___1 """
        super(LocalEndpoint, self).__init__()
        self.__init__(port, 0)
        #  let TransferLayer decide default

    @__init__.register(object)
    def __init___2(self):
        """ generated source for method __init___2 """
        super(LocalEndpoint, self).__init__()
        self.__init__(DEFAULT_PORT)

    def execute(self, request):
        """ generated source for method execute """
        #  check if request exists
        if request != None:
            #  retrieve resource identifier
            #  lookup resource
            #  check if resource available
            if resource != None:
                LOG.info("Dispatching execution: {:s}".format(resourcePath))
                #  invoke request handler of the resource
                request.dispatch(resource)
                #  check if resource did generate a response
                if request.getResponse() != None:
                    #  check if resource is to be observed
                    if resource.isObservable() and isinstance(request, (GETRequest,)) and CodeRegistry.responseClass(request.getResponse().getCode()) == CodeRegistry.CLASS_SUCCESS:
                        if request.hasOption(OptionNumberRegistry.OBSERVE):
                            #  establish new observation relationship
                            ObservingManager.getInstance().addObserver(request, resource)
                        elif ObservingManager.getInstance().isObserved(request.getPeerAddress().__str__(), resource):
                            #  terminate observation relationship on that resource
                            ObservingManager.getInstance().removeObserver(request.getPeerAddress().__str__(), resource)
                    #  send response here
                    request.sendResponse()
            elif isinstance(request, (PUTRequest,)):
                #  allows creation of non-existing resources through PUT
                self.createByPUT(request)
            else:
                #  resource does not exist
                LOG.info("Cannot find resource: {:s}".format(resourcePath))
                request.respond(CodeRegistry.RESP_NOT_FOUND)
                request.sendResponse()

    #
    # 	 * Delegates a {@link PUTRequest} for a non-existing resource to the
    # 	 * {@link LocalResource#createSubResource(Request, String)} method of the
    # 	 * first existing resource up the path.
    # 	 *
    # 	 * @param request - the PUT request
    #
    def createByPUT(self, request):
        """ generated source for method createByPUT """
        path = request.getUriPath()
        #  always starts with "/"
        #  find existing parent up the path
        parentIdentifier = str(path)
        newIdentifier = ""
        parent = None
        #  will end at rootResource ("")
        while True:
            newIdentifier = path.substring(parentIdentifier.lastIndexOf('/') + 1)
            parentIdentifier = parentIdentifier.substring(0, parentIdentifier.lastIndexOf('/'))
            if not parent
 = getResource(parentIdentifier)) == var = None
            :
                break
        parent.createSubResource(request, newIdentifier)

    def getResource(self, resourcePath):
        """ generated source for method getResource """
        if rootResource != None:
            return rootResource.getResource(resourcePath)
        else:
            return None

    def addResource(self, resource):
        """
        Adds a resource to the root resource of the endpoint. If the resource
        identifier is actually a path, it is split up into multiple resources.
        @param resource - the resource to add to the root resource
        """
        if rootResource != None:
            rootResource.add(resource)

    def removeResource(self, resourceIdentifier):
        """ generated source for method removeResource """
        if rootResource != None:
            rootResource.removeSubResource(resourceIdentifier)

    def handleRequest(self, request):
        """ generated source for method handleRequest """
        self.execute(request)

    def handleResponse(self, response):
        """ generated source for method handleResponse """
        #  response.handle();

    def getRootResource(self):
        """
        Provides access to the root resource that contains all local resources,
        e.g., for the surrounding server code to register at an RD.
        @return the root resource
        """
        return self.rootResource
