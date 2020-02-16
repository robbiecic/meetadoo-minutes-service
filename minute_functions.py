
import aws
import boto3
import uuid
from boto3.dynamodb.conditions import Key, Attr
import jwt
import json
from datetime import datetime
from datetime import timedelta

# Create dynamodb instance
dynamodb_resource = aws.create_dynamodb_resource()
dynamodb_client = aws.create_dynamodb_client()
# the lint error is wrong, this actually works!
table = dynamodb_resource.Table('Minutes')
table_actions = dynamodb_resource.Table('Actions')
# Set Master key for cryptography
master_secret_key = 'RobboSecretKey123'


def create_minute(body):

    try:
        # Body must contain the following mandatory fields
        creator = body['creator']
        title = body['title']
        creation_date = body['creation_date']
        time = body['time_start']
        finish = body['time_end']
        body['id'] = str(uuid.uuid4())
        response = table.put_item(Item=body)

        response_code = response['ResponseMetadata']['HTTPStatusCode']

        return {'statusCode': response_code, 'response': 'Success'}

    except Exception as e:
        print(e)
        return custom_400('Body is missing key information')


def create_minute_actions(minute_id):
    pass


def get_minute_detail(meeting_id):
    minute_detail = table.query(Key={'id': meeting_id})

    try:
        return {'statusCode': 200, 'response': minute_detail['Items']}
    except:
        return custom_400('Could not find a meeting')


def get_my_minutes(email):
    minutes_i_created = table.query(ProjectionExpression="id, creator, title, creation_date, time_start, time_end, time_zone, guests, repeat_event, description",
                                    IndexName='creator-index', KeyConditionExpression="creator = :email",
                                    ExpressionAttributeValues={
                                        ":email": email
                                    })

    minutes_i_attended = table.scan(ProjectionExpression="id, creator, title, creation_date, time_start, time_end, time_zone, guests, repeat_event, description",
                                    FilterExpression="contains(guests,:email) and creator <> :email",
                                    ExpressionAttributeValues={
                                        ":email": email
                                    })

    try:
        minutes_i_created['Items']
    except:
        minutes_i_created['Items'] = {}
    try:
        minutes_i_attended['Items']
    except:
        minutes_i_attended['Items'] = {}

    return_body = {"statusCode": 200, "response": {
        "minutes_created": minutes_i_created['Items'], "minutes_attended":  minutes_i_attended['Items']}}

    return_body_json = json.dumps(return_body, default=set_default)

    try:
        return return_body_json
    except:
        return custom_400('Could not find any')


def custom_400(message):
    return {'statusCode': 400, 'response': message}


def isAuthenticated(encoded_jwt):
    # jwt decode will throw an exception if fails verification
    try:
        payload = jwt.decode(encoded_jwt, 'NoteItUser', algorithms=['HS256'])
    except Exception as identifier:
        return custom_400('JWT INVALID')
    # if valid ensure not expired token
    expiration = datetime.fromtimestamp(payload['exp'])
    current_time = datetime.utcnow()
    if current_time <= expiration:
        return {'statusCode': 200, 'response': str(payload['email'])}
    else:
        return custom_400('Token expired or not valid')


def create_action(body):
    # With action
    # body must contain the meeting_id, assignee, description and due_date
    # Like this body = {meeting_id: 123, assignee: robert.cicero@hotmail.com, description: NEED TO DO SOMEHTING, due_date: 2020-02-15}
    try:
        body['id'] = str(uuid.uuid4())
        response = table_actions.put_item(Item=body)
        response_code = response['ResponseMetadata']['HTTPStatusCode']
        return {'statusCode': response_code, 'response': 'Success'}
    except:
        custom_400('Failed to add action')


def get_actions(meeting_id):
    actions_response = table_actions.scan(ProjectionExpression="description, assignee, due_date, id, meeting_id",
                                          FilterExpression="meeting_id = :vmeeting_id",
                                          ExpressionAttributeValues={
                                              ":vmeeting_id": meeting_id
                                          })
    try:
        actions_response['Items']
        return_body = {"statusCode": 200, "response": {
            "actions": actions_response['Items']}}
        return_body_json = json.dumps(return_body, default=set_default)
        return return_body_json
    except:
        return custom_400('No actions found')


def remove_action(action_id):

    # Delete item only works at client level, not resource
    response = dynamodb_client.delete_item(
        TableName='Actions', Key={'id': str(action_id)})

    # response = table_actions.delete_item(Key={'id': action_id})

    response_code = response['ResponseMetadata']['HTTPStatusCode']

    if (response_code == '200'):
        return {'statusCode': 200, 'response': 'Removed Item'}
    else:
        custom_400('Error removing Item')


def mock_GetMyMinutes(email_address):
    result = json.loads(get_my_minutes(email_address))
    return_result = {}
    return_result = {
        "statusCode":  result['statusCode'],
        "body": json.dumps(result['response']),
        "isBase64Encoded": False}
    return return_result


def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError
