# coding=utf-8

"""
The TokenManager stores all tokens currently used in transfers.
New transfers can acquire unique tokens from the manager.
"""

import logging
import time
from pycolo.codes import options
from pycolo import OBSERVING_REFRESH_INTERVAL


# Maps a resource path string to the resource's observers stored by client
# address string.
uri2client = dict()

checkInterval = OBSERVING_REFRESH_INTERVAL
intervalByResource = dict()


def isObserved(uri):
    return uri in uri2client


def notifyObservers(resource):
    raise NotImplementedError
#    if resource.path in uri2client:
#        observers = uri2client(resource.path)
#        if observers:
#            logging.info("Notifying %d observers about %s" % len(observers), resource.path)
#            #  get/initialize
#            if resource.path not in intervalByResource:
#                check = checkInterval
#            else:
#                check = intervalByResource[resource.path] - 1
#            #  update
#            if check <= 0:
#                intervalByResource[resource.path] = checkInterval
#                logging.info("Refreshing observing relationship: %s" % resource.path)
#            else:
#                intervalByResource.put(resource.getPath(), check)
#            for observer in observers:
#                request = Request()
#                if check <= 0:  #  check
#                    request.type(msgType.CON)
#                else:
#                    request.type(msgType.NON)
#                #  execute
#                resource.get(request)
#                prepareResponse(request)
#                request.sendResponse()


def updateLastMID(clientID, path, mid):
    raise NotImplementedError
#    clientObservees = client2uri[clientID]
#    if clientObservees is not None:
#        if toUpdate is not None:
#            toUpdate.lastMID = mid
#            logging.info("Updated last MID for observing relationship: %s @ %s"\
#            .format(clientID, toUpdate.resourcePath))
#            return
#    logging.warning("Cannot find observing relationship to update MID: {:s} @ {:s}"\
#    .format(clientID, path))


def prepareResponse(request):
    """
    consecutive response require new MID that must be stored for RST matching
    :param request:
    """
    raise NotImplementedError
#    if request.response.MID == -1:
#        request.getResponse().setMID(TransactionLayer.nextMessageID())
#    #  16-bit second counter
#    secs = ((round(time.time() * 1000) - request.startTime) / 1000) & 0xFFFF
#    request.getResponse().setOption(Option(secs, options.OBSERVE))
#    #  store MID for RST matching
#    updateLastMID(str(request.peer), request.uri, request.response.MID)


def addObserver(request, resource):
    """
    get clients map for the given resource path
    :param request:
    :param resource:
    """
    raise NotImplementedError
#    Map<String, ObservingRelationship> resourceObservers = observersByResource.get(resource.getPath())
#
#    if not resourceObservers:
#        #  lazy creation
#        resourceObservers = dict()
#        observersByResource[resource.getPath()] = resourceObservers
#        #  get resource map for given client address
#        Map<String, ObservingRelationship> clientObservees = observersByClient.get(request.getPeerAddress().__str__())
#
#    if not clientObservees:
#        #  lazy creation
#        clientObservees = dict()
#        observersByClient.put(str(request.peerAddress), clientObservees)
#
#    #  save relationship for notifications triggered by resource
#    resourceObservers.put(str(request.peerAddress), toAdd)
#    #  save relationship for actions triggered by client
#    clientObservees.put(resource.path, toAdd)
#    logging.info("Established observing relationship: %s @ %s", str(request.peerAddress), resource.path)
#    #  update response
#    request.response.options[0, options.OBSERVE]


def removeObserver(client, resource=None, mid=None):
    """
    Remove a selected observer from observation structures.
    Remove an observer by MID from RST.
    :param mid: the MID from the RST
    :param resource: the resource to un-observe.
    :param client: the peer address as string.
    """
    raise NotImplementedError
#    if mid:
#        if client2uri[client]:
#            for entry in clientObservees.values():
#                if mid == entry.lastMID and client == entry.clientID:  # found it
#                    del(entry)
#                    logging.info("Terminated observing relationship by RST: {:s} @ {:s}"\
#                    .format(client, toRemove.resourcePath))
#                    return
#        return
#    if resource:
#        client2uri[client].remove(resource)
#        uri2client[resource].remove(client)
#        logging.info("Terminated observing relationship: %s @ %s".format(resource, client))
#        return
#    if client in client2uri:
#        for entry in client2uri[client]:
#            entry.remove(client)
#        del(client2uri[client])
#        logging.info("Terminated all observing relationships for client: %s" % client)
#        return
#    #  should not be called if not existent
#    logging.warning("Cannot find observing relationship: %s @ %s".format(resource, client))
