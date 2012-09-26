# coding=utf-8

import java.net.URI
import logging

#  * This class implements a simple CoAP client for testing purposes. Usage:
#  * <p>
#  * {@code java -jar SampleClient.jar [-l] METHOD URI [PAYLOAD]}
#  * <ul>
#  * <li>METHOD: {GET, POST, PUT, DELETE, DISCOVER, OBSERVE}
#  * <li>URI: The URI to the remote endpoint or resource}
#  * <li>PAYLOAD: The data to send with the request}
#  * </ul>
#  * Options:
#  * <ul>
#  * <li>-l: Loop for multiple responses}
#  * </ul>
#  * Examples:
#  * <ul>
#  * <li>{@code SampleClient DISCOVER coap://localhost}
#  * <li>{@code SampleClient POST coap://someServer.org:5683 my data}
#  * </ul>
#  *  
#  * @author Dominique Im Obersteg, Daniel Pauli, and Matthias Kovatsch


class ExampleClient():
    """ generated source for class ExampleClient """
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

    # 
    #      * Main method of this client.
    #      
    @classmethod
    def main(cls, args):
        """ generated source for method main """
        #  initialize parameters
        method = None
        uri = None
        payload = None
        loop = False
        #  display help if no parameters specified
        if len(args):
            printInfo()
            return
        Log.setLevel(Level.ALL)
        Log.init()
        #  input parameters
        idx = 0
        for arg in args:
            if arg.startsWith("-"):
                if arg == "-l":
                    loop = True
                else:
                    print 'Unrecognized option: ' + arg
            else:
                if idx == cls.IDX_METHOD:
                    method = arg.toUpperCase()
                elif idx == cls.IDX_URI:
                    try:
                        uri = URI(arg)
                    except URISyntaxException as e:
                        System.err.println("Failed to parse URI: " + e.getMessage())
                        System.exit(cls.ERR_BAD_URI)
                elif idx == cls.IDX_PAYLOAD:
                    payload = arg
                else:
                    print "Unexpected argument: " + arg
                idx += 1
        #  check if mandatory parameters specified
        if method == None:
            System.err.println("Method not specified")
            System.exit(cls.ERR_MISSING_METHOD)
        if uri == None:
            System.err.println("URI not specified")
            System.exit(cls.ERR_MISSING_URI)
        #  create request according to specified method
        request = newRequest(method)
        if request == None:
            System.err.println("Unknown method: " + method)
            System.exit(cls.ERR_UNKNOWN_METHOD)
        if method == "OBSERVE":
            request.setOption(Option(0, OptionNumberRegistry.OBSERVE))
            loop = True
        #  set request URI
        if method == "DISCOVER" and (uri.getPath() == None or uri.getPath().isEmpty() or uri.getPath() == "/"):
            #  add discovery resource path to URI
            try:
                uri = URI(uri.getScheme(), uri.getAuthority(), cls.DISCOVERY_RESOURCE, uri.getQuery())
            except URISyntaxException as e:
                System.err.println("Failed to parse URI: " + e.getMessage())
                System.exit(cls.ERR_BAD_URI)
        request.setURI(uri)
        request.setPayload(payload)
        request.setToken(TokenManager.getInstance().acquireToken())
        #  enable response queue in order to use blocking I/O
        request.enableResponseQueue(True)
        # 
        request.prettyPrint()
        #  execute request
        try:
            request.execute()
            #  loop for receiving multiple responses
            while True:
                #  receive response
                print "Receiving response..."
                try:
                    response = request.receiveResponse()
                except InterruptedException as e:
                    System.err.println("Failed to receive response: " + e.getMessage())
                    System.exit(cls.ERR_RESPONSE_FAILED)
                #  output response
                if response != None:
                    response.prettyPrint()
                    print "Time elapsed (ms): " + response.getRTT()
                    #  check of response contains resources
                    if response.getContentType() == MediaTypeRegistry.APPLICATION_LINK_FORMAT:
                        #  create resource three from link format
                        if root != None:
                            #  output discovered resources
                            print "\nDiscovered resources:"
                            root.prettyPrint()
                        else:
                            System.err.println("Failed to parse link format")
                            System.exit(cls.ERR_BAD_LINK_FORMAT)
                    else:
                        #  check if link format was expected by client
                        if method == "DISCOVER":
                            print
                            var = "Server error: Link format not specified"
                else:
                    #  no response received    
                    System.err.println("Request timed out")
                    break
                if not loop:
                    break
        except UnknownHostException as e:
            System.err.println("Unknown host: " + e.getMessage())
            System.exit(cls.ERR_REQUEST_FAILED)
        except IOException as e:
            System.err.println("Failed to execute request: " + e.getMessage())
            System.exit(cls.ERR_REQUEST_FAILED)
        #  finish
        print 

    # 
    #      * Outputs user guide of this program.
    #      
    @classmethod
    def printInfo(cls):
        """ generated source for method printInfo """
        print "Californium (Cf) Example Client"
        print "(c) 2012, Institute for Pervasive Computing, ETH Zurich"
        print 
        print "Usage: " + ExampleClient.__class__.getSimpleName() + " [-l] METHOD URI [PAYLOAD]"
        print "  METHOD  : {GET, POST, PUT, DELETE, DISCOVER, OBSERVE}"
        print "  URI     : The CoAP URI of the remote endpoint or resource"
        print "  PAYLOAD : The data to send with the request"
        print "Options:"
        print "  -l      : Loop for multiple responses"
        print "           (automatic for OBSERVE and separate responses)"
        print 
        print "Examples:"
        print "  ExampleClient DISCOVER coap://localhost"
        print
        var = "  ExampleClient POST coap://vs0.inf.ethz.ch:5683/storage my data"

    # 
    #      * Instantiates a new request based on a string describing a method.
    #      * 
    #      * @return A new request object, or null if method not recognized
    #      
    @classmethod
    def newRequest(cls, method):
        """ generated source for method newRequest """
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
    import sys
    ExampleClient.main(sys.argv)
