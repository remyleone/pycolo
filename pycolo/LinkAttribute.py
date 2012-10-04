# coding=utf-8
import java.util.Scanner
import logging
import re


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

    @classmethod
    @overloaded
    def parse(cls, str_):
        """ generated source for method parse """
        return cls.parse(Scanner(str_))

    @classmethod
    @parse.register(object, Scanner)
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
        """ generated source for method compareTo """
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
