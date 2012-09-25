# coding=utf-8
import unittest
from pycolo.coap.CodeRegistry import CodeRegistry
from pycolo.coap import Message
from pycolo.coap import Option
from pycolo.coap import Message.messageType


class MessageTest(unittest.TestCase):
    def testMessage(self):
        msg = Message()
        msg.setCode(CodeRegistry.METHOD_GET)
        msg.setType(messageType.CON)
        msg.setMID(12345)
        msg.setPayload("some payload".getBytes())
        print msg.__str__()
        data = msg.toByteArray()
        convMsg = Message.fromByteArray(data)
        self.assertEquals(msg.getCode(), convMsg.getCode())
        self.assertEquals(msg.getType(), convMsg.getType())
        self.assertEquals(msg.getMID(), convMsg.getMID())
        self.assertEquals(msg.getOptionCount(), convMsg.getOptionCount())
        self.assertArrayEquals(msg.getPayload(), convMsg.getPayload())

    def testOptionMessage(self):
        """ generated source for method testOptionMessage """
        msg = Message()
        msg.setCode(CodeRegistry.METHOD_GET)
        msg.setType(messageType.CON)
        msg.setMID(12345)
        msg.setPayload("hallo".getBytes())
        msg.addOption(Option("a".getBytes(), 1))
        msg.addOption(Option("b".getBytes(), 2))
        data = msg.toByteArray()
        convMsg = Message.fromByteArray(data)
        self.assertEquals(msg.getCode(), convMsg.getCode())
        self.assertEquals(msg.getType(), convMsg.getType())
        self.assertEquals(msg.getMID(), convMsg.getMID())
        self.assertEquals(msg.getOptionCount(), convMsg.getOptionCount())
        self.assertArrayEquals(msg.getPayload(), convMsg.getPayload())

    def testExtendedOptionMessage(self):
        """ generated source for method testExtendedOptionMessage """
        msg = Message()
        msg.setCode(CodeRegistry.METHOD_GET)
        msg.setType(messageType.CON)
        msg.setMID(12345)
        msg.addOption(Option("a".getBytes(), 1))
        msg.addOption(Option("ab".getBytes(), 197))
        #  will fail as limit of max 15 options would be exceeded
        #  msg.addOption(new Option ("c".getBytes(), 212));
        data = msg.toByteArray()
        try:
            System.out.printf("Testing getHexString(): 0x%s (%d)\n", getHexString(data),)
        except Exception as e:
            #  TODO Auto-generated catch block
            e.printStackTrace()
        convMsg = Message.fromByteArray(data)
        self.assertEquals(msg.getCode(), convMsg.getCode())
        self.assertEquals(msg.getType(), convMsg.getType())
        self.assertEquals(msg.getMID(), convMsg.getMID())
        self.assertEquals(msg.getOptionCount(), convMsg.getOptionCount())

    @classmethod
    def getHexString(cls, b):
        """ generated source for method getHexString """
        result = ""
        i = 0
        while len(b):
            result += Integer.toString((b[i] & 0xff) + 0x100, 16).substring(1)
            i += 1
        return result
