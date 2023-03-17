from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser,FileUploadParser
# Create your views here.
@api_view(['post','get'])
def test(request):
    return Response("okay")

    

class upl(APIView):
    parser_classes = (FormParser,MultiPartParser,FileUploadParser)

    def get(self, request):
        return Response("GET API")

    def post(self, request):
        print(request.data)
        try:
            file = request.data['file']
            print(str(file))
            # print(request.FILES,request.data)
            file_uploaded = request.data['file']
            content_type = file_uploaded.content_type
            response = "POST API and you have uploaded a {} file".format(content_type)
        except Exception as e:
            response = "please select file"
        return Response({"message":response,
                         "status":200})