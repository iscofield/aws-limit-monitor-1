#!bin/bash/python
"""
Master lambda function
"""

from json import dumps
from boto3 import client
from os import environ

def lambda_handler(event, context):
    """
    Initial lambda handler which runs through each account ID
    """
    lambda_client = client('lambda', region_name=environ['Region'])
    # convert pipe delimited AccountList string to list
    accountList = environ['AccountList'].split('|')
    for account_id in accountList:
        # removing whitespace from account ID that may exist from copying
        # otherwise the assume role will fail
        account_id = account_id.strip()
        print "Running as "+str(account_id)+"\n"
        payload={}
        payload['AccountId'] = account_id
        payloadbytes = dumps(payload)
        # kick off lambda for each subaccount that will begin the TA refresh check
        response = lambda_client.invoke(
            FunctionName=environ['InitiateCheckLambda'],
            InvocationType='Event',
            Payload=payloadbytes
        )
        print response
    return
