
import json
import aws
import json
import bcrypt
import jwt
import base64
from datetime import datetime
from datetime import timedelta


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

        # Send item to Minutes table
        response = dynamodb_client.put_item(TableName='Minutes', Item=body)
        print(response)
        return {'statusCode': 200, 'response': 'Something'}

    except Exception as e:
        print(e)
        return custom_400('Body is missing key information')

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
# def custom_400(message):
#     return {'statusCode': 400, 'response': message}
#
#
# def set_cookie(jwt):
#     # Delete the cookie after 1 day
#     expires = (datetime.utcnow() +
#                timedelta(seconds=60 * 60 * 24)).strftime("%a, %d %b %Y %H:%M:%S GMT")
#     # Will remove HttpOnly and see if that works
#     # Will take out secure for now, doesn't work in dev
#     cookie_string = 'jwt=' + \
#         str(jwt) + ';  expires=' + \
#         str(expires) + "; SameSite=None; Path=/"
#     return cookie_string
#
#
# def encrypt_string(string_to_encrypt):
#     salt = bcrypt.gensalt()
#     combo_password = string_to_encrypt.encode(
#         'utf-8') + master_secret_key.encode('utf-8')
#     hashed_password = bcrypt.hashpw(combo_password, salt)
#     return hashed_password
