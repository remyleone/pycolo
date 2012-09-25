# coding=utf-8
#import java.util.SortedMap
#import java.util.TreeMap
#import java.util.TreeSet

import logging

from pycolo.coap import LinkAttribute
from pycolo.coap.LinkFormat import LinkFormat
from pycolo.coap import Request
from pycolo.coap import RequestHandler

#
#  * This class provides resource functionality to manage its attributes and
#  * composed trees of resources. A server will use concrete
#  * {@link LocalResource}s while a client will use {@link RemoteResource}s to
#  * manage discovered resources of a remote server.


class Resource(RequestHandler, Comparable, Resource):
    """ generated source for class Resource """
    #  Logging ////////////////////////////////////////////////////////////////
    #  Members ////////////////////////////////////////////////////////////////
    #  The resource's identifier.
    resourceIdentifier = str()

    #  The current parent of the resource. 
    parent = Resource()

    #  The current sub-resources of the resource. A map to remove sub-resources by identifier. 
    subResources = SortedMap()

    #  The total number of sub-resources down from this resource. 
    totalSubResourceCount = int()

    #  Determines whether the resource is hidden in a resource discovery. 
    hidden = bool()

    #  Contains the resource's attributes specified in the CoRE Link Format. 
    attributes = TreeSet()

    #  Constructors ////////////////////////////////////////////////////////////////
    @overloaded
    def __init__(self, resourceIdentifier):
        """ generated source for method __init__ """
        super(Resource, self).__init__()
        self.__init__(resourceIdentifier, False)

    @__init__.register(object, str, bool)
    def __init___0(self, resourceIdentifier, hidden):
        """ generated source for method __init___0 """
        super(Resource, self).__init__()
        #  not removing surrounding slashes here, will be split up by endpoint
        self.resourceIdentifier = resourceIdentifier
        self.attributes = TreeSet()
        self.hidden = hidden

    #  Methods /////////////////////////////////////////////////////////////////////
    # 
    # 	 * Returns the full resource path.
    # 	 * 
    # 	 * @return The path of this resource
    # 	 
    def getPath(self):
        """ generated source for method getPath """
        #  recursion does not work without passing along if called at root or deeper
        builder = StringBuilder()
        builder.append(self.__name__)
        if self.parent != None:
            while base != None:
                builder.insert(0, "/")
                builder.insert(0, base.__name__)
                base = base.parent
        else:
            builder.append("/")
        return builder.__str__()

    # 
    # 	 * Returns the resource name of this resource.
    # 	 * 
    # 	 * @return The name
    # 	 
    def getName(self):
        """ generated source for method getName """
        return self.resourceIdentifier

    # 
    # 	 * This method sets the resource name of this resource.
    # 	 * 
    # 	 * @param resourceURI the new name
    # 	 
    def setName(self, resourceIdentifier):
        """ generated source for method setName """
        self.resourceIdentifier = resourceIdentifier

    #  Methods /////////////////////////////////////////////////////////////////////
    # 
    # 	 * Returns all attributes set for this resource.
    # 	 * 
    # 	 * @return the full set of attributes
    # 	 
    @overloaded
    def getAttributes(self):
        """ generated source for method getAttributes """
        return self.attributes

    @getAttributes.register(object, str)
    def getAttributes_0(self, name):
        """
        Returns all attributes of the given name
        @param name the attribute name, e.g.: "title", "ct"
        @return the set of attributes with the given name 
        """
        ret = ArrayList()
        for attrib in self.attributes:
            if attrib.__name__ == name:
                ret.add(attrib)
        return ret

    def setAttribute(self, attrib):
        """
        Adds the given attribute to the resource depending on the Link Format
        definition. "title" for instance may only occur once.
        @param attrib the attribute to add
        @return the success of adding
        """
        #  Adds depending on the Link Format rules
        return LinkFormat.addAttribute(self.attributes, attrib)

    def clearAttribute(self, name):
        """
         Removes all attributes with the given name.
         @param name the name to remove
         @return the success of clearing
         """
        toRemove = ArrayList()
        cleared = False
        for attrib in attributes:
            if attrib.__name__ == name:
                #  store separately to avoid concurrent modification
                toRemove.add(attrib)
        #  eventually remove
        for attrib in toRemove:
            cleared |= self.attributes.remove(attrib)
        return cleared

    #  Convenience methods ////////////////////////////////////////////////////
    #
    # 	 * This method returns the resource title of this resource.
    # 	 *
    # 	 * @return The current resource title
    #
    def getTitle(self):
        """ generated source for method getTitle """
        title = self.getAttributes(LinkFormat.TITLE)
        return None if title.isEmpty() else title.get(0).getStringValue()

    # 
    # 	 * This method sets the resource title of this resource.
    # 	 * 
    # 	 * @param resourceTitle the resource title
    # 	 
    def setTitle(self, resourceTitle):
        """ generated source for method setTitle """
        self.clearAttribute(LinkFormat.TITLE)
        self.setAttribute(LinkAttribute(LinkFormat.TITLE, resourceTitle))

    def getResourceType(self):
        """
        This method returns the values of the resource type attributes.
        @return The list of set resource types
        """
        return LinkFormat.getStringValues(self.getAttributes(LinkFormat.RESOURCE_TYPE))

    def setResourceType(self, resourceType):
        """
        This method sets the resource type of this resource.
        @param resourceType the resource type
        """
        self.setAttribute(LinkAttribute(LinkFormat.RESOURCE_TYPE, resourceType))

    # 
    # 	 * This method returns the values of the interface description attributes.
    # 	 * 
    # 	 * @return The list of set interface descriptions
    # 	 
    def getInterfaceDescription(self):
        """ generated source for method getInterfaceDescription """
        return LinkFormat.getStringValues(self.getAttributes(LinkFormat.INTERFACE_DESCRIPTION))

    # 
    # 	 * This method adds a interface description to this resource.
    # 	 * 
    # 	 * @param description the resource interface description
    # 	 
    def setInterfaceDescription(self, description):
        """ generated source for method setInterfaceDescription """
        self.setAttribute(LinkAttribute(LinkFormat.INTERFACE_DESCRIPTION, description))

    def getContentTypeCode(self):
        """
        This method returns the content type code of this resource.
        @return The current resource content type code
        """
        return LinkFormat.getIntValues(self.getAttributes(LinkFormat.CONTENT_TYPE))

    # 
    # 	 * This method sets the content-type code of this resource.
    # 	 * 
    # 	 * @param code the resource content-type
    # 	 
    def setContentTypeCode(self, code_):
        """ generated source for method setContentTypeCode """
        self.setAttribute(LinkAttribute(LinkFormat.CONTENT_TYPE, code_))

    # 
    # 	 * This method returns the maximum size estimate of this resource.
    # 	 * 
    # 	 * @return The current resource maximum size estimate
    # 	 
    def getMaximumSizeEstimate(self):
        """ generated source for method getMaximumSizeEstimate """
        sz = self.getAttributes(LinkFormat.MAX_SIZE_ESTIMATE)
        return -1 if sz.isEmpty() else sz.get(0).getIntValue()

    # 
    # 	 * This method sets the maximum size estimate of this resource.
    # 	 * 
    # 	 * @param maximumSize the resource maximum size estimate
    # 	 
    def setMaximumSizeEstimate(self, size):
        """ generated source for method setMaximumSizeEstimate """
        self.setAttribute(LinkAttribute(LinkFormat.MAX_SIZE_ESTIMATE, size))

    # 
    # 	 * This method returns the observable flag of this resource.
    # 	 * 
    # 	 * @return The current resource observable flag
    # 	 
    @overloaded
    def isObservable(self):
        """ generated source for method isObservable """
        return self.getAttributes(LinkFormat.OBSERVABLE).size() > 0

    # 
    # 	 * This method sets the observable flag of this resource.
    # 	 * 
    # 	 * @param maximumSizeExtimate the resource maximum size estimate
    # 	 
    @isObservable.register(object, bool)
    def isObservable_0(self, observable):
        """ generated source for method isObservable_0 """
        if observable:
            self.setAttribute(LinkAttribute(LinkFormat.OBSERVABLE))
        else:
            self.clearAttribute(LinkFormat.OBSERVABLE)

    @overloaded
    def isHidden(self):
        """ generated source for method isHidden """
        return self.hidden

    @isHidden.register(object, bool)
    def isHidden_0(self, change):
        """ generated source for method isHidden_0 """
        self.hidden = change

    #  Sub-resource management /////////////////////////////////////////////////////
    # 
    # 	 * Removes this resource from its parent.
    # 	 
    def remove(self):
        """ generated source for method remove """
        if self.parent != None:
            self.parent.removeSubResource(self)

    # 
    # 	 * Counts the direct children of this resource.
    # 	 * 
    # 	 * @return The number of child resources
    # 	 
    def subResourceCount(self):
        """ generated source for method subResourceCount """
        return len(self.subResources) if self.subResources != None else 0

    # 
    # 	 * Counts the total number of sub-resources.
    # 	 * 
    # 	 * @return The total number of sub-resources
    # 	 
    def totalSubResourceCount(self):
        """ generated source for method totalSubResourceCount """
        return self.totalSubResourceCount

    # 
    # 	 * Returns the sorted set of sub-resources.
    # 	 * 
    # 	 * @return the sub-resource set
    # 	 
    def getSubResources(self):
        """ generated source for method getSubResources """
        if self.subResources == None:
            return Collections.emptySet()
        #  sorted sub-resources
        subs = TreeSet()
        for sub in subResources.values():
            subs.add(sub)
        return subs

    @overloaded
    def getResource(self, path):
        """ generated source for method getResource """
        return self.getResource(path, False)

    # 
    # 	 * Looks recursively for the resource specified by resourcePath. If the flag
    # 	 * create is set, a new resource of the same type as this will be created at
    # 	 * the given path.
    # 	 * 
    # 	 * @param path the path to the resource of interest
    # 	 * @param resource a resource that will be created at the given path or null for get only
    # 	 * @return The Resource of interest or null if not found and create is false
    # 	 
    @getResource.register(object, str, bool)
    def getResource_0(self, path, last):
        """ generated source for method getResource_0 """
        if path == None:
            return self
        #  find root for absolute path
        if path.startsWith("/"):
            while root.parent != None:
                root = root.parent
            path = None if path == "/" else path.substring(1)
            return root.getResource(path, last)
        pos = path.indexOf('/')
        head = None
        tail = None
        #  note: "some/resource/" addresses a resource "" under "resource"
        if pos != -1:
            head = path.substring(0, pos)
            tail = path.substring(pos + 1)
        else:
            head = path
        sub = self.subResources().get(head)
        if sub != None:
            return sub.getResource(tail, last)
        elif last:
            return self
        else:
            return None

    def add(self, resource):
        """ generated source for method add """
        if resource == None:
            raise NullPointerException()
        # print "TO ADD: " + resource.__name__;
        #  no absolute paths allowed, use root directly
        while resource.__name__.startsWith("/"):
            if self.parent != None:
                self.LOG.warning("Adding absolute path only allowed for root: made {:s} relative".format(resource.__name__))
            resource.setName(resource.__name__.substring(1))
        #  get last existing resource along path
        base = self.getResource(resource.__name__, True)
        #  compare paths
        path = self.getPath()
        if not path.endsWith("/"):
            path += "/"
        path += resource.__name__
        # print "NEWPATH: " + path;
        # print "BASPATH: " + base.getPath();
        path = path.substring(len(length))
        if path.startsWith("/"):
            path = path.substring(1)
        # print "DIFPATH: " + path;
        if path == "":
            #  resource replaces base
            # print "REPLACE: " + path;
            self.LOG.config("Replacing resource {:s}".format(base.getPath()))
            for r in base.getSubResources():
                r.parent = resource
                resource.subResources().put(r.__name__, r)
            resource.parent = base.parent
            base.parent.subResources().put(base.__name__, resource)
        else:
            #  resource is added to base
            self.LOG.config("Splitting up compound resource into {:d}: {:s}".format(resource.__name__,))
            resource.setName(segments[len(segments)])
            #  insert middle segments
            while i < len(segments):
                # print "NEW SEG";
                if isinstance(base, (RemoteResource,)):
                    sub = RemoteResource(segments[i])
                else:
                    sub = LocalResource(segments[i])
                sub.isHidden(True)
                base.add(sub)
                base = sub
                i += 1
            # print "ADDING: " + resource.__name__ + " to " + base.__name__;
            resource.parent = base
            base.subResources().put(resource.__name__, resource)
            # print "ADDED: " + resource.getPath();
        #  update number of sub-resources in the tree
        p = resource.parent
        while p != None:
            p.totalSubResourceCount += 1
            p = p.parent

    @overloaded
    def removeSubResource(self, resource):
        """ generated source for method removeSubResource """
        if resource != None:
            self.subResources().remove(resource.resourceIdentifier)
            #  update number of sub-resources in the tree
            while p != None:
                p.totalSubResourceCount -= 1
                p = p.parent
            resource.parent = None

    @removeSubResource.register(object, str)
    def removeSubResource_0(self, resourcePath):
        """ generated source for method removeSubResource_0 """
        self.removeSubResource(self.getResource(resourcePath))

    #
    # 	 * When implementing this method, {@link #add(Resource)} should be
    # 	 * used to keep sub-resource counting consistent.
    # 	 *
    # 	 * @param request the request carrying the data for creation
    # 	 * @param newIdentifier the name of the new sub-resource
    #
    def createSubResource(self, request, newIdentifier):
        """ generated source for method createSubResource """

    def compareTo(self, o):
        """ generated source for method compareTo """
        return self.getPath().compareTo(o.getPath())

    @overloaded
    def prettyPrint(self, out, intend):
        """ generated source for method prettyPrint """
        i = 0
        while i < intend:
            out.append(' ')
            i += 1
        out.printf("+[%s]", self.resourceIdentifier)
        title = self.getTitle()
        if title != None:
            out.printf(" %s", title)
        out.println()
        for attrib in self.getAttributes():
            if attrib.__name__ == LinkFormat.TITLE:
                continue
            while i < intend + 3:
                out.append(' ')
                i += 1
            out.printf("- %s\n", attrib.serialize())
        if self.subResources != None:
            for sub in self.subResources.values():
                sub.prettyPrint(out, intend + 2)

    @prettyPrint.register(object)
    def prettyPrint_0(self):
        """ generated source for method prettyPrint_0 """
        self.prettyPrint(System.out, 0)

    def subResources(self):
        """ Handles lazy creation of the sub-resources map. """
        if self.subResources == None:
            self.subResources = TreeMap()
        return self.subResources

Resource.LOG = Logger.getLogger(Resource.__class__.__name__)

