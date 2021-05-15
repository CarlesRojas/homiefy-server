from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import FileResponse, HttpResponse

from fileManager.serializers import *

import homiefy.constants as CT

import base64

class profilePic(APIView):
    #permission_classes = (AllowAny, )

    def post(self, request, format=None):
        """
        Returns the profile Pic of a User.
        ---
        many: False
        parameters:
            - name : body
              pytype: profilePicSerializer
              paramType: body
              description : Invoicing data
        responseMessages:
            - code: 200
              message: error 0. Mail sended.
            - code: 500
              message: error 108. Internal mail server error
        """
        in_data = profilePicSerializer(data=request.data)
        in_data.is_valid(raise_exception=True)


        username    = in_data.validated_data.get('username')

        try:
            imgPath = CT.PROFILEPICDIR + username +".jpg"
            #image_data = open(imgPath, 'rb')
            with open(imgPath, "rb") as image_file:
                image_data = base64.b64encode(image_file.read()).decode('utf-8')
            ctx = {}
            ctx["image"] = image_data

        except IOError:
            return Response( {'Error': "File not Found"}, status=status.HTTP_200_OK)

        response = HttpResponse(ctx, content_type="image/png")

        
        return response

        #return render(request, 'index.html', ctx)

