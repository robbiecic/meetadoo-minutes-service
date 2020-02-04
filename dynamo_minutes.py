#
# dynamo_user.py
#
# This file will create the new table store main user details in dynamodb

import aws
from botocore.exceptions import ClientError

# Create dynamodb instance
client = aws.create_dynamodb_resource()


try:
    table = client.create_table(
        TableName='Minutes',
        KeySchema=[
            {
                'AttributeName': 'creator',
                'KeyType': 'HASH'  # Partition key, unique
            },
            {
                'AttributeName': 'guests',
                'KeyType': 'HASH'  # Partition key, unique
            },
            {
                'AttributeName': 'date',
                'KeyType': 'Range'  # Partition key, unique
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'creator',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'guests',
                'AttributeType': 'L'
            },
            {
                'AttributeName': 'date',
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
