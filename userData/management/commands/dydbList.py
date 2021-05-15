"""
    Extra commands
"""
from __future__ import print_function
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from tabulate import tabulate

import boto3    #DynamoDB
from libs.dynamodb import getDyDbClient

def bytes_2_human_readable(number_of_bytes):
    if number_of_bytes < 0:
        raise ValueError("!!! numberOfBytes can't be smaller than 0 !!!")

    step_to_greater_unit = 1024.

    number_of_bytes = float(number_of_bytes)
    unit = 'bytes'

    if (number_of_bytes / step_to_greater_unit) >= 1:
        number_of_bytes /= step_to_greater_unit
        unit = 'KB'

    if (number_of_bytes / step_to_greater_unit) >= 1:
        number_of_bytes /= step_to_greater_unit
        unit = 'MB'

    if (number_of_bytes / step_to_greater_unit) >= 1:
        number_of_bytes /= step_to_greater_unit
        unit = 'GB'

    if (number_of_bytes / step_to_greater_unit) >= 1:
        number_of_bytes /= step_to_greater_unit
        unit = 'TB'

    precision = 1
    number_of_bytes = round(number_of_bytes, precision)

    return str(number_of_bytes) + ' ' + unit

class Command(BaseCommand):
    help = 'Initializes a DynamoDB database. Creating all the needed Tables for this application'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        client = getDyDbClient()

        if not settings.DYNAMODB_HOST:
            print("DynamoDB tables in AWS:")
        else:
            endpoint_url="http://%s:%s"% (settings.DYNAMODB_HOST, settings.DYNAMODB_PORT)
            print("DynamoDB tables in %s:" %endpoint_url)

        names = client.list_tables()['TableNames']
        tabdata = []
        for table in names:
            response = client.describe_table(TableName=table)
            tabdata.append((table, response["Table"]["ItemCount"], bytes_2_human_readable(int(response["Table"]["TableSizeBytes"]))))

        print(tabulate(tabdata))

