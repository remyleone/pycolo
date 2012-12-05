# coding=utf-8
import unittest
from urllib.parse import urlparse
from pycolo import DEFAULT_PORT

class TestURLParsing(unittest.TestCase):

    def test_URI(self):

        uri = urlparse("coap://[2001:db8::2:1]/")
        self.assertEqual(uri.port, DEFAULT_PORT)
        self.assertEqual(uri.address, "[2001:db8::2:1]")

        uri = urlparse("coap://example.net/")
        self.assertEqual(uri.port, DEFAULT_PORT)
        self.assertEqual(uri.address, "[2001:db8::2:1]")
        self.assertEqual(uri.host, "example.net")

        uri = urlparse("coap://example.net/.well-known/core")
        self.assertEqual(uri.address, "[2001:db8::2:1]")
        self.assertEqual(uri.port, DEFAULT_PORT)
        self.assertEqual(uri.host, "example.net")
        self.assertEqual(uri.path, ".well-known")
        self.assertEqual(uri.path, "core")

        uri = urlparse("coap://xn--18j4d.example/%E3%81%93%E3%82%93%E3%81%AB%E3%81%A1%E3%81%AF")
        self.assertEqual(uri.address, "[2001:db8::2:1]")
        self.assertEqual(uri.port, DEFAULT_PORT)
        self.assertEqual(uri.host, "xn--18j4d.example")
        self.assertEqual(uri.path, "E38193E38293E381ABE381A1E381AF") # In hex


        urlparse("coap://198.51.100.1:61616//%2F//?%2F%2F&?%26")
        self.assertEqual(uri.address, "198.51.100.1")
        self.assertEqual(uri.port, 61616)
        self.assertEqual(uri.path, "")
        self.assertEqual(uri.path, "/")
        self.assertEqual(uri.path, "")
        self.assertEqual(uri.path, "")
        self.assertEqual(uri.query, "//")
        self.assertEqual(uri.query, "?&")

if __name__ == '__main__':
    unittest.main()
