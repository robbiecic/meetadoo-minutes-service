
import json
import aws
import json
import bcrypt
import jwt
import base64
from datetime import datetime
from datetime import timedelta
import uuid
from boto3.dynamodb.conditions import Key, Attr


# Create dynamodb instance
dynamodb_client = aws.create_dynamodb_client()

# Set Master key for cryptography
master_secret_key = 'RobboSecretKey123'


def create_minute(body):

    try:
        # Body must contain the following mandatory fields
        creator = body['creator']
        title = body['title']
        date = body['date']
        time = body['time']
        finish = body['finish']
        dynamo_body = return_body(body)
        # Create unique identifier to add to DB
        dynamo_body['id'] = {'S': str(uuid.uuid4())}

        # Send item to Minutes table
        response = dynamodb_client.put_item(
            TableName='Minutes', Item=dynamo_body)

        return {'statusCode': 200, 'response': 'Something'}

    except Exception as e:
        print(e)
        return custom_400('Body is missing key information')


def create_minute_actions(minute_id):
    pass


def get_my_minutes(email):
    response = dynamodb_client.query(TableName='Minutes',
                                     IndexName='creator-index', KeyConditionExpression="creator = :v1",
                                     ExpressionAttributeValues={
                                         ":v1": {"S": email}
                                     })
    minutes = {}
    try:
        mintues = response['Items']
        return {'statusCode': 200, 'response': mintues}
    except:
        return custom_400('Could not find any')


def return_body(jsonObject):
    return_dict = {}
    for key in jsonObject:
        value = jsonObject[key]
        if key == 'guests':
            return_dict[key] = {'SS': value}
        elif key == 'repeat':
            return_dict[key] = {'BOOL': value}
        elif key == 'actions':
            return_dict[key] = {'L': value}
        else:
            return_dict[key] = {'S': value}

    return(return_dict)
#
# def update_user(body):
#     # Can't update key which is email address. Might need a change email address method which removes Item and creates new
#     email = str(body['email'])
#     new_firstname = str(body['firstname'])
#     new_surname = str(body['surname'])
#     try:
#         # Remove user record from dynamoDB if exists
#         if return_user(email) != 0:
#             dynamodb_client.update_item(TableName='Minutes', Key={'email_address': {'S': email}},
#                                         UpdateExpression="SET first_name = :firstnameUpdated, surname = :surnameUpdated",
#                                         ExpressionAttributeValues={':firstnameUpdated': {'S': new_firstname}, ':surnameUpdated': {'S': new_surname}})
#             return {'statusCode': 200, 'response': str('Updated User - ' + email)}
#         else:
#             return custom_400('No User found')
#     except Exception as E:
#         return custom_400(str(E))
#
#
# def remove_user(email):
#     if return_user(email) != 0:
#         dynamodb_client.delete_item(TableName='Minutes', Key={
#                                     'email_address': {'S': email}})
#         return('Removed User Successfully - ' + str(email))
#     else:
#         return custom_400('No User found')
#
#
# def get_user(email_address):
#     user = return_user(email_address)
#     return_body = {}
#     return_body["firstname"] = user['first_name']['S']
#     return_body["surname"] = user['surname']['S']
#     return_body["email"] = email_address
#     if user != 0:
#         return {'statusCode': 200, 'response': str(return_body)}
#     else:
#         return custom_400('No User found')
#
#
# def return_user(email_address):
#     response = dynamodb_client.get_item(
#         TableName='Minutes', Key={'email_address': {'S': email_address}})
#     # Check if an user existsx
#     try:
#         user = response['Item']
#         return user
#     except:
#         return 0
#
#


def custom_400(message):
    return {'statusCode': 400, 'response': message}
