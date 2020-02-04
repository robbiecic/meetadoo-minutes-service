
import aws
import uuid
from boto3.dynamodb.conditions import Key, Attr
import jwt
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
        creation_date = body['creation_date']
        time = body['time']
        finish = body['finish']
        dynamo_body = return_body(body)
        # Create unique identifier to add to DB
        dynamo_body['id'] = {'S': str(uuid.uuid4())}

        # Send item to Minutes table
        response = dynamodb_client.put_item(
            TableName='Minutes', Item=dynamo_body)

        return {'statusCode': 200, 'response': 'Success'}

    except Exception as e:
        print(e)
        return custom_400('Body is missing key information')


def create_minute_actions(minute_id):
    pass


def get_minute_detail(meeting_id):
    minute_detail = dynamodb_client.query(TableName='Minutes',
                                          Key={'id': {'S': meeting_id}})
    try:
        return {'statusCode': 200, 'response': minute_detail['Items']}
    except:
        return custom_400('Could not find a meeting')


def get_my_minutes(email):
    minutes_i_created = dynamodb_client.query(TableName='Minutes',
                                              IndexName='creator-index', KeyConditionExpression="creator = :email",
                                              ExpressionAttributeValues={
                                                  ":email": {"S": email}
                                              })

    minutes_i_attended = dynamodb_client.scan(TableName="Minutes",
                                              FilterExpression="contains(guests,:email) and creator <> :email",
                                              ExpressionAttributeValues={
                                                  ":email": {"S": email}
                                              })
    try:
        minutes_i_created['Items']
    except:
        minutes_i_created['Items'] = {}
    try:
        minutes_i_attended['Items']
    except:
        minutes_i_attended['Items'] = {}

    try:
        return {'statusCode': 200, 'response': {'minutes_created': minutes_i_created['Items'], 'minutes_attended': minutes_i_attended}}
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
