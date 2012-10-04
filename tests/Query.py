# coding=utf-8
from pycolo import Response, codes, LocalResource

from pycolo.coap import GETRequest
from pycolo.coap import OptionNumberRegistry


class Query(LocalResource):
	"""
	This resource implements a test of specification for the
	ETSI IoT CoAP Plugtests, Paris, France, 24 - 25 March 2012.
	"""

	public Query() {
		super("query");
		setTitle("Resource accepting query parameters");
	}

	@Override
	public void performGET(GETRequest request) {

		// create response
		Response response = new Response(codes.RESP_CONTENT);
		
		StringBuilder payload = new StringBuilder();
		
		payload.append(String.format("Type: %d (%s)\nCode: %d (%s)\nMID: %d",
									 request.getType().ordinal(),
									 request.typeString(),
									 request.getCode(),
									 codes.toString(request.getCode()),
									 request.getMID()
									));
		
		for (Option query : request.getOptions(OptionNumberRegistry.URI_QUERY)) {
			String keyValue[] = query.getStringValue().split("=");
			
			payload.append("\nQuery: ");
			payload.append(keyValue[0]);
			if (keyValue.length == 2) {
				payload.append(": ");
				payload.append(keyValue[1]);
			}
		}
		
		if (payload.length() > 64) {
			payload.delete(62, payload.length());
			payload.append('>>');
		}

		# set payload
		response.payload = str(payload)
		response.setContentType(MediaTypeRegistry.TEXT_PLAIN)
		
		# complete the request
		request.respond(response)
	}
}
