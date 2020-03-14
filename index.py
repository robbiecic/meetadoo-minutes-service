import json
from minute_functions import create_minute, get_minute_detail, get_my_minutes, isAuthenticated, create_action, get_actions, remove_action, get_history, update_minute, supplement_minutes, complete_action, get_my_actions
from getJwt import get_jwt


def lambda_handler(event, context):
    # This API is driven off the query string parameter 'request_action'
    print('Event details- ', str(event))

    # This will always be hear as defined by API Gateway rule
    action = event['queryStringParameters']['action']

    # If POST then get body
    if event['httpMethod'] == 'POST':
        # Try setting event body, fail if doesn't exist
        try:
            # For every request, we require a data object containing at least the email
            try:
                bodydata = json.loads(event['body'])
            except:
                bodydata = event['body']
        except Exception as identifier:
            return {
                'statusCode': 400,
                'body': 'Body Not formed properly' + str(identifier)
            }
        # Set body data
        body = bodydata['data']

    # Locate cookie details if there, if not ignore
    # 'cookie' is case sensistive. Is lower case from browser, upper care from Postman
    try:
        cookie = event['headers']['cookie']
    except:
        cookie = event['headers']['Cookie']
    jwt_token = get_jwt(cookie)

    # With any minute request, you must be authenticated
    authenticated_response = isAuthenticated(jwt_token)
    if authenticated_response['statusCode'] == 200:
        print('User pass authentication with response ' +
              str(authenticated_response))
        body_email = authenticated_response['response']

        if (action == 'CreateMinute' and event['httpMethod'] == 'POST'):
            result = create_minute(body, body_email)
            return {
                'statusCode': result['statusCode'],
                'body': result['response']
            }
        elif (action == 'UpdateMinute' and event['httpMethod'] == 'POST'):
            result = update_minute(body, body_email)
            return {
                'statusCode': result['statusCode'],
                'body': result['response']
            }
        elif (action == 'SupplementMinute' and event['httpMethod'] == 'POST'):
            result = supplement_minutes(body, body_email)
            return {
                'statusCode': result['statusCode'],
                'body': result['response']
            }
        elif (action == 'GetMinuteDetail' and event['httpMethod'] == 'GET'):
            meeting_id = event['queryStringParameters']['meetingID']
            result = get_minute_detail(meeting_id)
            return {
                'statusCode': result['statusCode'],
                'body': result['response']
            }
        elif (action == 'GetMyMinutes' and event['httpMethod'] == 'GET'):
            result = json.loads(get_my_minutes(body_email))
            return_result = {}
            return_result = {
                "statusCode":  result['statusCode'],
                "body": json.dumps(result['response']),
                "isBase64Encoded": False}
            return return_result
        elif (action == 'CreateAction' and event['httpMethod'] == 'POST'):
            result = create_action(body, body_email)
            return {
                'statusCode': result['statusCode'],
                'body': result['response']
            }
        elif (action == 'GetActions' and event['httpMethod'] == 'GET'):
            meeting_id = event['queryStringParameters']['meetingID']
            result = json.loads(get_actions(meeting_id))
            return {
                "statusCode": result['statusCode'],
                "body": json.dumps(result['response'])
            }
        elif (action == 'GetMyActions' and event['httpMethod'] == 'GET'):
            result = json.loads(get_my_actions(body_email))
            return {
                "statusCode": result['statusCode'],
                "body": json.dumps(result['response'])
            }
        elif (action == 'RemoveAction' and event['httpMethod'] == 'POST'):
            action_id = event['queryStringParameters']['actionID']
            meeting_id = event['queryStringParameters']['meetingID']
            result = remove_action(action_id, meeting_id, body_email)
            return {
                'statusCode': result['statusCode'],
                'body': result['response']
            }
        elif (action == 'CompleteAction' and event['httpMethod'] == 'POST'):
            result = complete_action(body, body_email)
            return {
                'statusCode': result['statusCode'],
                'body': result['response']
            }
        elif (action == 'GetHistory' and event['httpMethod'] == 'GET'):
            meeting_id = event['queryStringParameters']['meetingID']
            result = json.loads(get_history(meeting_id))
            return {
                "statusCode": result['statusCode'],
                "body": json.dumps(result['response'])
            }
        else:
            return {
                'statusCode': 400,
                'body': "A valid request action was not provided"
            }
    else:
        return authenticated_response
