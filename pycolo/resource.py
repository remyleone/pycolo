# -*- coding:utf-8 -*-

"""
pycolo.structures
~~~~~~~~~~~~~~~~~~~

Pycolo resource.
"""
import re

from pycolo.observe import notifyObservers


class Resource:
    """
    :param title:
    :param resourceIdentifier:
    :param link_format:
    :param hidden:
    :param observable:
    :raise:
    """
    subResources = dict()


    attributes = {
        "resourceType": "rt",
        "interfaceDescription": "if",
        "contentType": "ct",
        "sizeEstimate": "sz",
        "title": "title"
    }

    def __init__(self, title, resourceIdentifier=None,
                 interfaceDescription=None, link_format="",
                 hidden=False, observable=False, parent=None,
                 resourceType=None, contentType=None):
        """
        If a Core Link description string is passed, the resource
        created match the description
        given by this string.
        If a performXXX is not implemented then a message will be raised
        during running
        have
        a default implementation in this class that responds with
        "4.05 Method Not Allowed."
        """
        self.title = title
        self.attributes = dict()
        self.resourceType = resourceType
        self.contentType = contentType
        self.resourceIdentifier = resourceIdentifier
        self.interfaceDescription = interfaceDescription
        self.observable = observable
        self.hidden = hidden

        if parent:
            self.parent = parent
        # TODO: Secure link_format + add alias Ex: rt <=> ressourceType
        if link_format:
            regex_url = re.compile("(?P<url><(.*)>)")
            output = dict()
            for i in link_format.split(";"):
                if regex_url.search(i):
                    print("voici l'url : " + re.sub('[ "<>]', '', i))
                else:
                    t = i.split("=")
                    if len(t) == 1:
                        output[t[0]] = True
                    else:
                        output[t[0]] = re.sub('[ "<>]', '', t[1])


    def __getitem__(self, path):
        path = path.lstrip('/')
        child, sep, rest = path.partition('/')
        if not hasattr(self, child):
            raise AttributeError()
        if not rest:
            return getattr(self, child)
        return getattr(self, child)[rest]


    def count(self, recursive=False):
        """
        Counting sub resources.
        :param recursive:
        :raise:
        """
        if recursive:
            raise Exception("Not implemented yet")
        else:
            len(self.__dict__)

    def getPath(self):
        """
        Returns the full resource path.
        """
        url = str()
        res = self

        while res:
            url = "/" + res.name + url
            res = res.parent
        return url

    def __str__(self):
        """
        Provide a JSON description of the resource.
        :return:
        """
        self.href = self.getPath()
        return str(self.__dict__)

    def changed(self):
        """
        Send a notification to all the subscribed resource.
        :return:
        """
        notifyObservers(self)

    def toLink(self):
        """
        Serialize to a link format definitions as specified in
        draft-ietf-core-link-format-06
        :param self:
        """
        #TODO: Implement a more automatic version of this with unpredefined variables.
        res = "<%s>" % self.getPath()
        for i in self.__dict__:
            if i in Resource.attributes:
                res += ";{0:>s}=\"{1:>s}\""\
                .format(getattr(self, i), self.attributes[i])
        if self.observable:
            res += ";obs"
        return res
