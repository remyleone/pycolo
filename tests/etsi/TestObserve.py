# coding=utf-8

"""
Testing observation as specified in the ETSI IoT CoAP Plugtests.
"""

import datetime
import unittest

from threading import Timer

from pycolo.codes import codes, mediaCodes
from pycolo.endpoint import Endpoint
from pycolo.message import Response
from pycolo.resource import Resource


class Observe(Resource):
    """
    Observable resource which changes every 5 seconds.

    This resource implements a test of specification for the ETSI IoT CoAP
    Plugtests.

    - TD_COAP_OBS_01
    - TD_COAP_OBS_02
    - TD_COAP_OBS_03
    - TD_COAP_OBS_04
    - TD_COAP_OBS_05
    - TD_COAP_OBS_06
    - TD_COAP_OBS_07
    - TD_COAP_OBS_08
    """
    #  The current time represented as string
    time = ""

    def __init__(self):
        self.title = "Observable resource which changes every 5 seconds"
        self.resourceType = "observe"
        self.observable = True
        Timer(5.0, self._update).start()  # Set timer task scheduling

    def _update(self):
        """ Defines a new timer task to return the current time """
        self.time = datetime.datetime.now().strftime("%H:%m:%S")
        self.changed()  # Call changed to notify subscribers

    def performGET(self, request):
        """

        :param request:
        """
        response = Response(codes.RESP_CONTENT)
        response.payload = self.time
        response.contentType = mediaCodes.text
        response.maxAge = 5
        request.respond(response)  # complete the request


