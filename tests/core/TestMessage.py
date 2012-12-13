# coding=utf-8

"""
TODO
"""

import unittest
import logging
from pycolo.codes import codes, options
from pycolo.codes import msgType as refType
from pycolo.message import Message


class MessageTest(unittest.TestCase):
    """
    This test suite test a simple message load/dump.
    """

    def test_SimpleMessage(self):
        """
        Basic message serialization/deserialization
        """
        original = Message(
            peerAddress="localhost",
            status_code=codes.get,
            msg_type=refType.con,
            message_id=12345,
            payload="Hello"
        )
        logging.info(original)
        logging.info(original.to_raw())
        new_message = Message()
        new_message.from_raw(original.to_raw())
        self.assertEquals(original.status_code, new_message.status_code)
        self.assertEquals(original.msg_type, new_message.msg_type)
        self.assertEquals(original.message_id, new_message.message_id)
        self.assertEquals(original.payload, new_message.payload)

    def test_OptionMessage(self):
        """
        Basic options test messages.
        """
        msg = Message(
            peerAddress="localhost",
            status_code=codes.get,
            msg_type=refType.con,
            message_id=12345,
            payload="Hello",
        )
        logging.info(msg.to_raw())
        newMsg = Message()
        newMsg.from_raw(msg.to_raw())
        self.assertEquals(msg.status_code, newMsg.status_code)
        self.assertEquals(msg.msg_type, newMsg.msg_type)
        self.assertEquals(msg.message_id, newMsg.message_id)
        self.assertEquals(msg.payload, newMsg.payload)


    def test_ExtendedOptionMessage(self):
        """
        Test several options
        """
        msg = Message(
            peerAddress="localhost",
            status_code=codes.GET,
            msg_type=refType.con,
            message_id=12345,
        )
        logging.info(msg)
        newMsg = Message()
        newMsg.from_raw(msg.to_raw())
        self.assertEquals(msg.status_code, newMsg.status_code)
        self.assertEquals(msg.msg_type, newMsg.msg_type)
        self.assertEquals(msg.message_id, newMsg.message_id)


if __name__ == '__main__':
    unittest.main()
