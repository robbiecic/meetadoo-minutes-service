#
# dynamo_user.py
#
# This file will create the new table store main user details in dynamodb

from aws.aws import create_dynamodb_resource, create_dynamodb_client
from botocore.exceptions import ClientError

# Create dynamodb instance
client = aws.create_dynamodb_resource()
client2 = aws.create_dynamodb_client()

try:
    table = client.create_table(
        TableName='Minutes',
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'  # Partition key, unique
            },
            {
                'AttributeName': 'creation_date',
                'KeyType': 'RANGE'  # Partition key, unique
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'creation_date',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }

    )
except ClientError as ce:
    print("ERROR CREATING TABLE - ", ce.response)
