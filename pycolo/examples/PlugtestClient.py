# coding=utf-8

import logging
from pycolo.endpoint import Resource


class PlugtestClient:

    PLUGTEST_BLOCK_SIZE = 64

    serverURI = None
    testMap = dict()
    testsToRun = list()  # The test list.
    summary = list()  # The test summary.

    /** 
     * Default constructor. Loads with reflection each nested class that is a
     * derived type of TestClientAbstract.
     * 
     * @param serverURI
     * the server uri
     */ 
    public PlugtestClient(String serverURI) {
        if (serverURI == null || serverURI.isEmpty()) {
            logging.critical("serverURI == null || serverURI.isEmpty()");
            throw new IllegalArgumentException("serverURI == null || serverURI.isEmpty()");
        }
        this.serverURI = serverURI;

        # fill the map with each nested class not abstract that instantiate
        # TestClientAbstract
        for (Class < ? > clientTest : this.getClass().getDeclaredClasses()) {
            if (! Modifier.isAbstract(clientTest.getModifiers()) && (clientTest.getSuperclass() == TestClientAbstract.class)) {

                this.testMap.put(clientTest.getSimpleName(), clientTest);
            }
        }

        # DEBUG logging.info(this.testMap.size());
    }

    /** 
     * Instantiates the given testNames or if null all tests implemented.
     * 
     * @param testNames
     * the test names
     */ 
    public void instantiateTests(String... testNames) {

        testsToRun = Arrays.asList((testNames == null || testNames.length == 0) ? this.testMap.keySet().toArray(testNames) : testNames);
        Collections.sort(testsToRun);

        try {
            # iterate for each chosen test
            for (String testString : testsToRun) {
                # DEBUG logging.info(testString);

                # get the corresponding class
                Class < ? > testClass = this.testMap.get(testString);
                if (testClass == null) {
                    logging.critical("testClass == null")
                    sys.exit(-1)
                }

                # get the unique constructor
                Constructor < ? > [] constructors = testClass.getDeclaredConstructors();

                if (constructors.length == 0) {
                    logging.critical("constructors.length == 0");
                    sys.exit(-1);
                }

                # inner class: first argument (this) is the enclosing instance
                @SuppressWarnings("unused")
                    TestClientAbstract testClient = (TestClientAbstract) constructors[0].newInstance(this, serverURI);
            }

            waitForTests();

            # summary
            logging.info("\n==== SUMMARY ====");
            for (String result : summary) {
                logging.info(result);
            }

        } catch (InstantiationException e) {
            logging.critical("Reflection error");
            e.printStackTrace();
        } catch (IllegalAccessException e) {
            logging.critical("Reflection error");
            e.printStackTrace();
        } catch (IllegalArgumentException e) {
            logging.critical("Reflection error");
            e.printStackTrace();
        } catch (SecurityException e) {
            logging.critical("Reflection error");
            e.printStackTrace();
        } catch (InvocationTargetException e) {
            logging.critical("Reflection error");
            e.printStackTrace();
        } catch (InterruptedException e) {
            logging.critical("Concurrency error");
            e.printStackTrace();
        }
    }
    /* 
        public synchronized void waitForTests() throws InterruptedException {
        while (summary.size() < testsToRun.size()) {
        wait();
        }
        }

        public synchronized void tickOffTest() {
        notify();
        }

        public synchronized void addSummaryEntry(String entry) {
        summary.add(entry);
        }
     * / 
    /** 
     * Main entry point.
     * 
     * @param args
     * the arguments
     */ 
    public static void main(String[] args) {
        if (args.length == 0 || ! args[0].startsWith("coap://")) {
            logging.info("Californium (Cf) Plugtest Client");
            logging.info("(c) 2012, Institute for Pervasive Computing, ETH Zurich");
            logging.info();
            logging.info("Usage: " + PlugtestClient.class.getSimpleName() + " URI [TESTNAMES...]");
            logging.info("  URI       : The CoAP URI of the Plugtest server to test (coap://...)");
            logging.info("  TESTNAMES : A list of specific tests to run, omit to run all");
            logging.info();
            logging.info("Available tests:");
            System.out.print(" ");
            for (Class < ? > clientTest : PlugtestClient.class.getDeclaredClasses()) {
                if (! Modifier.isAbstract(clientTest.getModifiers()) && (clientTest.getSuperclass() == TestClientAbstract.class)) {
                    System.out.print(" " + clientTest.getSimpleName());
                }
            }
            sys.exit(-1);
        }

        Log.setLevel(Level.WARNING);
        Log.init();

        # default block size
        Communicator.setupTransfer(PLUGTEST_BLOCK_SIZE);

        # create the factory with the given server URI
        PlugtestClient clientFactory = new PlugtestClient(args[0]);

        # instantiate the chosen tests
        clientFactory.instantiateTests(Arrays.copyOfRange(args, 1, args.length));
    }

    /** 
     * Abstract class to support various test client implementations.
     * 
     * @author Francesco Corazza
     */ 
    public abstract class TestClientAbstract {
        testName = None
        verbose = False

        /** Use synchronous or asynchronous requests. Sync recommended due to single threaded servers and slow resources. * / 
        protected boolean sync = true;

        /** 
         * Instantiates a new test client abstract.
         * 
         * @param testName
         * the test name
         * @param verbose
         * the verbose
         */ 
        public TestClientAbstract(String testName, boolean verbose, boolean synchronous) {
            if (testName == null || testName.isEmpty()) {
                throw new IllegalArgumentException("testName == null || testName.isEmpty()");
            }

            this.testName = testName;
            this.verbose = verbose;
            this.sync = synchronous;
        }

        /** 
         * Instantiates a new test client abstract.
         * 
         * @param testName
         * the test name
         */ 
        public TestClientAbstract(String testName) {
            this(testName, false, true);
        }

        /** 
         * Execute request.
         * 
         * @param request
         * the request
         * @param serverURI
         * the server uri
         * @param resourceUri
         * the resource uri
         * @param payload
         * the payload
         */ 
        /* 
           protected synchronized void executeRequest(Request request, String serverURI, String resourceUri) {
           if (serverURI == null || serverURI.isEmpty()) {
           logging.critical("serverURI == null || serverURI.isEmpty()");
           throw new IllegalArgumentException("serverURI == null || serverURI.isEmpty()");
           }

        # defensive check for slash
        if (! serverURI.endsWith("/") && ! resourceUri.startsWith("/")) {
        resourceUri = "/" + resourceUri;
        }

        URI uri = null;
        try {
        uri = new URI(serverURI + resourceUri);
        } catch (URISyntaxException use) {
        logging.critical("Invalid URI: " + use.getMessage());
        # TODO
        }

        request.setURI(uri);
        if (request.requiresToken()) {
        request.setToken(TokenManager.getInstance().acquireToken());
        }

        request.registerResponseHandler(new TestResponseHandler());

        # enable response queue for synchronous I / O
        if (sync) {
        request.enableResponseQueue(true);
        }

        # print request info
        if (verbose) {
        logging.info("Request for test " + this.testName + " sent");
        str(request)
        }

        # execute the request
        try {
        request.execute();
        if (sync) {
        request.receiveResponse();
        }
        } catch (IOException e) {
        logging.critical("Failed to execute request: " + e.getMessage());
        sys.exit(-1);
        } catch (InterruptedException e) {
        logging.critical("Interupted during receive: " + e.getMessage())
        sys.exit(-1)
        }
        }
         * / 
        /** 
         * The Class TestResponseHandler.
         * / 
        protected class TestResponseHandler implements ResponseHandler {

            /** 
             * @see ch.ethz.inf.vs.californium.coap.ResponseHandler#handleResponse(ch.ethz.inf.vs.californium.coap.Response)
             */ 
            @Override
                public void handleResponse(Response response) {

                    logging.info();
                    logging.info("**** TEST: " + testName + " ****");

                    # checking the response
                    if (response != null) {

                        # print response info
                        if (verbose) {
                            logging.info("Response received");
                            logging.info("Time elapsed (ms): "
                                    + response.getRTT());
                            response.prettyPrint();
                        }

                        logging.info("**** BEGIN CHECK ****");

                        if (checkResponse(response.getRequest(), response)) {
                            logging.info("**** TEST PASSED ****");
                            addSummaryEntry(testName + ": PASSED");
                        } else {
                            logging.info("**** TEST FAILED ****");
                            addSummaryEntry(testName + ": FAILED");
                        }

                        tickOffTest();
                    }

                }
        }

        /** 
         * Check response.
         * 
         * @param request
         * the request
         * @param response
         * the response
         * @return true, if successful
         */ 
        protected abstract boolean checkResponse(Request request, Response response);

        /** 
         * Check int.
         * 
         * @param expected
         * the expected
         * @param actual
         * the actual
         * @param fieldName
         * the field name
         * @return true, if successful
         */ 
        protected boolean checkInt(int expected, int actual, String fieldName) {
            boolean success = expected == actual;

            if (! success) {
                logging.info("FAIL: Expected " + fieldName + ": " + expected + ", but was: " + actual);
            } else {
                logging.info("PASS: Correct " + fieldName + String.format(" (%d)", actual));
            }

            return success;
        }

        /** 
         * Check type.
         * 
         * @param expectedMessageType
         * the expected message type
         * @param actualMessageType
         * the actual message type
         * @return true, if successful
         */ 
        protected boolean checkType(Message.messageType expectedMessageType, Message.messageType actualMessageType) {
            boolean success = expectedMessageType.equals(actualMessageType);

            if (! success) {
                logging.info("FAIL: Expected type %s, but was %s\n", expectedMessageType, actualMessageType);
            } else {
                logging.info("PASS: Correct type (%s)\n", actualMessageType.toString());
            }

            return success;
        }

        /** 
         * Checks for Content - Type option.
         * 
         * @param response
         * the response
         * @return true, if successful
         */ 
        protected boolean hasContentType(Response response) {
            boolean success = response.hasOption(OptionNumberRegistry.CONTENT_TYPE);

            if (! success) {
                logging.info("FAIL: Response without Content-Type");
            } else {
                logging.info("PASS: Content-Type (%s)\n", MediaTypeRegistry.toString(response.getContentType()));
            }

            return success;
        }

        def hasLocation(response):
            """
            Checks for Location option.
            @param response the response
            @return true, if successful
            """
            success = response.hasOption(OptionNumberRegistry.LOCATION_PATH)

            if not success:
                logging.info("FAIL: Response without Location")
            else:
                logging.info("PASS: Location (%s)\n", response.getLocationPath())

            return success

        /** 
         * Checks for Observe option.
         * 
         * @param response
         * the response
         * @return true, if successful
         */ 
        protected boolean hasObserve(Response response, boolean invert) {
            boolean success = response.hasOption(OptionNumberRegistry.OBSERVE);

            # invert to check for not having the option
            success ^= invert;

            if (! success) {
                logging.info("FAIL: Response without Observe");
            } else if (! invert) {
                logging.info("PASS: Observe (%d)\n", response.getFirstOption(OptionNumberRegistry.OBSERVE).getIntValue());
            } else {
                logging.info("PASS: No Observe");
            }

            return success;
        }
        protected boolean hasObserve(Response response) {
            return hasObserve(response, false);
        }

        protected boolean checkOption(Option expextedOption, Option actualOption) {
            success = actualOption and expextedOption.optionNumber == actualOption.optionNumber

            if not success:
                logging.info("FAIL: Missing option nr %d\n", expextedOption.optionNumber);
            } else {

                # raw value byte array can be different, although value is the same 
                success &= expextedOption.toString().equals(actualOption.toString());

                if (! success) {
                    logging.info("FAIL: Expected %s, but was %s\n", expextedOption.toString(), actualOption.toString());
                } else {
                    logging.info("PASS: Correct option (%s)\n", actualOption.toString());
                }
            }

            return success;
        }

        /** 
         * Check token.
         * 
         * @param expectedToken the expected token
         * @param actualToken the actual token
         * @return true, if successful
         */ 
        protected boolean checkToken(Option expextedOption, Option actualOption) {
            success = True

            if (expextedOption.equals(new Option(TokenManager.emptyToken, OptionNumberRegistry.TOKEN))) {

                success = actualOption == null;

                if (! success) {
                    logging.info("FAIL: Expected empty token, but was %s" % actualOption)
                } else {
                    logging.info("PASS: Correct empty token")
                }

                return success;

            } else {

                success = actualOption.getRawValue().length <= 8
                success &= actualOption.getRawValue().length >= 1

                # eval token length
                if (! success) {
                    logging.info("FAIL: Expected token %s, but %s has illeagal length" % expextedOption, actualOption);
                    return success
                }

                success &= expextedOption.toString().equals(actualOption.toString());

                if (! success) {
                    logging.info("FAIL: Expected token %s, but was %s\n", expextedOption, actualOption);
                } else {
                    logging.info("PASS: Correct token (%s)\n", actualOption);
                }

                return success;
            }
        }

        def checkDiscovery(expextedAttribute, actualDiscovery):
            """
            Check discovery.
            @param expextedAttribute the resource attribute to filter
            @param actualDiscovery the reported Link Format
            @return true, if successful
            """

            Resource res = RemoteResource.newRoot(actualDiscovery);

            List < Option > query = new ArrayList < Option > ();
            query.add(new Option(expextedAttribute, OptionNumberRegistry.URI_QUERY));

            boolean success = true;

            for sub in res.getSubResources():
                success &= LinkFormat.matches(sub, query)

                if not success:
                    logging.info("FAIL: Expected %s, but was %s\n", expextedAttribute, LinkFormat.serialize(sub, null, false));

            if success:
                logging.info("PASS: Correct Link Format filtering")

            return success


    class CC01(TestClientAbstract):
        """
        TD_COAP_CORE_01:
        Perform GET transaction (CON mode).
        """

        RESOURCE_URI = "/test"
        EXPECTED_RESPONSE_CODE = 69

        public CC01(String serverURI) {
            super(CC01.class.getSimpleName());

            # create the request
            Request request = new GETRequest();

            # set the parameters and execute the request
            executeRequest(request, serverURI, RESOURCE_URI);
        }

        protected boolean checkResponse(Request request, Response response) {
            boolean success = true;

            success &= checkType(Message.messageType.ACK, response.getType());
            success &= checkInt(EXPECTED_RESPONSE_CODE, response.getCode(), "code");
            success &= checkInt(request.getMID(), response.getMID(), "MID");
            success &= hasContentType(response);

            return success;
        }
    }

    class CC02(TestClientAbstract):
        """
        TD_COAP_CORE_02:
        Perform POST transaction (CON mode).
        """

        public static final String RESOURCE_URI = "/test";
        EXPECTED_RESPONSE_CODE = 65;

        public CC02(String serverURI) {
            super(CC02.class.getSimpleName());

            # create the request
            Request request = new POSTRequest();
            # add payload
            request.setPayload("TD_COAP_CORE_02", MediaTypeRegistry.TEXT_PLAIN);
            # set the parameters and execute the request
            executeRequest(request, serverURI, RESOURCE_URI);
        }

        protected boolean checkResponse(Request request, Response response) {
            success = True

            success &= checkType(Message.messageType.ACK, response.getType())
            success &= checkInt(EXPECTED_RESPONSE_CODE, response.getCode(), "code")
            success &= checkInt(request.getMID(), response.getMID(), "MID")
            
            return success
        }
    }

    class CC03(TestClientAbstract):
        """
        TD_COAP_CORE_03:
        Perform PUT transaction (CON mode).
        """

        RESOURCE_URI = "/test"
        EXPECTED_RESPONSE_CODE = 68

        public CC03(String serverURI) {
            super(CC03.class.getSimpleName());

            # create the request
            Request request = new PUTRequest();
            # add payload
            request.setPayload("TD_COAP_CORE_02", MediaTypeRegistry.TEXT_PLAIN);
            # set the parameters and execute the request
            executeRequest(request, serverURI, RESOURCE_URI);
        }

        protected boolean checkResponse(Request request, Response response) {
            success = True

            success &= checkType(Message.messageType.ACK, response.getType());
            success &= checkInt(EXPECTED_RESPONSE_CODE, response.getCode(), "code");
            success &= checkInt(request.getMID(), response.getMID(), "MID");

            return success;
        }
    }

    class CC04(TestClientAbstract):
        """
        TD_COAP_CORE_04:
        Perform DELETE transaction (CON mode).
        """

        RESOURCE_URI = "/test"
        EXPECTED_RESPONSE_CODE = 66

        public CC04(String serverURI) {
            super(CC04.class.getSimpleName());

            # create the request
            Request request = new DELETERequest();
            # set the parameters and execute the request
            executeRequest(request, serverURI, RESOURCE_URI);
        }

        protected boolean checkResponse(Request request, Response response) {
            boolean success = true;

            success &= checkType(Message.messageType.ACK, response.getType());
            success &= checkInt(EXPECTED_RESPONSE_CODE, response.getCode(), "code");
            success &= checkInt(request.getMID(), response.getMID(), "MID");

            return success;
        }
    }

    class CC05(TestClientAbstract):
        """
        TD_COAP_CORE_05:
        Perform GET transaction (NON mode).
        """

        RESOURCE_URI = "/test"
        EXPECTED_RESPONSE_CODE = 69

        public CC05(String serverURI) {
            super(CC05.class.getSimpleName());

            # create the request
            Request request = new Request(CodeRegistry.METHOD_GET, false);
            # set the parameters and execute the request
            executeRequest(request, serverURI, RESOURCE_URI);
        }

        protected boolean checkResponse(Request request, Response response) {
            boolean success = true;

            success &= checkType(Message.messageType.NON, response.getType());
            success &= checkInt(EXPECTED_RESPONSE_CODE, response.getCode(), "code");
            success &= hasContentType(response);

            return success;
        }
    }

    class CC06(TestClientAbstract):
        """
        TD_COAP_CORE_06:
        Perform POST transaction (NON mode).
        """

        RESOURCE_URI = "/test"
        EXPECTED_RESPONSE_CODE = 65

        public CC06(String serverURI) {
            super(CC06.class.getSimpleName());

            # create the request
            Request request = new Request(CodeRegistry.METHOD_POST, false);
            # add payload
            request.setPayload("TD_COAP_CORE_06", MediaTypeRegistry.TEXT_PLAIN);
            # set the parameters and execute the request
            executeRequest(request, serverURI, RESOURCE_URI);
        }

        protected boolean checkResponse(Request request, Response response) {
            boolean success = true;

            success &= checkType(Message.messageType.NON, response.getType());
            success &= checkInt(EXPECTED_RESPONSE_CODE, response.getCode(), "code");

            return success;
        }
    }

    class CC07(TestClientAbstract):
        """
        TD_COAP_CORE_07:
        Perform PUT transaction (NON mode).
        """
        RESOURCE_URI = "/test"
        EXPECTED_RESPONSE_CODE = 68

        public CC07(String serverURI) {
            super(CC07.class.getSimpleName());

            # create the request
            Request request = new Request(CodeRegistry.METHOD_PUT, false);
            # add payload
            request.setPayload("TD_COAP_CORE_07", MediaTypeRegistry.TEXT_PLAIN);
            # set the parameters and execute the request
            executeRequest(request, serverURI, RESOURCE_URI);
        }

        protected boolean checkResponse(Request request, Response response) {
            boolean success = true;

            success &= checkType(Message.messageType.NON, response.getType());
            success &= checkInt(EXPECTED_RESPONSE_CODE, response.getCode(), "code");

            return success;
        }
    }

    class CC08(TestClientAbstract):
        """
        TD_COAP_CORE_08:
        Perform DELETE transaction (NON mode).
        """

        RESOURCE_URI = "/test"
        EXPECTED_RESPONSE_CODE = 66

        public CC08(String serverURI) {
            super(CC08.class.getSimpleName());

            # create the request
            Request request = new Request(CodeRegistry.METHOD_DELETE, false);
            # set the parameters and execute the request
            executeRequest(request, serverURI, RESOURCE_URI);
        }

        protected boolean checkResponse(Request request, Response response) {
            boolean success = true;

            success &= checkType(Message.messageType.NON, response.getType());
            success &= checkInt(EXPECTED_RESPONSE_CODE, response.getCode(), "code");

            return success;
        }
    }

    class CC09(TestClientAbstract):
        """
        TD_COAP_CORE_09:
        Perform GET transaction with delayed response (CON mode, no piggyback).
        """

        RESOURCE_URI = "/separate"
        EXPECTED_RESPONSE_CODE = 69

        public CC09(String serverURI) {
            super(CC09.class.getSimpleName());

            # create the request
            Request request = new Request(CodeRegistry.METHOD_GET, true);
            # set the parameters and execute the request
            executeRequest(request, serverURI, RESOURCE_URI);
        }

        protected boolean checkResponse(Request request, Response response) {
            boolean success = true;

            success &= checkType(Message.messageType.CON, response.getType());
            success &= checkInt(EXPECTED_RESPONSE_CODE, response.getCode(), "code");
            success &= hasContentType(response);

            return success;
        }
    }

    class CC10(TestClientAbstract):
        """
        TD_COAP_CORE_10:
        Handle request containing Token option.
        """

        RESOURCE_URI = "/test"
        EXPECTED_RESPONSE_CODE = 69

        public CC10(String serverURI) {
            super(CC10.class.getSimpleName());

            # create the request
            Request request = new Request(CodeRegistry.METHOD_GET, true);
            request.setToken(TokenManager.getInstance().acquireToken(false)); # not preferring empty token
            # set the parameters and execute the request
            executeRequest(request, serverURI, RESOURCE_URI);
        }

        protected boolean checkResponse(Request request, Response response) {
            boolean success = true;

            success &= checkType(Message.messageType.ACK, response.getType());
            success &= checkInt(EXPECTED_RESPONSE_CODE, response.getCode(), "code");
            success &= checkToken(request.getFirstOption(OptionNumberRegistry.TOKEN), response.getFirstOption(OptionNumberRegistry.TOKEN));
            success &= hasContentType(response);

            return success;
        }
    }

    class CC11(TestClientAbstract):
        """
        TD_COAP_CORE_11:
        Handle request not containing Token option.
        """

        public static final String RESOURCE_URI = "/test";
        EXPECTED_RESPONSE_CODE = 69;

        public CC11(String serverURI) {
            super(CC11.class.getSimpleName());

            # create the request
            Request request = new Request(CodeRegistry.METHOD_GET, true);
            request.setToken(TokenManager.getInstance().acquireToken(true));
            # set the parameters and execute the request
            executeRequest(request, serverURI, RESOURCE_URI);
        }

        protected boolean checkResponse(Request request, Response response) {
            boolean success = true;

            success &= checkType(Message.messageType.ACK, response.getType());
            success &= checkInt(EXPECTED_RESPONSE_CODE, response.getCode(), "code");
            success &= checkToken(new Option(TokenManager.emptyToken, OptionNumberRegistry.TOKEN), response.getFirstOption(OptionNumberRegistry.TOKEN));
            success &= hasContentType(response);

            return success;
        }
    }

    class CC12(TestClientAbstract):
        """
        TD_COAP_CORE_12:
        Handle request containing several Uri - Path options.
        """

        RESOURCE_URI = "/seg1/seg2/seg3"
        EXPECTED_RESPONSE_CODE = 69

        public CC12(String serverURI) {
            super(CC12.class.getSimpleName());

            # create the request
            Request request = new Request(CodeRegistry.METHOD_GET, true);
            # set the parameters and execute the request
            executeRequest(request, serverURI, RESOURCE_URI);
        }

        protected boolean checkResponse(Request request, Response response) {
            boolean success = true;

            success &= checkType(Message.messageType.ACK, response.getType());
            success &= checkInt(EXPECTED_RESPONSE_CODE, response.getCode(), "code");
            success &= hasContentType(response);

            return success;
        }
    }

    class CC13(TestClientAbstract):
        """
        TD_COAP_CORE_13:
        Handle request containing several Uri - Query options.
        """

        RESOURCE_URI = "/query"
        EXPECTED_RESPONSE_CODE = 69

        public CC13(String serverURI) {
            super(CC13.class.getSimpleName());

            # create the request
            Request request = new Request(CodeRegistry.METHOD_GET, true);
            # add query
            request.setOption(new Option("first=1", OptionNumberRegistry.URI_QUERY));
            request.addOption(new Option("second=2", OptionNumberRegistry.URI_QUERY));
            request.addOption(new Option("third=3", OptionNumberRegistry.URI_QUERY));
            # set the parameters and execute the request
            executeRequest(request, serverURI, RESOURCE_URI);
        }

        protected boolean checkResponse(Request request, Response response) {
            boolean success = true;

            success &= checkType(Message.messageType.ACK, response.getType()) || checkType(Message.messageType.CON, response.getType());
            success &= checkInt(EXPECTED_RESPONSE_CODE, response.getCode(), "code");
            success &= hasContentType(response);

            return success;
        }
    }

    class CC16(TestClientAbstract):
        """
        TD_COAP_CORE_16:
        Perform GET transaction with delayed response (NON mode).
        """

        RESOURCE_URI = "/separate"
        EXPECTED_RESPONSE_CODE = 69

        public CC16(String serverURI) {
            super(CC16.class.getSimpleName());

            # create the request
            Request request = new Request(CodeRegistry.METHOD_GET, false);
            # set the parameters and execute the request
            executeRequest(request, serverURI, RESOURCE_URI);
        }

        protected boolean checkResponse(Request request, Response response) {
            boolean success = true;

            success &= checkType(Message.messageType.NON, response.getType());
            success &= checkInt(EXPECTED_RESPONSE_CODE, response.getCode(), "code");
            success &= hasContentType(response);

            return success;
        }
    }

    class CL01(TestClientAbstract):
        """
        TD_COAP_LINK_01:
        Access to well - known interface for resource discovery.
        """

        RESOURCE_URI = "/.well-known/core"
        EXPECTED_RESPONSE_CODE = 69

        public CL01(String serverURI) {
            super(CL01.class.getSimpleName());

            # create the request
            Request request = new Request(CodeRegistry.METHOD_GET, true);
            # set the parameters and execute the request
            executeRequest(request, serverURI, RESOURCE_URI);
        }

        protected boolean checkResponse(Request request, Response response) {
            boolean success = true;

            success &= checkType(Message.messageType.ACK, response.getType());
            success &= checkInt(EXPECTED_RESPONSE_CODE, response.getCode(), "code");
            success &= checkOption(new Option(MediaTypeRegistry.APPLICATION_LINK_FORMAT, OptionNumberRegistry.CONTENT_TYPE), response.getFirstOption(OptionNumberRegistry.CONTENT_TYPE));

            return success;
        }
    }

    class CL02(TestClientAbstract):
        """
        TD_COAP_LINK_02:
        Use filtered requests for limiting discovery results.
        """

        RESOURCE_URI = "/.well-known/core"
        EXPECTED_RESPONSE_CODE = 69
        EXPECTED_RT = "rt=block"

        public CL02(String serverURI) {
            super(CL02.class.getSimpleName());

            # create the request
            Request request = new Request(CodeRegistry.METHOD_GET, true);
            # set query
            request.setOption(new Option(EXPECTED_RT, OptionNumberRegistry.URI_QUERY));
            # set the parameters and execute the request
            executeRequest(request, serverURI, RESOURCE_URI);
        }

        protected boolean checkResponse(Request request, Response response) {
            boolean success = true;

            success &= checkType(Message.messageType.ACK, response.getType());
            success &= checkInt(EXPECTED_RESPONSE_CODE, response.getCode(), "code");
            success &= checkOption(new Option(MediaTypeRegistry.APPLICATION_LINK_FORMAT, OptionNumberRegistry.CONTENT_TYPE), response.getFirstOption(OptionNumberRegistry.CONTENT_TYPE));
            success &= checkDiscovery(EXPECTED_RT, response.getPayloadString());

            return success;
        }
    }

    class CB01(TestClientAbstract):
        """
        TD_COAP_BLOCK_01:
        Handle GET blockwise transfer for large resource (early negotiation).
        """

        RESOURCE_URI = "/large"
        EXPECTED_RESPONSE_CODE = 69

        public CB01(String serverURI) {
            super(CB01.class.getSimpleName());

            # create the request
            Request request = new Request(CodeRegistry.METHOD_GET, true);
            # set block2
            request.setOption(new BlockOption(OptionNumberRegistry.BLOCK2, 0, BlockOption.encodeSZX(PLUGTEST_BLOCK_SIZE), false));
            # set the parameters and execute the request
            executeRequest(request, serverURI, RESOURCE_URI);
        }

        protected boolean checkResponse(Request request, Response response) {
            boolean success = response.hasOption(OptionNumberRegistry.BLOCK2);


            if (! success) {
                logging.info("FAIL: no Block2 option");
            } else {
                # get actual number of blocks for check
                int maxNUM = ((BlockOption)response.getFirstOption(OptionNumberRegistry.BLOCK2)).getNUM();

                success &= checkType(Message.messageType.ACK, response.getType());
                success &= checkInt(EXPECTED_RESPONSE_CODE, response.getCode(), "code");
                success &= checkOption(
                        new BlockOption(OptionNumberRegistry.BLOCK2, maxNUM, BlockOption.encodeSZX(PLUGTEST_BLOCK_SIZE), false),
                        response.getFirstOption(OptionNumberRegistry.BLOCK2)
                        );
                success &= hasContentType(response);
            }
            return success;
        }
    }

    class CB02(TestClientAbstract):
        """
        TD_COAP_BLOCK_02:
        Handle GET blockwise transfer for large resource (late negotiation).
        """

        RESOURCE_URI = "/large"
        EXPECTED_RESPONSE_CODE = 69

        public CB02(String serverURI) {
            super(CB02.class.getSimpleName());

            # create the request
            Request request = new Request(CodeRegistry.METHOD_GET, true);
            # set the parameters and execute the request
            executeRequest(request, serverURI, RESOURCE_URI);
        }

        protected boolean checkResponse(Request request, Response response) {
            boolean success = response.hasOption(OptionNumberRegistry.BLOCK2);

            if (! success) {
                logging.info("FAIL: no Block2 option");
            } else {
                # get actual number of blocks for check
                int maxNUM = ((BlockOption)response.getFirstOption(OptionNumberRegistry.BLOCK2)).getNUM();

                success &= checkType(Message.messageType.ACK, response.getType());
                success &= checkInt(EXPECTED_RESPONSE_CODE, response.getCode(), "code");
                success &= checkOption(
                        new BlockOption(OptionNumberRegistry.BLOCK2, maxNUM, BlockOption.encodeSZX(PLUGTEST_BLOCK_SIZE), false),
                        response.getFirstOption(OptionNumberRegistry.BLOCK2)
                        );
                success &= hasContentType(response);
            }
            return success;
        }
    }

    class CB03(TestClientAbstract):
        """
        TD_COAP_BLOCK_03:
        Handle PUT blockwise transfer for large resource.
        """

        RESOURCE_URI = "/large-update"
        EXPECTED_RESPONSE_CODE = 68

        public CB03(String serverURI) {
            super(CB03.class.getSimpleName());

            # create the request
            Request request = new Request(CodeRegistry.METHOD_PUT, true);

            # create payload
            StringBuilder builder = new StringBuilder();
            for (int i=0; i < 20; + +i) {
                for (int j=0; j < 63; + +j) {
                    builder.append(Integer.toString(i % 10));
                }
                builder.append('\n');
            }
            request.setPayload(builder.toString(), MediaTypeRegistry.TEXT_PLAIN);

            # set the parameters and execute the request
            executeRequest(request, serverURI, RESOURCE_URI);
        }

        protected boolean checkResponse(Request request, Response response) {
            boolean success = response.hasOption(OptionNumberRegistry.BLOCK1);

            if (! success) {
                logging.info("FAIL: no Block1 option");
            } else {
                # get actual number of blocks for check
                int maxNUM = ((BlockOption)response.getFirstOption(OptionNumberRegistry.BLOCK1)).getNUM();

                success &= checkType(Message.messageType.ACK, response.getType());
                success &= checkInt(EXPECTED_RESPONSE_CODE, response.getCode(), "code");
                success &= checkOption(
                        new BlockOption(OptionNumberRegistry.BLOCK1, maxNUM, BlockOption.encodeSZX(PLUGTEST_BLOCK_SIZE), false),
                        response.getFirstOption(OptionNumberRegistry.BLOCK1)
                        );
            }

            return success;
        }
    }

    class CB04(TestClientAbstract):
        """
        TD_COAP_BLOCK_04:
        Handle POST blockwise transfer for large resource.
        """

        RESOURCE_URI = "/large-create"
        EXPECTED_RESPONSE_CODE = 65

        public CB04(String serverURI) {
            super(CB04.class.getSimpleName());

            # create the request
            Request request = new Request(CodeRegistry.METHOD_POST, true);

            # create payload
            StringBuilder builder = new StringBuilder();
            for (int i=0; i < 20; + +i) {
                for (int j=0; j < 63; + +j) {
                    builder.append(Integer.toString(i % 10));
                }
                builder.append('\n');
            }
            request.setPayload(builder.toString(), MediaTypeRegistry.TEXT_PLAIN);

            # set the parameters and execute the request
            executeRequest(request, serverURI, RESOURCE_URI);
        }

        protected boolean checkResponse(Request request, Response response) {
            boolean success = response.hasOption(OptionNumberRegistry.BLOCK1);

            if (! success) {
                logging.info("FAIL: no Block1 option");
            } else {
                # get actual number of blocks for check
                int maxNUM = ((BlockOption)response.getFirstOption(OptionNumberRegistry.BLOCK1)).getNUM();

                success &= checkType(Message.messageType.ACK, response.getType());
                success &= checkInt(EXPECTED_RESPONSE_CODE, response.getCode(), "code");
                success &= checkOption(
                        new BlockOption(OptionNumberRegistry.BLOCK1, maxNUM, BlockOption.encodeSZX(PLUGTEST_BLOCK_SIZE), false),
                        response.getFirstOption(OptionNumberRegistry.BLOCK1)
                        );
                success &= hasLocation(response);
            }

            return success;
        }
    }

    class CO01_02(TestClientAbstract):
        """
        TD_COAP_OBS_01:
        Handle resource observation.
        TD_COAP_OBS_02:
        Stop resource observation.
        """

        RESOURCE_URI = "/obs"
        EXPECTED_RESPONSE_CODE = 69

        public CO01_02(String serverURI) {
            super(CO01_02.class.getSimpleName());

            # create the request
            Request request = new Request(CodeRegistry.METHOD_GET, true);
            # set Observe option
            request.setOption(new Option(0, OptionNumberRegistry.OBSERVE));
            # set the parameters and execute the request
            executeRequest(request, serverURI, RESOURCE_URI);
        }

        protected boolean checkResponse(Request request, Response response) {
            boolean success = true;

            success &= checkInt(EXPECTED_RESPONSE_CODE, response.getCode(), "code");
            success &= hasObserve(response);
            success &= hasContentType(response);

            return success;
        }
        /* 
           @Override
           protected synchronized void executeRequest(Request request, String serverURI, String resourceUri) {
           if (serverURI == null || serverURI.isEmpty()) {
           throw new IllegalArgumentException("serverURI == null || serverURI.isEmpty()");
           }

        # defensive check for slash
        if (! serverURI.endsWith("/") && ! resourceUri.startsWith("/")) {
        resourceUri = "/" + resourceUri;
        }

        URI uri = null;
        try {
        uri = new URI(serverURI + resourceUri);
        } catch (URISyntaxException use) {
        throw new IllegalArgumentException("Invalid URI: " + use.getMessage());
        }

        request.setURI(uri);
        if (request.requiresToken()) {
        request.setToken(TokenManager.getInstance().acquireToken());
        }

        # enable response queue for synchronous I / O
        request.enableResponseQueue(true);

        # for observing
        int observeLoop = 5;

        # print request info
        if (verbose) {
        logging.info("Request for test " + this.testName + " sent");
        request.prettyPrint();
        }

        # execute the request
        try {
        Response response = null;
        boolean success = true;

        request.execute();

        logging.info();
        logging.info("**** TEST: " + testName + " ****");
        logging.info("**** BEGIN CHECK ****");

        # receive multiple responses
        for (int l=0; l < observeLoop; + +l) {
        response = request.receiveResponse();

        # checking the response
        if (response != null) {

        # print response info
        if (verbose) {
        logging.info("Response received");
        logging.info("Time elapsed (ms): " + response.getRTT());
        response.prettyPrint();
        }

        success &= checkResponse(response.getRequest(), response);

        if (! hasObserve(response)) {
        break;
        }
        }
        }

        # TD_COAP_OBS_02: Stop resource observation
        request.removeOptions(OptionNumberRegistry.OBSERVE);
        request.setMID(-1);
        request.execute();
        response = request.receiveResponse();

        success &= hasObserve(response, true);

        if (success) {
            logging.info("**** TEST PASSED ****");
            addSummaryEntry(testName + ": PASSED");
        } else {
            logging.info("**** TEST FAILED ****");
            addSummaryEntry(testName + ": FAILED");
        }

        tickOffTest();

    } catch (IOException e) {
        logging.critical("Failed to execute request: " + e.getMessage());
        sys.exit(-1);
    } catch (InterruptedException e) {
        logging.critical("Interupted during receive: " + e.getMessage());
        sys.exit(-1);
    }
}
}* / 

class CO03_05(TestClientAbstract):
    """
    TD_COAP_OBS_03:
    Client detection of deregistration (Max - Age).
    TD_COAP_OBS_05:
    Server detection of deregistration (explicit RST).
    """

    RESOURCE_URI = "/obs"
    EXPECTED_RESPONSE_CODE = 69

    private Timer timer = new Timer(true);

    /* 
     * Utility class to provide transaction timeouts
     */ 
    private class MaxAgeTask extends TimerTask {

        private Request request;

        public MaxAgeTask(Request request) {
            this.request = request;
        }

        @Override
            public void run() {
                this.request.handleTimeout();
            }
    }

    public CO03_05(String serverURI) {
        super(CO03_05.class.getSimpleName());

        # create the request
        Request request = new Request(CodeRegistry.METHOD_GET, true);
        # set Observe option
        request.setOption(new Option(0, OptionNumberRegistry.OBSERVE));
        # set the parameters and execute the request
        executeRequest(request, serverURI, RESOURCE_URI);
    }

    protected boolean checkResponse(Request request, Response response) {
        boolean success = true;

        success &= checkInt(EXPECTED_RESPONSE_CODE, response.getCode(), "code");
        success &= hasObserve(response);
        success &= hasContentType(response);

        return success;
    }
    /* 
        @Override
        protected synchronized void executeRequest(Request request, String serverURI, String resourceUri) {
        if (serverURI == null || serverURI.isEmpty()) {
        throw new IllegalArgumentException("serverURI == null || serverURI.isEmpty()");
        }

# defensive check for slash
if (! serverURI.endsWith("/") && ! resourceUri.startsWith("/")) {
resourceUri = "/" + resourceUri;
}

URI uri = null;
try {
uri = new URI(serverURI + resourceUri);
} catch (URISyntaxException use) {
throw new IllegalArgumentException("Invalid URI: " + use.getMessage());
}

request.setURI(uri);
if (request.requiresToken()) {
request.setToken(TokenManager.getInstance().acquireToken());
}

# enable response queue for synchronous I / O
if (sync) {
request.enableResponseQueue(true);
}

# for observing
int observeLoop = 5;

# print request info
if (verbose) {
logging.info("Request for test " + this.testName + " sent");
request.prettyPrint();
}

# execute the request
try {
Response response = null;
boolean success = true;
boolean timedOut = false;

MaxAgeTask timeout = null;

request.execute();

logging.info("**** TEST: " + testName + " ****");
logging.info("**** BEGIN CHECK ****");

for (int l=0; l < observeLoop; + +l) {

response = request.receiveResponse();

# checking the response
if (response != null) {

if (l >= 2 && ! timedOut) {
logging.info("+++++++++++++++++++++++");
logging.info("++++ REBOOT SERVER ++++");
logging.info("+++++++++++++++++++++++");
}

if (timeout != null) {
timeout.cancel();
timer.purge();
}

long time = response.getMaxAge() * 1000;

timeout = new MaxAgeTask(request);
timer.schedule(timeout, time + 1000);

# print response info
if (verbose) {
    logging.info("Response received");
    logging.info("Time elapsed (ms): " + response.getRTT());
    response.prettyPrint();
}

success &= checkResponse(response.getRequest(), response);

if (! hasObserve(response)) {
    break;
}

} else {
    timedOut = true;
    logging.info("PASS: Max-Age timed out");
    request.setMID(-1);
    request.execute();

    + +observeLoop;
}
}

# RST to cancel
response.reject();

success &= timedOut;

if (success) {
    logging.info("**** TEST PASSED ****");
    addSummaryEntry(testName + ": PASSED");
} else {
    logging.info("**** TEST FAILED ****");
    addSummaryEntry(testName + ": FAILED");
}

tickOffTest();

} catch (IOException e) {
    logging.critical("Failed to execute request: " + e.getMessage());
    sys.exit(-1);
} catch (InterruptedException e) {
    logging.critical("Interupted during receive: " + e.getMessage());
    sys.exit(-1);
}
}
}
* / 
class CO04(TestClientAbstract):
    """
    TD_COAP_OBS_04:
    Server detection of deregistration (client OFF).
    """

    RESOURCE_URI = "/obs"
    EXPECTED_RESPONSE_CODE = 69

    public CO04(String serverURI) {
        super(CO04.class.getSimpleName());

        # create the request
        Request request = new Request(CodeRegistry.METHOD_GET, true);
        # set Observe option
        request.setOption(new Option(0, OptionNumberRegistry.OBSERVE));
        # set the parameters and execute the request
        executeRequest(request, serverURI, RESOURCE_URI);
    }

    protected boolean checkResponse(Request request, Response response) {
        boolean success = true;

        success &= checkInt(EXPECTED_RESPONSE_CODE, response.getCode(), "code");
        success &= hasObserve(response);
        success &= hasContentType(response);

        return success;
    }
}
}
