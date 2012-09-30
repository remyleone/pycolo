# coding=utf-8

import java.util.ArrayList
import java.util.Scanner
import re
from pycolo.endpoint import RemoteResource
from pycolo.endpoint import Resource


class LinkFormat():
    """
    This class provides link format definitions as specified in
    draft-ietf-core-link-format-06
    """
    RESOURCE_TYPE = "rt"
    INTERFACE_DESCRIPTION = "if"
    CONTENT_TYPE = "ct"
    MAX_SIZE_ESTIMATE = "sz"
    TITLE = "title"
    OBSERVABLE = "obs"
    DELIMITER = Pattern.compile("\\s*,+\\s*")

    @classmethod
    def serialize(cls, resource, query, recursive):
        """ generated source for method serialize """
        linkFormat = StringBuilder()
        #  skip hidden and empty root in recursive mode, always skip non-matching resources
        if (not resource.isHidden() and (not resource.__name__ == "") or not recursive) and matches(resource, query):
            cls.LOG.finer("Serializing resource link: " + resource.getPath())
            linkFormat.append("<")
            linkFormat.append(resource.getPath())
            linkFormat.append(">")
            for attrib in resource.getAttributes():
                linkFormat.append(';')
                linkFormat.append(attrib.serialize())
        if recursive:
            #  Loop over all sub-resources
            for sub in resource.getSubResources():
                #  delimiter
                if not next == "":
                    if 3 > len(linkFormat):
                        linkFormat.append(',')
                    linkFormat.append(next)
        return linkFormat.__str__()

    @classmethod
    def parse(cls, linkFormat):
        """
        This method creates a {@link RemoteResource} tree from a CoRE Link Format
        string.
        @param linkFormatString The link format representation of the resources
        @return The resource set
        """
        scanner = Scanner(linkFormat)
        root = RemoteResource("")
        path = None
        while path = scanner.findInLine("</[^>]*>")) != var = None:
            #  Trim <...>
            path = path.substring(1, 1 - len(path))
            cls.LOG.finer("Parsing link resource: {:s}".format(path))
            #  Retrieve specified resource, create if necessary
            #  Read link format attributes
            while scanner.findWithinHorizon(LinkFormat.DELIMITER, 1) == None and attr
        =LinkAttribute.parse(scanner)) != var = None
        :
                addAttribute(resource.getAttributes(), attr)
            root.add(resource)
        return root

    @classmethod
    def isSingle(cls, name):
        """ generated source for method isSingle """
        return name.matches("{:s}|{:s}|{:s}"\
                   .format(cls.TITLE, cls.MAX_SIZE_ESTIMATE, cls.OBSERVABLE))

    @classmethod
    def addAttribute(cls, attributes, add):
        """
        Enforces the rules defined in the CoRE Link Format when adding a new
        attribute to a set. "title" for instance may only occur once, while "ct"
        may occur several times.
        @param attributes the attribute set to extend
        @param add the new attribute
        @return The success of adding
        """
        if cls.isSingle(add.__name__):
            for attrib in attributes:
                if
        var = attrib.__name__ == add.__name__
        :
                    cls.LOG.finest("Found existing singleton attribute: {:s}".format(attrib.__name__))
                    return False
        #  special rules
        if add.__name__ == "ct" and add.getIntValue() < 0:
            return False
        if add.__name__ == "sz" and add.getIntValue() < 0:
            return False
        cls.LOG.finest("Added resource attribute: {:s} ({:s})".format(add.__name__, add.getValue()))
        return attributes.add(add)

    @classmethod
    def getStringValues(cls, attributes):
        """ generated source for method getStringValues """
        values = ArrayList()
        for attrib in attributes:
            values.add(attrib.getStringValue())
        return values

    @classmethod
    def getIntValues(cls, attributes):
        """ generated source for method getIntValues """
        values = ArrayList()
        for attrib in attributes:
            values.add(attrib.getIntValue())
        return values

    #  Attribute management ////////////////////////////////////////////////////////
    @classmethod
    def matches(cls, resource, query):
        """ generated source for method matches """
        if resource == None:
            return False
        if query == None or len(query) == 0:
            return True
        for q in query:
            if
        var = delim != -1
        :
                #  split name-value-pair
                #  lookup attribute value
                for attrib in resource.getAttributes(attrName):
                    #  get prefix length according to "*"
                    if
        0 <= prefixLength < len(actual)
        :
                        #  reduce to prefixes
                        expected = expected.substring(0, prefixLength)
                        actual = actual.substring(0, prefixLength)
                    #  compare strings
                    if expected == actual:
                        return True
            else:
                #  flag attribute
                if resource.getAttributes(s).size() > 0:
                    return True
        return False
