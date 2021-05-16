from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from userData.serializers import *
from userData.models      import *
import homiefy.constants as CT
from datetime import datetime
from decimal import Decimal
import decimal
import uuid

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
        
        utilities =  {u.name: {"username":u.username,"price": u.price,"people": u.people,"period": u.period,"lastPayment": u.lastPayment, "picture": u.picture} for u in utilities}

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
        picture = in_data.validated_data.get('picture')

        dydbInst = UtilitiesTable.filter(username=username,
                                        name=name)

        package = {
            "username" : username,
            "name" : name,
            "price" : price,
            "people" : people,
            "period" : period,
            "lastPayment" : lastPayment,
            "picture" : picture,
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







class AddBalance(APIView):
    #permission_classes = (AllowAny, )

    def post(self, request, format=None):
        """
        Adds a expense to the users balance
        ---
        many: False
        parameters:
            - name : body
              pytype: newExpenseSerializer
              paramType: body
              description : Expenses data
        responseMessages:
            - code: 200
              message: error 0. All okey
            - code: 500
              message: error 108. Internal server error
        """
        in_data = newExpenseSerializer(data=request.data)
        in_data.is_valid(raise_exception=True)

        username    = in_data.validated_data.get('username')
        name        = in_data.validated_data.get('name')
        people      = in_data.validated_data.get('people')
        price       = in_data.validated_data.get('price')
        name        = in_data.validated_data.get('name')

        print
        print
        print
        pricePerPerson = Decimal(price/len(people))

        TWO_PLACES = decimal.Decimal("0.01")
        pricePerPerson = pricePerPerson.quantize(TWO_PLACES)

        people.remove(username)


        expenses = ExpensesTable.filter(username =username)
        if expenses:
            expenseUser = expenses[0]
        else:
            package = {
                "username" : username,
                "balance" : {},
            }
            expenseUser = ExpensesEntry(**package)
    

        for person in people:
            expenses = ExpensesTable.filter(username =person)
            if expenses:
                expenses = expenses[0]
            else:
                package = {
                    "username" : person,
                    "balance" : {},
                }

                expenses = ExpensesEntry(**package)

            print expenses.username
            print expenses.balance
            if username in expenses["balance"]:
                
                sumExpenses = 0
                for key in expenses["balance"][username]:
                    sumExpenses +=expenses["balance"][username][key]
                
                print "SUM EXPENSES: ", sumExpenses
                
                #si ja li deviem diners li sumem si ja existia la categoria o creem la caeoria de 0
                if sumExpenses <= 0:

                    if name in expenses["balance"][username]: 
                        print "CASE 1"
                        expenses["balance"][username][name] += pricePerPerson
                        expenseUser["balance"][person][name]+= pricePerPerson * -1
                    else:
                        print "CASE 2"
                        expenses["balance"][username][name] = pricePerPerson
                        expenseUser["balance"][person][name] = pricePerPerson * -1
                
                else:
                    if sumExpenses < abs(pricePerPerson):
                        rest = pricePerPerson + sumExpenses

                        print "CASE 3"
                        expenses["balance"][username] = {}
                        expenses["balance"][username][name] = rest

                        print "REST: ", pricePerPerson, "+", sumExpenses, "=", rest
                        expenseUser["balance"][person]  = {}
                        expenseUser["balance"][person][name] = rest * -1
                    
                    else:
                        #we have to decrease expenses proportinoal to 
                        print "CASE 4"
                        for key in  expenses["balance"][username]:
                            expenses["balance"][username][key] += pricePerPerson*(expenses["balance"][username][key]/sumExpenses)
                            expenseUser["balance"][person][key] += pricePerPerson*(expenseUser["balance"][person][key]/sumExpenses)
                        


            else:
                print "CASE 5"
                expenses["balance"][username] = {}
                expenses["balance"][username][name] = pricePerPerson

                expenseUser["balance"][person]  = {}
                expenseUser["balance"][person][name] = pricePerPerson * -1
            
            expenses["balance"][username] = {x:y for x,y in expenses["balance"][username].items() if y!=0}
            expenses["balance"] = {x:y for x,y in expenses["balance"].items() if y}

            expenseUser["balance"][person] = {x:y for x,y in expenseUser["balance"][person].items() if y!=0}
            expenseUser["balance"] = {x:y for x,y in expenseUser["balance"].items() if y}

            
            
            print expenses.balance
            print "-"*60
            print
            expenses.save()


        print expenseUser.balance

        expenseUser.save()

        return Response( {'Error': 0}, status=status.HTTP_200_OK)


class Balance(APIView):
    #permission_classes = (AllowAny, )

    def post(self, request, format=None):
        """
        Retrive a user Balance.
        ---
        many: False
        parameters:
            - name : body
              pytype: ExpenseSelectorSerializer
              paramType: body
              description : Expenses data
        responseMessages:
            - code: 200
              message: error 0. All okey
            - code: 500
              message: error 108. Internal server error
        """
        in_data = ExpenseSelectorSerializer(data=request.data)
        in_data.is_valid(raise_exception=True)

        username    = in_data.validated_data.get('username')

        expenses = ExpensesTable.filter(username =username)
        if expenses:
            expenseUser = expenses[0]
        else:
            package = {
                "username" : username,
                "balance" : {},
            }
            expenseUser = ExpensesEntry(**package)
        
        return Response( expenseUser.balance, status=status.HTTP_200_OK)
    
def multikeysort(items, columns):
    from operator import itemgetter
    comparers = [((itemgetter(col[1:].strip()), -1) if col.startswith('-') else
                  (itemgetter(col.strip()), 1)) for col in columns]
    def comparer(left, right):
        for fn, mult in comparers:
            result = cmp(fn(left), fn(right))
            if result:
                return mult * result
        else:
            return 0
    return sorted(items, cmp=comparer)



class Postit(APIView):
    #permission_classes = (AllowAny, )

    def post(self, request, format=None):
        """
        Store a postit.
        ---
        many: False
        parameters:
            - name : body
              pytype: PostitSerializer
              paramType: body
              description : Expenses data
        responseMessages:
            - code: 200
              message: error 0. All okey
            - code: 500
              message: error 108. Internal server error
        """
        in_data = PostitSerializer(data=request.data)
        in_data.is_valid(raise_exception=True)

        username        = in_data.validated_data.get('username')
        message         = in_data.validated_data.get("message")
        priorityType    = in_data.validated_data.get("priorityType")
        people          = in_data.validated_data.get("people")
        period          = in_data.validated_data.get("period")
        createdDate          = in_data.validated_data.get("createdDate")

        _uuid = str(uuid.uuid1())
        dydbInst = PostitTable.filter(username=username, id = _uuid)

        package = {
            "username" : username,
            "id":_uuid,
            "message" : message,
            "priorityType" : priorityType,
            "people" : people,
            "period" : period,
            "createdDate": createdDate,
        }

        c = PostitEntry(**package)
        c.save()

        return Response( {'Error': 0}, status=status.HTTP_200_OK)
    
    def get(self, request, format=None):
        """
        Returns all the postits
        ---
        response_serializer: UtilityDictSerializer
        many: False
        responseMessages:
            - code: 200
              message: error 0. Mail sended.
            - code: 500
              message: error 108. Internal mail server error
        """

        postits = []
        for user in CT.USERNAMES:
            postits += PostitTable.filter(username =user)

        postits = [{"username":p.username, "message":p.message, "priorityType": p.priorityType,
                     "people":p.people, "period":p.period, "uuid": p.id, "createdDate": p.createdDate}for p in postits]

        a = multikeysort(postits, ['-priorityType', 'period'])
        print a

        return Response( {"response":a}, status=status.HTTP_200_OK)

    def delete(self, request, format=None):
        """
        Deletes a postit
        ---
        many: False
        parameters:
            - name : body
              pytype: PostitSelectorSerializer
              paramType: body
              description : Invoicing data
        responseMessages:
            - code: 200
              message: error 0. All okey
            - code: 500
              message: error 108. Internal server error
        """
        in_data = PostitSelectorSerializer(data=request.data)
        in_data.is_valid(raise_exception=True)


        username    = in_data.validated_data.get('username')
        uuiid        = in_data.validated_data.get('uuid')


        dydbInst = PostitTable.filter(username=username,
                                        id=uuiid)

        if dydbInst:
            dydbInst[0].delete()

        return Response( {'Error': 0}, status=status.HTTP_200_OK)

        

class List(APIView):
    #permission_classes = (AllowAny, )

    def post(self, request, format=None):
        """
        Store a element to the list.
        ---
        many: False
        parameters:
            - name : body
              pytype: ListSerializer
              paramType: body
              description : Expenses data
        responseMessages:
            - code: 200
              message: error 0. All okey
            - code: 500
              message: error 108. Internal server error
        """
        in_data = ListSerializer(data=request.data)
        in_data.is_valid(raise_exception=True)

        name            = in_data.validated_data.get('name')
        people          = in_data.validated_data.get("people")
        price           = in_data.validated_data.get("price")

        _uuid = str(uuid.uuid1())
        print _uuid
        dydbInst = ListTable.filter(username="list",  id = _uuid)

        package = {
            "username" : "list",
            "name" : name,
            "id":_uuid,
            "people" : people,
            "price" : price,
        }

        c = ListEntry(**package)
        c.save()

        return Response( {'Error': 0}, status=status.HTTP_200_OK)
    
    def get(self, request, format=None):
        """
        Returns all the postits
        ---
        response_serializer: UtilityDictSerializer
        many: False
        responseMessages:
            - code: 200
              message: error 0. Mail sended.
            - code: 500
              message: error 108. Internal mail server error
        """

        postits = []
        postits += ListTable.filter(username ="list")

        postits = [{"name":p.name, "price":p.price,
                     "people":p.people,"uuid": p.id}for p in postits]

        a = multikeysort(postits, ['name'])
        print a

        return Response( {"response":a}, status=status.HTTP_200_OK)

    def delete(self, request, format=None):
        """
        Deletes a postit
        ---
        many: False
        parameters:
            - name : body
              pytype: ListSelectorSerializer
              paramType: body
              description : Invoicing data
        responseMessages:
            - code: 200
              message: error 0. All okey
            - code: 500
              message: error 108. Internal server error
        """
        in_data = ListSelectorSerializer(data=request.data)
        in_data.is_valid(raise_exception=True)


        uuiid        = in_data.validated_data.get('uuid')


        dydbInst = ListTable.filter(username="list",
                                        id=uuiid)

        if dydbInst:
            dydbInst[0].delete()

        return Response( {'Error': 0}, status=status.HTTP_200_OK)
