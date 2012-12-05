# coding=utf-8

"""
Implementing ETSI Optional CoAP BLOCK Tests
"""
import logging

import unittest
from pycolo import message

from tests.etsi import PLUGTEST_BLOCK_SIZE
from pycolo.request import request as coap, request
from pycolo.codes import mediaCodes, options, codes, msgType
from pycolo.endpoint import Endpoint
from pycolo.message import Response
from pycolo.resource import Resource
from tests.etsi import server


class TestBlock(unittest.TestCase):
    """
    Test suite for ETSI Optional CoAP BLOCK Tests

    - TD_COAP_BLOCK_01: Handle GET blockwise transfer for large resource
        (early negotiation)
    - TD_COAP_BLOCK_02: Handle GET blockwise transfer for large resource
        (late negotiation)
    - TD_COAP_BLOCK_03: Handle PUT blockwise transfer for large resource
    - TD_COAP_BLOCK_04: Handle POST blockwise transfer for large resource
    """

    def setUp(self):
        """
        Setting up a CoAP server running on localhost for testing.
        """
        self.server = server

    def test_TD_COAP_BLOCK_01(self):
        """
        :Identifier: TD_COAP_BLOCK_01
        :Objective: Handle GET blockwise transfer for large resource
            (early negotiation)
        :Configuration: CoAP_CFG_01

        :Pre-test conditions:
            - Client supports Block transfers
            - Server supports Block transfers
            - Server offers a large resource /large
            - Client knows /large requires block transfer

        - Step 1 stimulus Client is requested to retrieve resource /large

        - Step 2 (check (CON)) Client sends a GET request containing Block2
            option indicating block number 0 and desired block size

        - Step 3 (check (CON)) Server sends response containing
            Block2 option indicating block number and size

        - Step 4 (check (CON)) Client send GET requests for further blocks

        - Step 5 (check (CON)) Each request contains Block2 option indicating
            block number of the next block and size of the last received block

        - Step 6 (check (CON)) Server sends further responses containing
            Block2 option indicating block number and size

        - Step 7 (verify (IOP)) Client displays the received information
        """
        r = coap.get(self.server.url + "/large",
            confirmable=True,
            options={options.block2: (0, PLUGTEST_BLOCK_SIZE)})
        self.assertEqual(r.options[options.block2])
        self.assertEqual(r.code, codes.content)
        self.assertEqual(r.msgType, msgType.ack)
        logging.info(r)

    #        #request.setOption(new BlockOption(options.BLOCK2, 0, BlockOption.encodeSZX(PLUGTEST_BLOCK_SIZE), false))
    #
    #        # get actual number of blocks for check
    #        maxNUM = ((BlockOption)response.getFirstOption(options.BLOCK2)).getNUM()
    #
    #        self.assertEqual(
    #            new BlockOption(options.BLOCK2, maxNUM, BlockOption.encodeSZX(PLUGTEST_BLOCK_SIZE), false),
    #                response.getFirstOption(options.BLOCK2))

    def test_TD_COAP_BLOCK_02(self):
        """
        :Identifier: TD_COAP_BLOCK_02
        :Objective: Handle GET block wise transfer for large resource (late negotiation)
        :Configuration: CoAP_CFG_01

        :Pre-test conditions:
            - Client supports Block transfers
            - Server supports Block transfers
            - Server offers a large resource /large
            - Client does not know /large requires block transfer

        - Step 1 stimulus Client is requested to retrieve resource /large

        - Step 2 (check (CON)) Client sends a GET request not containing Block2 option

        - Step 3 (check (CON)) Server sends response containing Block2 option indicating block number and size

        - Step 4 (check (CON)) Client send GET requests for further blocks

        - Step 5 (check (CON)) Each request contains Block2 option indicating block number
            of the next block and size of the last received block or the
            desired size of next block

        - Step 6 (check (CON)) Server sends further responses containing
            Block2 option indicating block number and size

        - Step 7 (verify (IOP)) Client displays the received information
        """
        r = coap.get(self.server.url + "/large", confirmable=True)
        self.assertEqual(r.code, codes.content)
        self.assertEqual(r.msgType, msgType.ack)
        self.assertin(r.options, options.block2)
        # get actual number of blocks for check
        maxNUM = r.options[options.block2]
        self.assertEqual(r.options[options.block2],
            options.BLOCK2, maxNUM, message.encodeSZX(PLUGTEST_BLOCK_SIZE))

    def test_TD_COAP_BLOCK_03(self):
        """
        :Identifier: TD_COAP_BLOCK_03
        :Objective: Handle PUT block wise transfer for large resource
        :Configuration: CoAP_CFG_01

        :Pre-test conditions:
            - Client supports Block transfers
            - Server supports Block transfers
            - Server offers a large updatable resource /large-update

        - Step 1 (stimulus) Client is requested to update
            resource /large-update on Server

        - Step 2 (check (CON)) Client sends a PUT request containing Block1
            option indicating block number 0 and block size

        - Step 3 (check (CON)) Client sends further requests containing
            Block1 option indicating block number and size

        - Step 4 (verify (IOP)) Server indicates presence of the complete
            updated resource /large-update
        """
        payload = "7" * 128
        r = coap.put(self.server.url + "/large-update",
            confirmable=True, payload=payload)

        # get actual number of blocks for check
        maxNUM = r.options[options.block1]
        coap.put(self.server.url + "/large-update",
            payload=payload,
            options={options.block1: (maxNUM, PLUGTEST_BLOCK_SIZE)})

        self.assertEqual(r.code, codes.changed)
        self.assertEqual(msgType.ack, r.msgType)
        self.assertIn(options.block1, r.options)

    def test_TD_COAP_BLOCK_04(self):
        """
        Identifier: TD_COAP_BLOCK_04
        Objective: Handle POST block wise transfer for large resource
        Configuration: CoAP_CFG_01

        Pre-test conditions:
            - Client supports Block transfers
            - Server supports Block transfers
            - Server accepts creation of new resources on /large-create

        - Step 1 stimulus Client is requested to create a new resource on Server

        - Step 2 (check (CON)) Client sends a POST request containing Block1 option
            indicating block number 0 and block size

        - Step 3 (check (CON)) Client sends further requests containing
            Block1 option indicating block number and size

        - Step 4 (verify (IOP)) Server indicates presence of the complete new resource
        """
        payload = "7" * 63 * 20
        r = coap.post(self.server.url + "/large-create",
            confirmable=True, payload=payload,
            options={options.block1: (0, PLUGTEST_BLOCK_SIZE)})
        # get actual number of blocks for check
        self.assertIn(options.block1, r.sent.options)
        self.assertEqual(msgType.ack, r.msgType)
        self.assertEqual(r.code, codes.created)
        maxNUM = r.options[options.block1]
        self.assertEqual((options.BLOCK1, maxNUM, message.encodeSZX(PLUGTEST_BLOCK_SIZE), False,), r.options[options.block1] )
        assert(r.hasLocation)


if __name__ == '__main__':
    unittest.main()
