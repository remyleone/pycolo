# coding=utf-8
import unittest
import logging
from pycolo.coap.CodeRegistry import CodeRegistry
from pycolo.coap import Message


class MessageTest(unittest.TestCase):
    def testMessage(self):
        msg = Message()
        msg.code = CodeRegistry.METHOD_GET
        msg.type = "CON"
        msg.MID = 12345
        msg.payload = b"some payload"
        logging.info(msg)
        data = msg.dump()
        convMsg = Message.load(data)
        self.assertEquals(msg.code, convMsg.code)
        self.assertEquals(msg.type, convMsg.type)
        self.assertEquals(msg.MID, convMsg.MID)
        self.assertEquals(len(msg.option), len(convMsg.option))
        self.assertArrayEquals(msg.payload, convMsg.payload)

    def testOptionMessage(self):
        msg = Message()
        msg.code = CodeRegistry.METHOD_GET
        msg.type = "CON"
        msg.MID = 12345
        msg.payload = b"hallo"
        msg.option["a"] = 1
        msg.option["b"] = 2
        data = msg.dump()
        convMsg = Message.load(data)
        self.assertEquals(msg.code, convMsg.code)
        self.assertEquals(msg.type, convMsg.type)
        self.assertEquals(msg.MID, convMsg.MID)
        self.assertEquals(len(msg.option), len(convMsg.option))
        self.assertArrayEquals(msg.payload, convMsg.payload)

    def testExtendedOptionMessage(self):
        msg = Message()
        msg.code = CodeRegistry.METHOD_GET
        msg.type = messageType.CON
        msg.MID = 12345
        msg.option["a"] = 1
        msg.option["ab"] = 197
        #  will fail as limit of max 15 options would be exceeded
        #  msg.addOption(new Option ("c".getBytes(), 212));
        data = msg.dump()
        try:
            logging.info("Testing getHexString(): 0x%s (%d)\n", getHexString(data),)
        except Exception as e:
            e.with_traceback
        convMsg = Message.load(data)
        self.assertEquals(msg.code, convMsg.code)
        self.assertEquals(msg.type, convMsg.type)
        self.assertEquals(msg.MID, convMsg.MID)
        self.assertEquals(len(msg.option), len(convMsg.option))

    @classmethod
    def getHexString(cls, b):
        result = ""
        i = 0
        while len(b):
            result += int.toString((b[i] & 0xff) + 0x100, 16).substring(1)
            i += 1
        return result
