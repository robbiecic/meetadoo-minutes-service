
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
# dynamodb_client = aws.create_dynamodb_client()
# the lint error is wrong, this actually works!
table = dynamodb_resource.Table('Minutes')
table_actions = dynamodb_resource.Table('Actions')
table_history = dynamodb_resource.Table('History')
# Set Master key for cryptography
master_secret_key = 'RobboSecretKey123'


def create_minute(body, user_email):

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

        audit = {}
        audit['meeting_id'] = body['id']
        audit['description'] = 'Added Meeting  - ' + str(body['title'])
        audit['author'] = user_email
        add_audit_history(audit)

        return {'statusCode': response_code, 'response': 'Success'}

    except Exception as e:
        print(e)
        return custom_400('Body is missing key information')


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


def create_action(body, user_email):
    # With action
    # body must contain the meeting_id, assignee, description and due_date
    # Like this body = {meeting_id: 123, assignee: robert.cicero@hotmail.com, description: NEED TO DO SOMEHTING, due_date: 2020-02-15}
    try:
        body['id'] = str(uuid.uuid4())
        response = table_actions.put_item(Item=body)
        response_code = response['ResponseMetadata']['HTTPStatusCode']
        # If successful, add to audit table
        audit = {}
        audit['meeting_id'] = body['meeting_id']
        audit['description'] = 'Added Action - ' + str(body['description'])
        audit['author'] = user_email
        add_audit_history(audit)

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


def remove_action(action_id, meeting_id, user_email):
    # Get description
    action_details = table_actions.get_item(
        Key={'id': action_id, 'meeting_id': meeting_id})

    # If successful, add to audit table
    audit = {}
    audit['meeting_id'] = str(meeting_id)
    audit['description'] = 'Removed Action - ' + \
        str(action_details['Item']['description'])
    audit['author'] = user_email
    add_audit_history(audit)

    # Delete item only works at client level, not resource
    response = table_actions.delete_item(
        Key={'id': str(action_id), 'meeting_id': str(meeting_id)})

    response_code = response['ResponseMetadata']['HTTPStatusCode']

    return {'statusCode': response_code, 'response': 'Success'}


def mock_GetMyMinutes(email_address):
    result = json.loads(get_my_minutes(email_address))
    return_result = {}
    return_result = {
        "statusCode":  result['statusCode'],
        "body": json.dumps(result['response']),
        "isBase64Encoded": False}
    return return_result


def add_audit_history(message):
    # Message = meeting_id, author, description
    try:
        message['id'] = str(uuid.uuid4())
        message['date_stamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        response = table_history.put_item(Item=message)
        response_code = response['ResponseMetadata']['HTTPStatusCode']
        return {'statusCode': response_code, 'response': 'Success'}
    except:
        custom_400('Failed to add to history')


def get_history(meeting_id):
    history_response = table_history.scan(ProjectionExpression="id, meeting_id, date_stamp, author, description",
                                          FilterExpression="meeting_id = :vmeeting_id",
                                          ExpressionAttributeValues={
                                              ":vmeeting_id": meeting_id
                                          })
    try:
        history_response['Items']
        return_body = {"statusCode": 200, "response": {
            "actions": history_response['Items']}}
        return_body_json = json.dumps(return_body, default=set_default)
        return return_body_json
    except:
        return custom_400('No history found')


def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError
