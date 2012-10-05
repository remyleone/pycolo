# coding=utf-8
import logging
import sys
import unittest

class ExampleClient:
    """
    This class implements a simple CoAP client for testing purposes.
    Usage: ExampleClient.__class__.getSimpleName() [-l] METHOD URI [PAYLOAD]
    METHOD  : {GET, POST, PUT, DELETE, DISCOVER, OBSERVE}
    URI     : The CoAP URI of the remote endpoint or resource
    PAYLOAD : The data to send with the request
    Options:
    -l      : Loop for multiple responses
    (automatic for OBSERVE and separate responses)
    Examples:
    ExampleClient DISCOVER coap://localhost
    ExampleClient POST coap://vs0.inf.ethz.ch:5683/storage my data
    """
    #  resource URI path used for discovery
    DISCOVERY_RESOURCE = "/.well-known/core"

    #  indices of command line parameters
    IDX_METHOD = 0
    IDX_URI = 1
    IDX_PAYLOAD = 2

    #  exit codes for runtime errors
    ERR_MISSING_METHOD = 1
    ERR_UNKNOWN_METHOD = 2
    ERR_MISSING_URI = 3
    ERR_BAD_URI = 4
    ERR_REQUEST_FAILED = 5
    ERR_RESPONSE_FAILED = 6
    ERR_BAD_LINK_FORMAT = 7

    @classmethod
    def main(cls, args):
        """ Main method of this client. """
        #  initialize parameters
        method = None
        uri = None
        payload = None
        loop = False
        #  display help if no parameters specified
        if len(args):
            print(__doc__)
            return
        #  input parameters
        idx = 0
        for arg in args:
            if arg.startsWith("-"):
                if arg == "-l":
                    loop = True
                else:
                    logging.info("Unrecognized option: " + arg)
            else:
                if idx == cls.IDX_METHOD:
                    method = arg.toUpperCase()
                elif idx == cls.IDX_URI:
                    try:
                        uri = URI(arg)
                    except URISyntaxException as e:
                        logging.critical("Failed to parse URI: " + e.getMessage())
                        sys.exit(cls.ERR_BAD_URI)
                elif idx == cls.IDX_PAYLOAD:
                    payload = arg
                else:
                    logging.info("Unexpected argument: " + arg)
                idx += 1
        #  check if mandatory parameters specified
        if method == None:
            logging.critical("Method not specified")
            sys.exit(cls.ERR_MISSING_METHOD)
        if uri == None:
            logging.critical("URI not specified")
            sys.exit(cls.ERR_MISSING_URI)
        #  create request according to specified method
        request = newRequest(method)
        if request == None:
            logging.critical("Unknown method: " + method)
            sys.exit(cls.ERR_UNKNOWN_METHOD)
        if method == "OBSERVE":
            request.setOption(Option(0, OptionNumberRegistry.OBSERVE))
            loop = True
        #  set request URI
        if method == "DISCOVER" and (uri.getPath() == None or uri.getPath().isEmpty() or uri.getPath() == "/"):
            #  add discovery resource path to URI
            try:
                uri = URI(uri.getScheme(), uri.getAuthority(), cls.DISCOVERY_RESOURCE, uri.getQuery())
            except URISyntaxException as e:
                logging.critical("Failed to parse URI: " + e.getMessage())
                sys.exit(cls.ERR_BAD_URI)
        request.uri = uri
        request.payload = payload
        request.setToken(TokenManager.getInstance().acquireToken())
        #  enable response queue in order to use blocking I/O
        request.enableResponseQueue(True)

        str(request)
        #  execute request
        try:
            request.execute()
            #  loop for receiving multiple responses
            while True:
                #  receive response
                logging.info("Receiving response...")
                try:
                    response = request.receiveResponse()
                except InterruptedException as e:
                    logging.critical("Failed to receive response: " + e.getMessage())
                    sys.exit(cls.ERR_RESPONSE_FAILED)
                #  output response
                if response != None:
                    response.prettyPrint()
                    print "Time elapsed (ms): " + response.getRTT()
                    #  check of response contains resources
                    if response.getContentType() == MediaTypeRegistry.APPLICATION_LINK_FORMAT:
                        #  create resource three from link format
                        if root:
                            #  output discovered resources
                            print "\nDiscovered resources:"
                            root.prettyPrint()
                        else:
                            logging.critical("Failed to parse link format")
                            sys.exit(cls.ERR_BAD_LINK_FORMAT)
                    else:
                        #  check if link format was expected by client
                        if method == "DISCOVER":
                            print "Server error: Link format not specified"
                else:
                    #  no response received	
                    logging.critical("Request timed out")
                    break
                if not ((loop)):
                    break
        except UnknownHostException as e:
            logging.critical("Unknown host: " + e.getMessage())
            sys.exit(cls.ERR_REQUEST_FAILED)
        except IOException as e:
            logging.critical("Failed to execute request: " + e.getMessage())
            sys.exit(cls.ERR_REQUEST_FAILED)


    @classmethod
    def newRequest(cls, method):
        """
        Instantiates a new request based on a string describing a method.
        @return A new request object, or null if method not recognized
        """
        if method == "GET":
            return GETRequest()
        elif method == "POST":
            return POSTRequest()
        elif method == "PUT":
            return PUTRequest()
        elif method == "DELETE":
            return DELETERequest()
        elif method == "DISCOVER":
            return GETRequest()
        elif method == "OBSERVE":
            return GETRequest()
        else:
            return None


if __name__ == '__main__':
    unittest.main()