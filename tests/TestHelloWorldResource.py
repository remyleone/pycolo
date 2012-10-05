# coding=utf-8
from pycolo import Resource
from pycolo.Response import Response
from pycolo.codes import mediaCodes, codes


class HelloWorldResource(Resource):
    """
    This class implements a 'hello world' resource for demonstration purposes.
    Defines a resource that returns text with special characters on GET.
    """

    def __init__(self, title="helloWorld", rt="HelloWorldDisplayer"):
        self.title = title
        self.resourceType = rt

    def performGET(self, request):
        # create response
        response = Response(code=codes.RESP_CONTENT)

        payload = "Hello World! My name is Rémy Léone look @ the funny €"
        response.contentType(mediaCodes.text)
        response.payload = payload
        return response