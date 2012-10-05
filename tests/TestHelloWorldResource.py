# coding=utf-8
from pycolo import Resource


class HelloWorldResource(Resource):
    """
    This class implements a 'hello world' resource for demonstration purposes.
    Defines a resource that returns text with special characters on GET.
    """

    public
    HelloWorldResource(String
    custom, String
    title, String
    rt) {
    super(custom);
    setTitle(title);
    setResourceType(rt);
    }

    public
    HelloWorldResource()
    {
    this("helloWorld", "GET a friendly greeting!", "HelloWorldDisplayer");
    }

    @Override

    public
    void
    performGET(GETRequest
    request) {

             // create
    response
    Response
    response = new
    Response(CodeRegistry.RESP_CONTENT);

    // set
    payload
    response.setPayload(
        "Hello World! Some umlauts: äöü\n\nZalgo: C͓̦̭̹̭͎͖̗̗̊Ȱ̬̥͚͚̏͛ͩ͆̎̿̈͝A̵̴̡̩̞͇̱͓͎̾P͎ͤͦ͆̍͋͒̽̂ͮ͠ͅ ̧̯̟̑ͫ͑͑͢͡R͈̜͍̄͌̄ͣͅU̥̭͓͉̟̳͗̈́̂L͎̘̪͓̟̩͌ͮͧ͞Ẽ̴̖̳̘̌̉ͯ͋̽̔Z̠̣̩̫͚͇̬̲͛ͮ̓ͧͨ̕");
    response.setContentType(MediaTypeRegistry.TEXT_PLAIN);

    // complete
    the
    request
    request.respond(response);
    }

}
