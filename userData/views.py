from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from userData.serializers import *
from userData.models      import *
import homiefy.constants as CT
from datetime import datetime



class utilities(APIView):
    #permission_classes = (AllowAny, )

    def get(self, request, format=None):
        """
        Returns all the utilities
        ---
        response_serializer: UtilityDictSerializer
        many: False
        responseMessages:
            - code: 200
              message: error 0. Mail sended.
            - code: 500
              message: error 108. Internal mail server error
        """

        utilities = []
        for user in CT.USERNAMES:
            utilities += UtilitiesTable.filter(username =user)
        
        utilities =  {u.name: {"username":u.username,"price": u.price,"people": u.people,"period": u.period,"lastPayment": u.lastPayment} for u in utilities}

        serializer = UtilityDictSerializer(data=utilities)

        if not serializer.is_valid():
            print serializer.errors

        return Response( utilities, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        """
        Adds a utility
        ---
        many: False
        parameters:
            - name : body
              pytype: UtilitySerializer
              paramType: body
              description : Invoicing data
        responseMessages:
            - code: 200
              message: error 0. All okey
            - code: 500
              message: error 108. Internal server error
        """
        in_data = UtilitySerializer(data=request.data)
        in_data.is_valid(raise_exception=True)


        username    = in_data.validated_data.get('username')
        name        = in_data.validated_data.get('name')
        price       = in_data.validated_data.get('price')
        people      = in_data.validated_data.get('people')
        period      = in_data.validated_data.get('period')
        lastPayment = in_data.validated_data.get('lastPayment')

        dydbInst = UtilitiesTable.filter(username=username,
                                        name=name)

        package = {
            "username" : username,
            "name" : name,
            "price" : price,
            "people" : people,
            "period" : period,
            "lastPayment" : lastPayment,
        }

        c = UtilitiesEntry(**package)
        c.save()

        return Response( {'Error': 0}, status=status.HTTP_200_OK)


    def delete(self, request, format=None):
        """
        Deletes a utility
        ---
        many: False
        parameters:
            - name : body
              pytype: UtilitySelectorSerializer
              paramType: body
              description : Invoicing data
        responseMessages:
            - code: 200
              message: error 0. All okey
            - code: 500
              message: error 108. Internal server error
        """
        in_data = UtilitySelectorSerializer(data=request.data)
        in_data.is_valid(raise_exception=True)


        username    = in_data.validated_data.get('username')
        name        = in_data.validated_data.get('name')


        dydbInst = UtilitiesTable.filter(username=username,
                                        name=name)

        if dydbInst:
            dydbInst[0].delete()

        return Response( {'Error': 0}, status=status.HTTP_200_OK)
