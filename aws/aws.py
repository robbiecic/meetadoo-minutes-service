import boto3
import json
from aws.secrets import get_secrets


# Read JSON data into the datastore variable
data = json.loads(get_secrets())


def create_ses_client():
    return boto3.client('ses', region_name=data['aws_region_name'], aws_access_key_id=data['aws_access_key_id'],
                        aws_secret_access_key=data['aws_secret_access_key'])


def create_dynamodb_client():
    return boto3.client('dynamodb', region_name=data['aws_region_name'], aws_access_key_id=data['aws_access_key_id'],
                        aws_secret_access_key=data['aws_secret_access_key'])


def create_dynamodb_resource():
    return boto3.resource('dynamodb', region_name=data['aws_region_name'], aws_access_key_id=data['aws_access_key_id'],
                          aws_secret_access_key=data['aws_secret_access_key'])
