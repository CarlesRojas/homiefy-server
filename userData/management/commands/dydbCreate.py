"""
    Extra commands
"""
from __future__ import print_function
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from userData.models import *

import sys,inspect

class Command(BaseCommand):
    help = 'Initializes a DynamoDB database. Creating all the needed Tables for this application'

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            '--verbose',
            action='store_true',
            dest='verbose',
            default=False,
            help='Verbose print all errors and DynamoDb query petitions',
        )

    def handle(self, *args, **options):
        #Loop all classes, look for dynamoDbTable classes and create them
        for name,obj in inspect.getmembers(sys.modules[__name__]):
            if not inspect.isclass(obj):
                continue
            if not issubclass(obj, dynamoDbTable):
                continue
            if obj.Name is None:
                continue

            print("Creating: ",obj.Name)

            try:
                obj.create_table(verbose=True)
                print("DONE")
            except Exception as e:
                if options['verbose']:
                    print(e)
                else:
                    if "preexisting table" in e.message:
                        print("Already created %s"%obj.Name)
                    else:
                        print("Can't create table %s"%obj.Name)
                        print(e.message)

