#!/usr/bin/env python
# coding=utf-8

import unittest

from pycolo.endpoint import Endpoint
from pycolo.request import request
from pycolo.resource import Resource


class ResourceTest(unittest.BaseTestSuite):


    def setUp(self):
        res = ResourceTest()
        server = Endpoint()
        server.addResource(res)

    def simpleTest(self):
        root = Resource(link_format="</sensors/temp>;ct=41;rt=\"TemperatureC\"")
        res = root["/sensors/temp"]
        self.assertNotNull(res)
        self.assertEquals("temp", res)
        self.assertEquals(41, res.contentType)
        self.assertEquals("TemperatureC", res.resourceType)

    def extendedTest(self):
        input = "</my/Path>;rt=\"MyName\";if=\"/someRef/path\";ct=42;obs;sz=10"
        root = Resource(link_format=input)
        my = Resource("my")
        my.setResourceType("replacement")
        root.add(my)
        str(root)
        res = root.getResource("/my/Path")
        self.assertNotNull(res)
        res = root.getResource("my/Path")
        self.assertNotNull(res)
        res = root.getResource("my")
        res = res.getResource("Path")
        self.assertNotNull(res)
        res = res.getResource("/my/Path")
        self.assertNotNull(res)
        self.assertEquals("Path", res.__name__)
        self.assertEquals("/my/Path", res.getPath())
        self.assertEquals("MyName", res.getResourceType().get(0))
        self.assertEquals("/someRef/path", res.getInterfaceDescription().get(0))
        self.assertEquals(42, res.getContentTypeCode().get(0).intValue())
        self.assertEquals(10, res.getMaximumSizeEstimate())
        self.assertTrue(res.isObservable())
        res = root.getResource("my")
        self.assertNotNull(res)
        self.assertEquals("replacement", res.getResourceType().get(0))

    def conversionTest(self):
        link1 = "</myUri/something>;ct=42;if=\"/someRef/path\";obs;rt=\"MyName\";sz=10"
        link2 = "</myUri>;rt=\"NonDefault\""
        link3 = "</a>"
        format = "%s,%s,%s" % (link1, link2, link3)
        res = Resource(format)
        str(res)
        result = res.link()
        print("%s,%s,%s" % (link3, link2, link1))
        print(result)
        self.assertEquals("%s,%s,%s" % (link3, link2, link1), result)

    def concreteTest(self):
        link = "</careless>;rt=\"SepararateResponseTester\";title=\"This resource will ACK anything," \
               " but never send a separate response\"," \
               "</feedback>;rt=\"FeedbackMailSender\";title=\"POST feedback using mail\"," \
               "</helloWorld>;rt=\"HelloWorldDisplayer\";title=\"GET a friendly greeting!\"," \
               "</image>;ct=21;ct=22;ct=23;ct=24;rt=\"Image\";sz=18029;title=\"GET an image with different content-types\"," \
               "</large>;rt=\"block\";title=\"Large resource\"," \
               "</large_update>;rt=\"block\";rt=\"observe\";title=\"Large resource that can be updated using PUT method\"," \
               "</mirror>;rt=\"RequestMirroring\";title=\"POST request to receive it back as echo\"," \
               "</obs>;obs;rt=\"observe\";title=\"Observable resource which changes every 5 seconds\"," \
               "</query>;title=\"Resource accepting query parameters\"," \
               "</seg1/seg2/seg3>;title=\"Long path resource\"," \
               "</separate>;title=\"Resource which cannot be served immediately and which cannot be acknowledged in a piggy-backed way\"," \
               "</storage>;obs;rt=\"Storage\";title=\"PUT your data here or POST new resources!\"," \
               "</test>;title=\"Default test resource\"," \
               "</timeResource>;rt=\"CurrentTime\";title=\"GET the current time\"," \
               "</toUpper>;rt=\"UppercaseConverter\";title=\"POST text here to convert it to uppercase\"," \
               "</weatherResource>;rt=\"ParisWeather\";title=\"GET the current weather in Paris, France\""
        res = Resource(link_format=link)

    def matchTest(self):
        link1 = "</myUri/something>;ct=42;if=\"/someRef/path\";obs;rt=\"MyName\";sz=10"
        link2 = "</myUri>;ct=50;rt=\"MyName\""
        link3 = "</a>;sz=10;rt=\"MyNope\""
        raw_links = "%s,%s,%s" % (link1, link2, link3)
        res = Resource(link_format=raw_links)
        query = {"rt": "MyName"}
        res = request.get("/myUri/something", param=query)
        self.assertEquals(link2 + "," + link1, res.payload)

    def test_simple(self):
        raw_links = """
        </hello>;n="hello";ct=0,
        </secret>;n="secret";ct=0,
        </sources>;n="sources";ct=0
        """
        r = Resource(from_link=raw_links)

    def test_other(self):
        raw_link = """
        </sensors>;ct=40;title="Sensor Index",
        </sensors/temp>;rt="temperature-c";if="sensor",
        </sensors/light>;rt="light-lux";if="sensor",
        <http://www.example.com/sensors/t123>;anchor="/sensors/temp";rel="describedby",
        </t>;anchor="/sensors/temp";rel="alternate"
        """
        pass

    def test_search(self):
        """
        Implement a test on search parameter in a query.
        :return:
        """
        pass

if __name__ == '__main__':
    unittest.main()
