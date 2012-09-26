/*******************************************************************************
 * Copyright (c) 2012, Institute for Pervasive Computing, ETH Zurich.
 * All rights reserved.
 * 
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 * 3. Neither the name of the Institute nor the names of its contributors
 *    may be used to endorse or promote products derived from this software
 *    without specific prior written permission.
 * 
 * THIS SOFTWARE IS PROVIDED BY THE INSTITUTE AND CONTRIBUTORS "AS IS" AND
 * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED.  IN NO EVENT SHALL THE INSTITUTE OR CONTRIBUTORS BE LIABLE
 * FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
 * OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
 * HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 * LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
 * OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
 * SUCH DAMAGE.
 * 
 * This file is part of the Californium (Cf) CoAP framework.
 ******************************************************************************/
package ch.ethz.inf.vs.californium.examples.resources;

import ch.ethz.inf.vs.californium.coap.CodeRegistry;
import ch.ethz.inf.vs.californium.coap.GETRequest;
import ch.ethz.inf.vs.californium.coap.MediaTypeRegistry;
import ch.ethz.inf.vs.californium.coap.Response;
import ch.ethz.inf.vs.californium.endpoint.LocalResource;

/**
 * This class implements a 'hello world' resource for demonstration purposes.
 * Defines a resource that returns text with special characters on GET.
 * 
 * @author Dominique Im Obersteg, Daniel Pauli, and Matthias Kovatsch
 */
public class HelloWorldResource extends LocalResource {

	public HelloWorldResource(String custom, String title, String rt) {
		super(custom);
		setTitle(title);
		setResourceType(rt);
	}
	
	public HelloWorldResource() {
		this("helloWorld", "GET a friendly greeting!", "HelloWorldDisplayer");
	}

	@Override
	public void performGET(GETRequest request) {

		// create response
		Response response = new Response(CodeRegistry.RESP_CONTENT);

		// set payload
		response.setPayload("Hello World! Some umlauts: äöü\n\nZalgo: C͓̦̭̹̭͎͖̗̗̊Ȱ̬̥͚͚̏͛ͩ͆̎̿̈͝A̵̴̡̩̞͇̱͓͎̾P͎ͤͦ͆̍͋͒̽̂ͮ͠ͅ ̧̯̟̑ͫ͑͑͢͡R͈̜͍̄͌̄ͣͅU̥̭͓͉̟̳͗̈́̂L͎̘̪͓̟̩͌ͮͧ͞Ẽ̴̖̳̘̌̉ͯ͋̽̔Z̠̣̩̫͚͇̬̲͛ͮ̓ͧͨ̕");
		response.setContentType(MediaTypeRegistry.TEXT_PLAIN);

		// complete the request
		request.respond(response);
	}
}
