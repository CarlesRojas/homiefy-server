from __future__ import unicode_literals

from django.db import models
from libs.dynamodb import dynamoDbInstance, dynamoDbTable
# Create your models here.

class UtilitiesEntry(dynamoDbInstance):
    """
        Table holding the Utilities of the house
    """
    VALID_CONSTRUCTOR_KEYS = ['username',
                              'name',        #name of the utility
                              'price',       #price of the utility
                              'people',      #people that uses that utility
                              'period',      #days of the utility period
                              'lastPayment', #date of the last payment
                              ]

    def __init__(self, **kwargs):
        self.constructor(**kwargs)
        self.DYDB_TABLE = UtilitiesTable


class UtilitiesTable(dynamoDbTable):
    """
        Table with the utilities
    """

    Name = 'Utilities'
    DataInstanceFactory = UtilitiesEntry

    AttributeDefinitions = [
        {'AttributeName': 'username',          'AttributeType': 'S'},
        {'AttributeName': 'name',      'AttributeType': 'S'},
    ]


    KeySchema = [
        {'AttributeName': 'username',   'KeyType': 'HASH'},
        {'AttributeName': 'name',  'KeyType': 'RANGE'},
    ]

    ProvisionedThroughput = {
        'ReadCapacityUnits':  10,
        'WriteCapacityUnits': 10
    }
