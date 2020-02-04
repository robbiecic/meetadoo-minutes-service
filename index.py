import json
from user_functions import create_user, remove_user, login, get_user, isAuthenticated, update_user


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
        email = body['email']

    # Locate cookie details if there, if not ignore
    try:
        # 'cookie' is case sensistive. Is lower case from browser, upper care from Postman
        try:
            cookie = event['headers']['cookie']
        except:
            cookie = event['headers']['Cookie']
        print('Cookie - ' + str(cookie))
        jwt_token = cookie.replace("jwt=", "")
    except:
        jwt_token = "Something Invalid"

    print('jwt_token - ' + str(jwt_token))

    # Enter if statement block to route message
    if (action == 'CreateUser'):
        result = create_user(body)
        return {
            "headers": {"Set-Cookie": result['cookie'], "Access-Control-Allow-Origin": "http://localhost:8080", "Access-Control-Allow-Credentials": "true"},
            'statusCode': result['statusCode'],
            'body': result['response']
        }
    elif (action == 'RemoveUser'):
        result = remove_user(email)
        return {
            'statusCode': result['statusCode'],
            'body': result['response']
        }
    elif (action == 'Login'):
        result = login(body)
        return {
            "headers": {"Set-Cookie": result['cookie'], "Access-Control-Allow-Origin": "http://localhost:8080", "Access-Control-Allow-Credentials": "true"},
            'statusCode': result['statusCode'],
            'body': result['response']
        }
    elif (action == 'isAuthenticated'):
        result = isAuthenticated(jwt_token)
        return {
            'statusCode': result['statusCode'],
            'body': result['response']
        }
    elif (action == 'UpdateUser'):
        result = update_user(body)
        return {
            'statusCode': result['statusCode'],
            'body': result['response']
        }
    elif (action == 'getUser'):
        authenticated_response = isAuthenticated(jwt_token)
        if authenticated_response['statusCode'] == 200:
            print('User pass authentication with response ' +
                  str(authenticated_response))
            # Get email from decoded response. Don't want to store it on client side, but it's in the token which is issued upon successful login
            body_email = authenticated_response['response']
            result = get_user(body_email)
            return {
                'statusCode': result['statusCode'],
                'body': result['response']
            }
        else:
            return authenticated_response
    else:
        return {
            'statusCode': 400,
            'body': "A valid request action was not provided"
        }
