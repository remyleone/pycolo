# coding=utf-8
from pycolo import Response, codes, LocalResource

from pycolo.codes import mediaCodes

class Query(LocalResource):
	"""
	This resource implements a test of specification for the
	ETSI IoT CoAP Plugtests, Paris, France, 24 - 25 March 2012.
	"""

	def __init__(self):
        self.title = "Resource accepting query parameters"

	def performGET(request):

		# create response
		response = Response(codes.RESP_CONTENT)
		
		payload = "Type: %d (%s)\nCode: %d (%s)\nMID: %d" %\
									 request.getType().ordinal(),\
									 request.typeString,\
									 request.code,\
									 request.MID
		
		for (Option query : request.getOptions(OptionNumberRegistry.URI_QUERY)):
			String keyValue[] = query.getStringValue().split("=")
			
			payload.append("\nQuery: ")
			payload.append(keyValue[0])
			if keyValue.length == 2:
				payload.append(": ");
				payload.append(keyValue[1])

		if payload.length() > 64:
			payload.delete(62, payload.length())
			payload.append('>>')

		# set payload
		response.payload = str(payload)
		response.contentType = mediaCodes.TEXT_PLAIN
		
		# complete the request
		request.respond(response)