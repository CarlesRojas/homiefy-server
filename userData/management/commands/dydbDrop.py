"""
    Extra commands
"""
from __future__ import print_function
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from userData.models import *


import sys,inspect
import boto3

from django.conf import settings

def confirm(prompt=None, resp=False):
    """prompts for yes or no response from the user. Returns True for yes and
    False for no.

    'resp' should be set to the default value assumed by the caller when
    user simply types ENTER.

    >>> confirm(prompt='Create Directory?', resp=True)
    Create Directory? [y]|n:
    True
    >>> confirm(prompt='Create Directory?', resp=False)
    Create Directory? [n]|y:
    False
    >>> confirm(prompt='Create Directory?', resp=False)
    Create Directory? [n]|y: y
    True

    """

    if prompt is None:
        prompt = 'Confirm'

    if resp:
        prompt = '%s [%s]|%s: ' % (prompt, 'y', 'n')
    else:
        prompt = '%s [%s]|%s: ' % (prompt, 'n', 'y')

    while True:
        ans = raw_input(prompt)
        if not ans:
            return resp
        if ans not in ['y', 'Y', 'n', 'N']:
            print('please enter y or n.')
            continue
        if ans == 'y' or ans == 'Y':
            return True
        if ans == 'n' or ans == 'N':
            return False

class Command(BaseCommand):
    help = 'Initializes a DynamoDB database. Creating all the needed Tables for this application'

    def add_arguments(self, parser):
        parser.add_argument('dbname', nargs='+')
        pass

    def handle(self, *args, **options):
        tablesToDrop = []

        for dbname in options['dbname']:
            tablesToDrop.append(dbname)

        if 'all' in tablesToDrop:
            #Loop all classes, look for dynamoDbTable classes and create them
            for name,obj in inspect.getmembers(sys.modules[__name__]):

                if not inspect.isclass(obj):
                    continue
                if not issubclass(obj, dynamoDbTable):
                    continue
                if obj.Name is None:
                    continue

                print("Delete %s"%obj.Name)

                try:
                    obj.delete_table()
                    print("Deleted")
                except Exception as e:
                    print("Can't delete table %s"%obj.Name)
        else:

            if settings.DEBUG:
                dydbClient = boto3.client('dynamodb',
                        region_name='us-west-1',
                        endpoint_url="http://%s:%s"% ( settings.DYNAMODB_HOST, settings.DYNAMODB_PORT))
            else:
                confirm(prompt='Pointing to Production Dydb. Are you sure you want to drop that Database?', resp=False)
                dydbClient = boto3.client('dynamodb',
                        region_name=settings.AWS_REGION)

            for tname in tablesToDrop:
                table = dydbClient.delete_table(TableName = tname)

            #delete by name
