# coding=utf-8
import unittest
import logging
from pycolo import Message
from pycolo import codes


class MessageTest(unittest.TestCase):
    def testMessage(self):
        msg = Message()
        msg.code = codes.get
        msg.type = "CON"
        msg.MID = 12345
        msg.payload = b"some payload"
        logging.info(str(msg))
        data = msg.dump()
        convMsg = Message()
        convMsg.load(data)
        self.assertEquals(msg.code, convMsg.code)
        self.assertEquals(msg.type, convMsg.type)
        self.assertEquals(msg.MID, convMsg.MID)
        self.assertEquals(len(msg.option), len(convMsg.option))
        self.assertArrayEquals(msg.payload, convMsg.payload)

    def testOptionMessage(self):
        """

        """
        msg = Message()
        msg.code = codes.get
        msg.type = "CON"
        msg.MID = 12345
        msg.payload = b"hallo"
        msg.option["a"] = 1
        msg.option["b"] = 2
        data = msg.dump()
        convMsg = Message()
        convMsg.load(data)
        self.assertEquals(msg.code, convMsg.code)
        self.assertEquals(msg.type, convMsg.type)
        self.assertEquals(msg.MID, convMsg.MID)
        self.assertEquals(len(msg.option), len(convMsg.option))
        self.assertArrayEquals(msg.payload, convMsg.payload)

    def testExtendedOptionMessage(self):
        msg = Message()
        msg.code = codes.get
        msg.type = "CON"
        msg.MID = 12345
        msg.option["a"] = 1
        msg.option["ab"] = 197
        #  will fail as limit of max 15 options would be exceeded
        #  msg.addOption(new Option ("c".getBytes(), 212));
        data = msg.dump()
        try:
            logging.info("Testing getHexString(): %s (%d)",
                str(data), len(data))
        except Exception as e:
            e.with_traceback
        convMsg = Message()
        convMsg.load(data)
        self.assertEquals(msg.code, convMsg.code)
        self.assertEquals(msg.type, convMsg.type)
        self.assertEquals(msg.MID, convMsg.MID)
        self.assertEquals(len(msg.option), len(convMsg.option))


if __name__ == '__main__':
    unittest.main()