class TestObserve(unittest.TestCase):
    """
    TODO
    """

    def setUp(self):
        """
        Set up a configuration as specified in CoAP_CFG_01
        """
        server = Endpoint()
        res = Observe()
        server.addResource(res)

    def test_TD_COAP_OBS_01(self):
        """
        :Identifier: TD_COAP_OBS_01
        :Objective: Handle resource observation
        :Configuration: CoAP_CFG_01

        - Pre-test conditions:
            - Client supports Observe option
            - Server supports Observe option
            - Server offers an observable resource /obs which changes periodically (e.g. every 5s)

        - Step 1 stimulus Client is requested to observe resource /obs on Server

        - Step 2 (check (CON)) Client sends a GET request containing Observe option indicating 0

        - Step 3 (check (CON)) Server sends response containing Observe option

        - Step 4 (verify (IOP)) Client displays the received information

        - Step 5 (check (CON)) Server sends response containing Observe option indicating
          increasing values, as resource changes

        - Step 6 (verify (IOP)) Client displays the updated information
        """
        pass

    def test_TD_COAP_OBS_02(self):
        """
        :Identifier: TD_COAP_OBS_02
        :Objective: Stop resource observation
        :Configuration: CoAP_CFG_01

        - Pre-test conditions:
            - Client supports Observe option
            - Server supports Observe option
            - Server offers an observable resource /obs which changes periodically (e.g. every 5s)
            - Client is observing /obs on Server

        - Step 1 stimulus Client is requested to stop observing resource /obs on Server

        - Step 2 (check (CON))
            Client sends GET request not containing Observe option

        - Step 3 (check (CON))
            Server sends response not containing Observe option

        - Step 4 (verify (IOP)) Client displays the received information

        - Step 5 (check (CON)) Server does not send further response

        - Step 6 (verify (IOP)) Client does not display updated information
        """
        pass


    def test_TD_COAP_OBS_03(self):
        """
        :Identifier: TD_COAP_OBS_03
        :Objective: Client detection of deregistration (Max-Age)
        :Configuration: CoAP_CFG_01

        :Pre-test conditions:
            - Client supports Observe option
            - Server supports Observe option
            - Server offers an observable resource /obs which changes periodically (e.g. every
              5s)
            - Client is observing /obs on Server

        - Step 1 stimulus Server is rebooted

        - Step 2 (check (CON)) Server does not send notifications

        - Step 3 (verify (IOP)) Client does not display updated information

        - Step 4 (verify (IOP)) After Max-Age expiration, Client sends a new GET with
            Observe option for Server’s observable resource

        - Step 5 (check (CON)) Sent request contains Observe option indicating 0

        - Step 6 (check (CON)) Server sends response containing Observe option

        - Step 7 (verify (IOP)) Client displays the received information

        - Step 8 (check (CON)) Server sends response containing Observe option indicating
            increasing values, as resource changes

        - Step 9 (verify (IOP)) Client displays the updated information
        """
        pass

    def test_TD_COAP_OBS_04(self):
        """
        :Identifier: TD_COAP_OBS_04
        :Objective: Server detection of deregistration (client OFF)
        :Configuration: CoAP_CFG_01

        :Pre-test conditions:
            - Client supports Observe option
            - Server supports Observe option
            - Server offers an observable resource /obs which changes periodically (e.g. every 5s)
            - Client is observing /obs on Server

        - Step 1 stimulus Client is switched off

        - Step 2 (check (CON)) Server’s confirmable responses are not acknowledged

        - Step 3 (verify (IOP)) After some delay, Server does not send further responses
        """
        pass

    def test_TD_COAP_OBS_05(self):
        """
        :Identifier: TD_COAP_OBS_05
        :Objective: Server detection of deregistration (explicit OFF)
        :Configuration: CoAP_CFG_01

        :Pre-test conditions:
            - Client supports Observe option
            - Server supports Observe option
            - Server offers an observable resource /obs which changes periodically (e.g. every 5s)
            - Client is observing /obs on Server

        - Step 1 stimulus Client is rebooted

        - Step 2 (check (CON)) Server sends response containing Observe option

        - Step 3 (verify (IOP)) Client discards response and does not display information

        - Step 4 (check (CON)) Client sends RST to Server

        - Step 5 (check (CON)) Server does not send further response
        """
        pass

    def test_TD_COAP_OBS_06(self):
        """
        :Identifier: TD_COAP_OBS_06
        :Objective: Server detection of deregistration (explicit RST)
        :Configuration: CoAP_CFG_01

        :Pre-test conditions:
            - Client supports Observe option
            - Server supports Observe option
            - Server offers an observable resource /obs which changes periodically (e.g. every 5s)

        - Step 1 Stimulus Client is requested to send to the server a GET request with observe option for resource /obs

        - Step 2 (check): The request sent by client contains:
            - Type = 1 (CON)
            - Code = 1 (GET)
            - Token value = a value generated by the client
            - Observe option = empty

        - Step 3 (check): Server sends a notification containing:
            - Type = 1 (CON)
            - Content-format = the same for all notifications
            - Token value = same as one found in the step 2
            - Observe option indicating increasing values

        - Step 4 (check): Client displays the received information

        - Step 5 (check): Client sends an ACK

        - Step 6 (Stimulus): Client is rebooted

        - Step 7 (check): Server is still sending notifications for the request in step 2. Notification contains:
            - Type = 1 (CON)
            - Content-format = the same for all notifications
            - Token value = same as one found in the step 2
            - Observe option indicating increasing values

        - Step 8 (verify): Client discards response and does not display information

        - Step 9 (check): Client sends RST to Server

        - Step 10 (verify): Server does not send further response

        Notes:
            (1) Steps 3-5 are in a loop.
            (2) Step 6-10 are asynchronous to the loop.
        """
        pass

    def test_TD_COAP_OBS_07(self):
        """
        :Identifier: TD_COAP_OBS_07
        :Objective: Server cleans the observers list on DELETE
        :Configuration: CoAP_CFG_01

        :Pre-test conditions:
            - Client supports Observe option
            - Server supports Observe option
            - Server offers an observable resource /obs which changes periodically (e.g. every 5s)

        - Step 1 (stimulus): Client is requested to send to the server a GET request with observe option for resource /obs

        - Step 2 (check): The request sent by client contains:
            - Type = 1 (CON)
            - Code = 1 (GET)
            - Token value = a value generated by the client
            - Observe option = empty

        - Step 3 (check): Server sends a notification containing:
            - Type = 1 (CON)
            - Content-format = the same for all notifications
            - Token value = same as one found in the step 2
            - Observe option indicating increasing values

        - Step 4 (check): Client displays the received information

        - Step 5 (check): Client sends an ACK

        - Step 6 (stimulus): Client is requested to send to the server a DELETE request with observe option for resource /obs

        - Step 7 (check): The request sent by client contains:
            - Type = 1(NON)
            - Code = 4(DELETE)

        - Step 8 (check): Server sends response containing:
            - Type = 1(CON)
            - Code = 66(2.02 Deleted)

        - Step 9 (check): Server sends 4.04 (Not Found) response to the observer registered for /obs

        - Step 10 (verify): Server does not send further responses

        Notes:
            (1) Steps 3-5 are in a loop.
            (2) Step 6-10 are asynchronous to the loop.
            (3) Steps 8 and 9 may occur out-of-order
        """
        pass

    def test_TD_COAP_OBS_08(self):
        """
        :Identifier: TD_COAP_OBS_08
        :Objective: Server cleans the observers list when observed resource content-format changes
        :Configuration: CoAP_CFG_01

        :Pre-test conditions:
            - Client supports Observe option
            - Server supports Observe option
            - Server offers an observable resource /obs which changes periodically (e.g. every 5s)

        - Step 1 (stimulus): Client is requested to send to the server a GET request with observe option for resource /obs

        - Step 2 (check): The request sent by client contains:
            - Type = 1 (CON)
            - Code = 1 (GET)
            - Token value  = a value generated by the client
            - Observe option = None

        - Step 3 (check): Server sends a notification containing:
            - Type = 1 (CON)
            - Content-format = the same for all notifications
            - Token value = same as one found in the step 2
            - Observe option indicating increasing values

        - Step 4 (check): Client displays the received information

        - Step 5 (check): Client sends an ACK

        - Step 6 (stimulus): Client is requested to update the /obs content-format on Server

        - Step 7 (check): Client sends a POST request for /obs indicating a different
            content-format from one received in step 3

        - Step 8 (check): Server sends 2.04 (Changed) to the client

        - Step 9 (check): Server sends 5.00 (Internal Server Error) to the observer registered for /obs

        - Step 10 (Verify): Server does not send further notifications

        Notes:
            (1) Steps 3-5 are in a loop.
            (2) Step 6-10 are asynchronous to the loop.
            (3) Steps 8 and 9 may occur out-of-order
        """
        pass

if __name__ == '__main__':
    unittest.main()
