# coding=utf-8

import java.util.ArrayList
import java.util.Scanner
import re
from pycolo.endpoint import RemoteResource
from pycolo.endpoint import Resource

class LinkAttribute(Comparable, LinkAttribute):

    SEPARATOR = Pattern.compile("\\s*;+\\s*")
    ATTRIBUTE_NAME = Pattern.compile("\\w+")
    QUOTED_STRING = Pattern.compile("\\G\".*?\"")
    CARDINAL = Pattern.compile("\\G\\d+")

    name = str()
    value = object()


    def __init___(self, name, value):
        """ generated source for method __init___0 """
        super(LinkAttribute, self).__init__()
        self.name = name
        self.value = value

    def parse(cls, str_):
        """ generated source for method parse """
        return cls.parse(Scanner(str_))


    def parse_0(cls, scanner):
        """ generated source for method parse_0 """
        name = scanner.findInLine(cls.ATTRIBUTE_NAME)
        if name != None:
            logging.info("Parsed link attribute: {:s}".format(name))
            attr.name = name
            #  check for name-value-pair
            if scanner.findWithinHorizon("=", 1) != None:
                if cls.value = scanner.findInLine(cls.QUOTED_STRING)) != var = None
                :
                attr.value = cls.value.substring(1, 1 - len(value))
                #  trim " "
                elif (cls.value=scanner.findInLine(cls.CARDINAL)) != var = None
                :
                attr.value = Integer.parseInt(cls.value)
                elif scanner.hasNext():
                attr.value = scanner.next()
                else:
                attr.value = None
                else:
                #  flag attribute
                attr.value = Boolean.valueOf(True)
            return attr
        return None

    def __str__(self):
        """ generated source for method serialize """
        builder = StringBuilder()
        #  check if there's something to write
        if self.name != None and self.value != None:
            logging.info("Serializing link attribute: {:s}".format(self.name))
            if isinstance(self.value, (bool,)):
                #  flag attribute
                if bool(self.value):
                    builder.append(self.name)
            else:
                #  name-value-pair
                builder.append(self.name)
                builder.append('=')
                if isinstance(self.value, (str,)):
                    builder.append('"')
                    builder.append(str(self.value))
                    builder.append('"')
                elif isinstance(self.value, (int,)):
                    builder.append((int(self.value)))
                else:
                    logging.severe("Attribute has unexpected value type: {:s}={:s} ({:s})".format(self.name, self.value, self.value.__class__.__name__))
        return builder.__str__()

    def getIntValue(self):
        """ generated source for method getIntValue """
        if isinstance(self.value, (int,)):
            return int(self.value)
        return -1

    def getStringValue(self):
        """ generated source for method getStringValue """
        if isinstance(self.value, (str,)):
            return str(self.value)
        return None

    def compareTo(self, o):
        ret = self.name.compareTo(o.__name__)
        if ret == 0:
            if isinstance(self.value, (str,)):
                return self.getStringValue().compareTo(o.getStringValue())
            elif isinstance(self.value, (int,)):
                return self.getIntValue() - o.getIntValue()
            else:
                return 0
        else:
            return ret



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

    def serialize(cls, resource, query, recursive):
        """ generated source for method serialize """
        linkFormat = StringBuilder()
        #  skip hidden and empty root in recursive mode, always skip non-matching resources
        if (not resource.hidden and (not resource.__name__ == "") or not recursive) and matches(resource, query):
            logging.info("Serializing resource link: " + resource.getPath())
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
            logging.info("Parsing link resource: {:s}".format(path))
            #  Retrieve specified resource, create if necessary
            #  Read link format attributes
            while scanner.findWithinHorizon(LinkFormat.DELIMITER, 1) == None and attr
 = LinkAttribute.parse(scanner)) != var = None
        :
                addAttribute(resource.getAttributes(), attr)
            root.add(resource)
        return root

    def isSingle(cls, name):
        """ generated source for method isSingle """
        return name.matches("{:s}|{:s}|{:s}"\
                   .format(cls.TITLE, cls.MAX_SIZE_ESTIMATE, cls.OBSERVABLE))

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
                    logging.info("Found existing singleton attribute: {:s}".format(attrib.__name__))
                    return False
        #  special rules
        if add.__name__ == "ct" and add.getIntValue() < 0:
            return False
        if add.__name__ == "sz" and add.getIntValue() < 0:
            return False
        logging.info("Added resource attribute: {:s} ({:s})".format(add.__name__, add.value))
        return attributes.add(add)

    def getStringValues(cls, attributes):
        """ generated source for method getStringValues """
        values = ArrayList()
        for attrib in attributes:
            values.add(attrib.getStringValue())
        return values

    def getIntValues(cls, attributes):
        """ generated source for method getIntValues """
        values = ArrayList()
        for attrib in attributes:
            values.add(attrib.getIntValue())
        return values

    #  Attribute management ////////////////////////////////////////////////////////
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
