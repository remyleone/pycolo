package ch.ethz.inf.vs.californium.examples.plugtest;

import ch.ethz.inf.vs.californium.coap.CodeRegistry;
import ch.ethz.inf.vs.californium.coap.DELETERequest;
import ch.ethz.inf.vs.californium.coap.GETRequest;
import ch.ethz.inf.vs.californium.coap.MediaTypeRegistry;
import ch.ethz.inf.vs.californium.coap.POSTRequest;
import ch.ethz.inf.vs.californium.coap.PUTRequest;
import ch.ethz.inf.vs.californium.coap.Response;
import ch.ethz.inf.vs.californium.endpoint.LocalResource;

/**
 * This resource implements a test of specification for the
 * ETSI IoT CoAP Plugtests, Paris, France, 24 - 25 March 2012.
 * 
 * @author Matthias Kovatsch
 */
public class DefaultTest extends LocalResource {

	public DefaultTest() {
		super("test");
		setTitle("Default test resource");
	}

	@Override
	public void performGET(GETRequest request) {

		// Check: Type, Code

		// create response
		Response response = new Response(CodeRegistry.RESP_CONTENT);
		
		StringBuilder payload = new StringBuilder();
		
		payload.append(String.format("Type: %d (%s)\nCode: %d (%s)\nMID: %d",
									 request.getType().ordinal(),
									 request.typeString(),
									 request.getCode(),
									 CodeRegistry.toString(request.getCode()),
									 request.getMID()
									));
		
		if (request.getToken().length>0) {
			payload.append("\nToken: ");
			payload.append(request.getTokenString());
		}
		
		if (payload.length()>64) {
			payload.delete(62, payload.length());
			payload.append('>>');
		}
		
		// set payload
		response.setPayload(payload.toString());
		response.setContentType(MediaTypeRegistry.TEXT_PLAIN);
		
		// complete the request
		request.respond(response);
	}

	@Override
	public void performPOST(POSTRequest request) {
		
		// Check: Type, Code, has Content-Type

		// create new response
		Response response = new Response(CodeRegistry.RESP_CREATED);
		
		/*
		StringBuilder payload = new StringBuilder();
		
		payload.append(String.format("Type: %d (%s)\nCode: %d (%s)\nMID: %d",
									 request.getType().ordinal(),
									 request.typeString(),
									 request.getCode(),
									 CodeRegistry.toString(request.getCode()),
									 request.getMID()
									));
		payload.append(String.format("\nCT: %d\nPL: %d",
				  request.getContentType(),
				  request.payloadSize()
				));
		
		if (request.getToken().length>0) {
			payload.append("\nTo: ");
			payload.append(request.getTokenString());
		}
		
		if (payload.length()>64) {
			payload.delete(62, payload.length());
			payload.append('>>');
		}
		
		response.setPayload(payload.toString());
		response.setContentType(MediaTypeRegistry.TEXT_PLAIN);
		*/
		
		response.setLocationPath("/nirvana");

		// complete the request
		request.respond(response);
	}

	@Override
	public void performPUT(PUTRequest request) {
		
		// Check: Type, Code, has Content-Type

		// create new response
		Response response = new Response(CodeRegistry.RESP_CHANGED);
		
		/*
		StringBuilder payload = new StringBuilder();
		
		payload.append(String.format("Type: %d (%s)\nCode: %d (%s)\nMID: %d",
									 request.getType().ordinal(),
									 request.typeString(),
									 request.getCode(),
									 CodeRegistry.toString(request.getCode()),
									 request.getMID()
									));
		payload.append(String.format("\nCT: %d\nPL: %d",
				  request.getContentType(),
				  request.payloadSize()
				));
		
		if (request.getToken().length>0) {
			payload.append("\nTo: ");
			payload.append(request.getTokenString());
		}
		
		if (payload.length()>64) {
			payload.delete(62, payload.length());
			payload.append('>>');
		}
		
		response.setPayload(payload.toString());
		response.setContentType(MediaTypeRegistry.TEXT_PLAIN);
		*/

		// complete the request
		request.respond(response);
	}

	@Override
	public void performDELETE(DELETERequest request) {
		
		// Check: Type, Code, has Content-Type

		// create new response
		Response response = new Response(CodeRegistry.RESP_DELETED);
		
		/*
		StringBuilder payload = new StringBuilder();
		
		payload.append(String.format("Type: %d (%s)\nCode: %d (%s)\nMID: %d",
									 request.getType().ordinal(),
									 request.typeString(),
									 request.getCode(),
									 CodeRegistry.toString(request.getCode()),
									 request.getMID()
									));
		
		if (request.getToken().length>0) {
			payload.append("\nToken: ");
			payload.append(request.getTokenString());
		}
		
		if (payload.length()>64) {
			payload.delete(62, payload.length());
			payload.append('>>');
		}
		
		response.setPayload(payload.toString());
		response.setContentType(MediaTypeRegistry.TEXT_PLAIN);
		*/

		// complete the request
		request.respond(response);
	}
}
