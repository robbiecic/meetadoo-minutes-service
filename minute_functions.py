
from aws.aws import create_dynamodb_resource
from aws.secrets import get_secrets
import boto3
import uuid
from boto3.dynamodb.conditions import Key, Attr
import jwt
import json
from datetime import datetime
from datetime import timedelta

# Create dynamodb instance
dynamodb_resource = create_dynamodb_resource()

# the lint error is wrong, this actually works!
table = dynamodb_resource.Table('Minutes')
table_actions = dynamodb_resource.Table('Actions')
table_history = dynamodb_resource.Table('History')

data = json.loads(get_secrets())


def create_minute(body, user_email):

    try:
        # Body must contain the following mandatory fields
        body['creator'] = user_email
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


def update_minute(body, user_email):
    # Will need need some validation here, as it will just create or replace the existing object
    # You cannot modify creation date! Creation date and meeting ID must match in order for it to update correctly
    try:
        # Put Item will replace the entire content of the existing object
        response = table.put_item(Item=body)
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            # If successful add to audit table
            audit = {}
            audit['meeting_id'] = body['id']
            audit['description'] = 'Updated Meeting  - ' + str(body['title'])
            audit['author'] = user_email
            add_audit_history(audit)
            return {'statusCode': 200, 'response': 'Successfully updated Minute'}
        else:
            return custom_400('No minute found')
    except Exception as E:
        return custom_400(str(E))


def get_minute_detail(meeting_id, creation_date):

    minute_detail = table.get_item(
        Key={'id': meeting_id, 'creation_date': creation_date})
    return_body = {"statusCode": 200, "response": minute_detail['Item']}
    return_body_json = json.dumps(return_body, default=set_default)

    try:
        return return_body_json
    except:
        return custom_400('Could not find a meeting')


def get_my_minutes(email):
    minutes_i_created = table.query(ProjectionExpression="id, creator, title, creation_date, time_start, time_end, time_zone, guests, repeat_event, description, minutes, labels",
                                    IndexName='creator-index', KeyConditionExpression="creator = :email",
                                    ExpressionAttributeValues={
                                        ":email": email
                                    })

    minutes_i_attended = table.scan(ProjectionExpression="id, creator, title, creation_date, time_start, time_end, time_zone, guests, repeat_event, description, minutes, labels",
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
        payload = jwt.decode(
            encoded_jwt, data['jwt_encode'], algorithms=['HS256'])
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
    actions_response = table_actions.scan(ProjectionExpression="description, assignee, due_date, id, meeting_id, checked",
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


def get_my_actions(email_address):
    actions_response = table_actions.scan(ProjectionExpression="description, assignee, due_date, id, meeting_id, checked",
                                          FilterExpression="contains(assignee, :vassignee)",
                                          ExpressionAttributeValues={
                                              ":vassignee": email_address
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
        history = history_response['Items']
        history_sorted = sorted(
            history, key=lambda history_sorted: history_sorted['date_stamp'], reverse=True)

        return_body = {"statusCode": 200, "response": {
            "actions": history_sorted}}
        return_body_json = json.dumps(return_body, default=set_default)
        return return_body_json
    except:
        return custom_400('No history found')


def supplement_minutes(body, user_email):
    # Expected body format
    # {
    #   "meeting": {
    #     "id": "",
    #     "creation_date": ""
    #   },
    #   "minutes": {
    #   }
    # }

    minute_to_update = body['meeting']
    supplemented_data = body['minutes']
    try:
        response = table.update_item(
            Key={
                'id': minute_to_update['id'],
                'creation_date': minute_to_update['creation_date']
            },
            UpdateExpression="SET minutes= :var1",
            ExpressionAttributeValues={':var1': supplemented_data}

        )
        # If successful, add to audit table
        audit = {}
        audit['meeting_id'] = str(minute_to_update['id'])
        audit['description'] = 'Updated Minute detail'
        audit['author'] = user_email
        add_audit_history(audit)

        return {'statusCode': 200, 'response': 'Success'}

    except:
        custom_400('Failed to add to history')


def complete_action(body, user_email):
    # Expected body format
    # {
    #   "meeting_id": Value,
    #   "action_id": Value,
    #   "completed": Value
    # }

    meeting_id = body['meeting_id']
    action_id = body['action_id']
    checked = body['checked']

    try:
        response = table_actions.update_item(
            Key={
                'id': action_id,
                'meeting_id': meeting_id
            },
            UpdateExpression="SET checked= :var1",
            ExpressionAttributeValues={':var1': checked}

        )
        # If successful, add to audit table
        audit = {}
        audit['meeting_id'] = str(meeting_id)
        audit['description'] = 'Changed status of ' + \
            str(action_id) + ' to ' + str(checked)
        audit['author'] = user_email

        add_audit_history(audit)

        return {'statusCode': 200, 'response': 'Success'}

    except:
        custom_400('Failed to update action')


def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError
