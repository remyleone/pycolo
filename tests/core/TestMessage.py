# coding=utf-8

"""
TODO
"""

import unittest
import logging
from pycolo import message
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
            code=codes.get,
            msgType=refType.con,
            messageID=12345,
            payload=b"Hello"
        )
        logging.info(original)
        new_message = Message()
        new_message.load(original.dump())
        self.assertEquals(original.code, new_message.code)
        self.assertEquals(original.type, new_message.type)
        self.assertEquals(original.MID, new_message.MID)
        self.assertEquals(len(original.option), len(new_message.option))
        self.assertArrayEquals(original.payload, new_message.payload)

    def test_OptionMessage(self):
        """
        Basic options test messages.
        """
        msg = Message(
            peerAddress="localhost",
            code=codes.get,
            msgType=refType.con,
            messageID=12345,
            payload=b"Hello",
            options={2: 42, 6: 42}
        )
        logging.info(msg)
        newMsg = Message()
        newMsg.load(msg.dump())
        self.assertEquals(msg.code, newMsg.code)
        self.assertEquals(msg.type, newMsg.type)
        self.assertEquals(msg.MID, newMsg.MID)
        self.assertEquals(msg.options, newMsg.options)
        self.assertArrayEquals(msg.payload, newMsg.payload)


    def test_ExtendedOptionMessage(self):
        """
        Test several options
        """
        msg = Message(
            peerAddress="localhost",
            code=codes.GET,
            msgType=refType.con,
            messageID=12345,
            # will fail as limit of max 15 options would be exceeded
            options={"a": 1, "ab": 197}
        )
        logging.info(msg)
        newMsg = Message()
        newMsg.load(msg.dump())
        self.assertEquals(msg.code, newMsg.code)
        self.assertEquals(msg.type, newMsg.type)
        self.assertEquals(msg.MID, newMsg.MID)
        self.assertEquals(len(msg.option), len(newMsg.option))


if __name__ == '__main__':
    unittest.main()
