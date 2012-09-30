#!/usr/bin/env python
""" generated source for module ResourceTest """
# package: ch.ethz.inf.vs.californium.test
import 

import java.util.ArrayList

import java.util.List

import org.junit.Test

import ch.ethz.inf.vs.californium.coap.LinkFormat

import ch.ethz.inf.vs.californium.coap.Option

import ch.ethz.inf.vs.californium.coap.OptionNumberRegistry

import ch.ethz.inf.vs.californium.endpoint.RemoteResource

import ch.ethz.inf.vs.californium.endpoint.Resource

class ResourceTest(object):
    """ generated source for class ResourceTest """
    def simpleTest(self):
        """ generated source for method simpleTest """
        print "=[ simpleTest ]=============================="
        input = "</sensors/temp>;ct=41;rt=\"TemperatureC\""
        root = RemoteResource.newRoot(input)
        root.prettyPrint()
        res = root.getResource("/sensors/temp")
        assertNotNull(res)
        print res.__name__
        assertEquals("temp", res.__name__)
        assertEquals(Integer.valueOf(41), res.getContentTypeCode().get(0))
        assertEquals("TemperatureC", res.getResourceType().get(0))

    def extendedTest(self):
        """ generated source for method extendedTest """
        print "=[ extendedTest ]=============================="
        input = "</my/Path>;rt=\"MyName\";if=\"/someRef/path\";ct=42;obs;sz=10"
        root = RemoteResource.newRoot(input)
        my = RemoteResource("my")
        my.setResourceType("replacement")
        root.add(my)
        root.prettyPrint()
        res = root.getResource("/my/Path")
        assertNotNull(res)
        res = root.getResource("my/Path")
        assertNotNull(res)
        res = root.getResource("my")
        res = res.getResource("Path")
        assertNotNull(res)
        res = res.getResource("/my/Path")
        assertNotNull(res)
        assertEquals("Path", res.__name__)
        assertEquals("/my/Path", res.getPath())
        assertEquals("MyName", res.getResourceType().get(0))
        assertEquals("/someRef/path", res.getInterfaceDescription().get(0))
        assertEquals(42, res.getContentTypeCode().get(0).intValue())
        assertEquals(10, res.getMaximumSizeEstimate())
        assertTrue(res.isObservable())
        res = root.getResource("my")
        assertNotNull(res)
        assertEquals("replacement", res.getResourceType().get(0))

    def conversionTest(self):
        """ generated source for method conversionTest """
        print "=[ conversionTest ]=============================="
        link1 = "</myUri/something>;ct=42;if=\"/someRef/path\";obs;rt=\"MyName\";sz=10"
        link2 = "</myUri>;rt=\"NonDefault\""
        link3 = "</a>"
        format = link1 + "," + link2 + "," + link3
        res = RemoteResource.newRoot(format)
        res.prettyPrint()
        result = LinkFormat.serialize(res, None, True)
        print link3 + "," + link2 + "," + link1
        print result
        assertEquals(link3 + "," + link2 + "," + link1, result)

    def concreteTest(self):
        """ generated source for method concreteTest """
        print "=[ concreteTest ]=============================="
        link = "</careless>;rt=\"SepararateResponseTester\";title=\"This resource will ACK anything, but never send a separate response\",</feedback>;rt=\"FeedbackMailSender\";title=\"POST feedback using mail\",</helloWorld>;rt=\"HelloWorldDisplayer\";title=\"GET a friendly greeting!\",</image>;ct=21;ct=22;ct=23;ct=24;rt=\"Image\";sz=18029;title=\"GET an image with different content-types\",</large>;rt=\"block\";title=\"Large resource\",</large_update>;rt=\"block\";rt=\"observe\";title=\"Large resource that can be updated using PUT method\",</mirror>;rt=\"RequestMirroring\";title=\"POST request to receive it back as echo\",</obs>;obs;rt=\"observe\";title=\"Observable resource which changes every 5 seconds\",</query>;title=\"Resource accepting query parameters\",</seg1/seg2/seg3>;title=\"Long path resource\",</separate>;title=\"Resource which cannot be served immediately and which cannot be acknowledged in a piggy-backed way\",</storage>;obs;rt=\"Storage\";title=\"PUT your data here or POST new resources!\",</test>;title=\"Default test resource\",</timeResource>;rt=\"CurrentTime\";title=\"GET the current time\",</toUpper>;rt=\"UppercaseConverter\";title=\"POST text here to convert it to uppercase\",</weatherResource>;rt=\"ZurichWeather\";title=\"GET the current weather in zurich\""
        res = RemoteResource.newRoot(link)
        result = LinkFormat.serialize(res, None, True)
        print link
        print result
        assertEquals(link, result)

    def matchTest(self):
        """ generated source for method matchTest """
        print "=[ matchTest ]=============================="
        link1 = "</myUri/something>;ct=42;if=\"/someRef/path\";obs;rt=\"MyName\";sz=10"
        link2 = "</myUri>;ct=50;rt=\"MyName\""
        link3 = "</a>;sz=10;rt=\"MyNope\""
        format = link1 + "," + link2 + "," + link3
        res = RemoteResource.newRoot(format)
        res.prettyPrint()
        query = ArrayList()
        query.add(Option("rt=MyName", OptionNumberRegistry.URI_QUERY))
        print LinkFormat.matches(res.getResource("/myUri/something"), query)
        queried = LinkFormat.serialize(res, query, True)
        assertEquals(link2 + "," + link1, queried)

