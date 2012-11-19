# coding=utf-8

"""
TODO
"""

import unittest
import logging
from pycolo import message
from pycolo import codes
from pycolo.message import Message


class MessageTest(unittest.TestCase):
    """
    TODO
    """

    def testMessage(self):
        """
        Basic message serialization/deserialization
        """
        msg = Message("localhost")
        msg.code = codes.get
        msg.type = "CON"
        msg.MID = 12345
        msg.payload = b"Hello"
        logging.info(str(msg))
        data = msg.dump()
        convMsg = Message("localhost")
        convMsg.load(data)
        self.assertEquals(msg.code, convMsg.code)
        self.assertEquals(msg.type, convMsg.type)
        self.assertEquals(msg.MID, convMsg.MID)
        self.assertEquals(len(msg.option), len(convMsg.option))
        self.assertArrayEquals(msg.payload, convMsg.payload)

    def testOptionMessage(self):
        """
        Basic options test messages.
        """
        msg = Message("localhost")
        msg.code = codes.get
        msg.type = "CON"
        msg.MID = 12345
        msg.payload = b"Hello"
        msg.option["a"] = 1
        msg.option["b"] = 2
        data = msg.dump()
        newMsg = Message("localhost")
        newMsg.load(data)
        self.assertEquals(msg.code, newMsg.code)
        self.assertEquals(msg.type, newMsg.type)
        self.assertEquals(msg.MID, newMsg.MID)
        self.assertEquals(len(msg.option), len(newMsg.option))
        self.assertArrayEquals(msg.payload, newMsg.payload)


    def testExtendedOptionMessage(self):
        """
        TODO
        """
        msg = Message("localhost")
        msg.code = codes.get
        msg.type = codes.confirmable
        msg.MID = 12345
        msg.option["a"] = 1
        msg.option["ab"] = 197  # will fail as limit of max 15 options would be exceeded
        data = msg.dump()
        newMsg = Message("localhost")
        newMsg.load(data)
        self.assertEquals(msg.code, newMsg.code)
        self.assertEquals(msg.type, newMsg.type)
        self.assertEquals(msg.MID, newMsg.MID)
        self.assertEquals(len(msg.option), len(newMsg.option))

    def testGETRequestHeader(self):
        """ generated source for method testGETRequestHeader """
        versionIn = 1
        versionSz = 2
        typeIn = 0
        #  Confirmable
        typeSz = 2
        optionCntIn = 1
        optionCntSz = 4
        codeIn = 1
        #  GET Request
        codeSz = 8
        msgIdIn = 0x1234
        msgIdSz = 16
        writer = DatagramWriter()
        writer.write(versionIn, versionSz)
        writer.write(typeIn, typeSz)
        writer.write(optionCntIn, optionCntSz)
        writer.write(codeIn, codeSz)
        writer.write(msgIdIn, msgIdSz)
        data = writer.toByteArray()
        dataRef = [0x41, 0x01, 0x12, 0x34]
        self.assertArrayEquals(dataRef, data)
        reader = DatagramReader(data)
        versionOut = reader.read(versionSz)
        typeOut = reader.read(typeSz)
        optionCntOut = reader.read(optionCntSz)
        codeOut = reader.read(codeSz)
        msgIdOut = reader.read(msgIdSz)
        self.assertEquals(versionIn, versionOut)
        self.assertEquals(typeIn, typeOut)
        self.assertEquals(optionCntIn, optionCntOut)
        self.assertEquals(codeIn, codeOut)
        self.assertEquals(msgIdIn, msgIdOut)



if __name__ == '__main__':
    unittest.main()
