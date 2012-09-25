# coding=utf-8

import logging

from pycolo.coap import Message
from pycolo.layers import TransactionLayer

import util.Properties


class ObservingManager(object):
    """
    The TokenManager stores all tokens currently used in transfers.
    New transfers can acquire unique tokens from the manager.
    """
    #  Logging ////////////////////////////////////////////////////////////////
    #  Inner class ////////////////////////////////////////////////////////////
    class ObservingRelationship(object):
        """ generated source for class ObservingRelationship """
        clientID = str()
        resourcePath = str()
        request = GETRequest()
        lastMID = int()

        def __init__(self, request):
            """ generated source for method __init__ """
            request.setMID(-1)
            self.clientID = request.getPeerAddress().__str__()
            self.resourcePath = request.getUriPath()
            self.request = request
            self.lastMID = -1

    singleton = ObservingManager()

    #  Maps a resource path string to the resource's observers stored by client address string. 
    observersByResource = HashMap()

    #  Maps a peer address string to the clients relationships stored by resource path. 
    observersByClient = HashMap()
    checkInterval = Properties.std.getInt("OBSERVING_REFRESH_INTERVAL")
    intervalByResource = HashMap()

    def __init__(self):
        """ generated source for method __init__ """

    @classmethod
    def getInstance(cls):
        """ generated source for method getInstance """
        return cls.singleton

    def setRefreshInterval(self, interval):
        """ generated source for method setRefreshInterval """
        self.checkInterval = interval

    def notifyObservers(self, resource):
        """ generated source for method notifyObservers """
        resourceObservers = self.observersByResource.get(resource.getPath())
        if resourceObservers != None and len(resourceObservers) > 0:
            logging.info("Notifying observers: {:d} @ {:s}".format(len(resourceObservers), resource.getPath()))
            #  get/initialize
            if not self.intervalByResource.containsKey(resource.getPath()):
                check = self.checkInterval
            else:
                check = self.intervalByResource.get(resource.getPath()) - 1
            #  update
            if check <= 0:
                self.intervalByResource.put(resource.getPath(), self.checkInterval)
                self.LOG.info("Refreshing observing relationship: {:s}".format(resource.getPath()))
            else:
                self.intervalByResource.put(resource.getPath(), check)
            for observer in resourceObservers.values():
                #  check
                if check <= 0:
                    request.setType(messageType.CON)
                else:
                    request.setType(messageType.NON)
                #  execute
                resource.performGET(request)
                prepareResponse(request)
                request.sendResponse()

    def prepareResponse(self, request):
        """ generated source for method prepareResponse """
        #  consecutive response require new MID that must be stored for RST matching
        if request.getResponse().getMID() == -1:
            request.getResponse().setMID(TransactionLayer.nextMessageID())
        #  16-bit second counter
        secs = int(((System.currentTimeMillis() - request.startTime) / 1000)) & 0xFFFF
        request.getResponse().setOption(Option(secs, OptionNumberRegistry.OBSERVE))
        #  store MID for RST matching
        updateLastMID(request.getPeerAddress().__str__(), request.getUriPath(), request.getResponse().getMID())


    # 	public synchronized void addObserver(GETRequest request, LocalResource resource) {
    # 		ObservingRelationship toAdd = new ObservingRelationship(request);
    #  get clients map for the given resource path
    # 		Map<String, ObservingRelationship> resourceObservers = observersByResource.get(resource.getPath());
    # 		if (resourceObservers==null) {
    #  lazy creation
    # 			resourceObservers = new HashMap<String, ObservingRelationship>();
    # 			observersByResource.put(resource.getPath(), resourceObservers);
    # 		}
    #  get resource map for given client address
    # 		Map<String, ObservingRelationship> clientObservees = observersByClient.get(request.getPeerAddress().__str__());
    # 		if (clientObservees==null) {
    #  lazy creation
    # 			clientObservees = new HashMap<String, ObservingRelationship>();
    # 			observersByClient.put(request.getPeerAddress().__str__(), clientObservees);
    # 		}
    #  save relationship for notifications triggered by resource
    # 		resourceObservers.put(request.getPeerAddress().__str__(), toAdd);
    #  save relationship for actions triggered by client
    # 		clientObservees.put(resource.getPath(), toAdd);
    # 		LOG.info(String.format("Established observing relationship: %s @ %s", request.getPeerAddress().__str__(), resource.getPath()));
    #  update response
    # 		request.getResponse().setOption(new Option(0, OptionNumberRegistry.OBSERVE));
    # 	}
    # 	public synchronized void removeObserver(String clientID) {
    # 		Map<String, ObservingRelationship> clientObservees = observersByClient.get(clientID);
    # 		if (clientObservees!=null) {
    # 			for (Map<String, ObservingRelationship> entry : observersByResource.values()) {
    # 				entry.remove(clientID);
    # 			}
    # 			observersByClient.remove(clientID);
    # 			LOG.info(String.format("Terminated all observing relationships for client: %s", clientID));
    # 		}
    # 	}

    @overloaded
    def removeObserver(self, clientID, resource):
        """
        Remove an observer by missing Observe option in GET.
        @param clientID the peer address as string
        @param resource the resource to un-observe.
        """
        resourceObservers = self.observersByResource.get(resource.getPath())
        clientObservees = self.observersByClient.get(clientID)
        if resourceObservers != None and clientObservees != None:
            if resourceObservers.remove(clientID) != None and clientObservees.remove(resource.getPath()) != None:
                logging.info("Terminated observing relationship by GET: {:s} @ {:s}".format(clientID, resource.getPath()))
                return
        #  should not be called if not existent
        logging.warning("Cannot find observing relationship: {:s} @ {:s}".format(clientID, resource.getPath()))

    @removeObserver.register(object, str, int)
    def removeObserver_0(self, clientID, mid):
        """
        Remove an observer by MID from RST.
        @param clientID the peer address as string
        @param mid the MID from the RST
        """
        toRemove = None
        clientObservees = self.observersByClient.get(clientID)
        if clientObservees != None:
            for entry in clientObservees.values():
                if mid == entry.lastMID and clientID == entry.clientID:
                    #  found it
                    toRemove = entry
                    break
        if toRemove != None:
            #  FIXME Inconsistent state check
            if resourceObservers == None:
                logging.severe("FIXME: ObservingManager has clientObservee, but no resourceObservers ({:s} @ {:s})".format(clientID, toRemove.resourcePath))
            if resourceObservers.remove(clientID) != None and clientObservees.remove(toRemove.resourcePath) != None:
                logging.info("Terminated observing relationship by RST: {:s} @ {:s}".format(clientID, toRemove.resourcePath))
                return
        self.LOG.warning("Cannot find observing relationship by MID: {:s}|{:d}".format(clientID, mid))

    def isObserved(self, clientID, resource):
        return self.observersByClient.containsKey(clientID) and self.observersByClient.get(clientID).containsKey(resource.getPath())

    def updateLastMID(self, clientID, path, mid):
        clientObservees = self.observersByClient.get(clientID)
        if clientObservees != None:
            if toUpdate != None:
                toUpdate.lastMID = mid
                self.LOG.finer("Updated last MID for observing relationship: {:s} @ {:s}".format(clientID, toUpdate.resourcePath))
                return
        logging.warning("Cannot find observing relationship to update MID: {:s} @ {:s}".format(clientID, path))
