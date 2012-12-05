# coding=utf-8

"""
Proxy
An intermediary that mainly is concerned with forwarding requests
and relaying back responses, possibly performing caching,
namespace translation, or protocol translation in the process. As
opposed to intermediaries in the general sense, proxies generally
do not implement specific application semantics. Based on the
position in the overall structure of the request forwarding, there
are two common forms of proxy: forward-proxy and reverse-proxy.
In some cases, a single endpoint might act as an origin server,
forward-proxy, or reverse-proxy, switching behavior based on the
nature of each request.

Forward-Proxy
A "forward-proxy" is an endpoint selected by a client, usually via
local configuration rules, to perform requests on behalf of the
client, doing any necessary translations. Some translations are
minimal, such as for proxy requests for "coap" URIs, whereas other
requests might require translation to and from entirely different
application-layer protocols.

Reverse-Proxy
A "reverse-proxy" is an endpoint that stands in for one or more
other server(s) and satisfies requests on behalf of these, doing
any necessary translations. Unlike a forward-proxy, the client
may not be aware that it is communicating with a reverse-proxy; a
reverse-proxy receives requests as if it was the origin server for
the target resource.

Cross-Proxy
A cross-protocol proxy, or "cross-proxy" for short, is a proxy
that translates between different protocols, such as a CoAP-to-
HTTP proxy or an HTTP-to-CoAP proxy. While this specification
makes very specific demands of CoAP-to-CoAP proxies, there is more
variation possible in cross-proxies.
"""
import unittest

from pycolo.endpoint import Proxy

if __name__ == '__main__':
    unittest.main()

