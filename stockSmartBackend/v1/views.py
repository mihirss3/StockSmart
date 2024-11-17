from rest_framework.response import Response
from rest_framework.views import APIView

class IndexView(APIView):
    def get(self, request):
        return Response({"message": ""})

class HelloView(APIView):
    def get(self, request):
        return Response({"message": "Hello"})

class WorldView(APIView):
    def get(self, request):
        return Response({"message": "World"})
