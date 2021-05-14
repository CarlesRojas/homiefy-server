from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from userData.serializers import *

class debts(APIView):
    #permission_classes = (AllowAny, )

    def get(self, request, format=None):
        """
        Returns the debt betweens all the house members
        ---
        response_serializer: debtResposeSerializer
        many: True
        responseMessages:
            - code: 200
              message: error 0. Mail sended.
            - code: 500
              message: error 108. Internal mail server error
        """
        pass
