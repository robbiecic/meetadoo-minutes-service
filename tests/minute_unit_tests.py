import unittest
import json
from minute_functions import *
from index import lambda_handler


# Import test data
with open('tests/create_minute.json') as json_file:
    json_data = json.load(json_file)


class UserTestCase(unittest.TestCase):

    # Remove Test User
    @classmethod
    def tearDownClass(cls):
        remove_user('test@NoteIt.com')

    # Create test user
    def test_create_user(self):
        response = create_user(user_object)
        self.assertEqual(response['statusCode'], 200)

    # # Get Test User
    def test_return_user(self):
        response = return_user(user_object['email'])
        email_start = str(response).find('email_address', 0)
        # If email address key is found in the return string, then it successfully finds the email
        self.assertGreater(email_start, 0)

    # Update Test User
    def test_update_user(self):
        response = update_user(user_object2)
        # Need to handle redirect in above call
        self.assertEqual(response['statusCode'], 200)

    # Test Login
    def test_login(self):
        response = login(user_object)
        self.assertEqual(response['statusCode'], 200)

    # Test Failed Login
    def test_failed_login(self):
        response = login(user_object_bad)
        # Need to handle redirect in above call
        self.assertEqual(response['statusCode'], 400)

    # Test login from lambda function
    def test_lambda_login(self):
        context = ""
        event = {}
        event["body"] = {"data": user_object}
        event["queryStringParameters"] = {}
        event["queryStringParameters"]["action"] = 'Login'
        event["headers"] = {
            'Cookie': 'jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6InRlc3Q1QHRlc3QuY29tIiwiZXhwIjoxNTgwNTgxODc2fQ.iuyFn7JZ4Ux8CQ0_EB9xotA2uyERM0csiZYZ-zOqUOQ'}
        event['httpMethod'] = 'POST'
        response = lambda_handler(event, context)
        self.assertEqual(response['statusCode'], 200)

    # Test get User from Lambda function
    def test_lambda_getUser(self):
        # Will test get user now, but cookie isn't valid so should receive a 400
        context = ""
        event = {}
        event["body"] = {"data": user_object}
        event["queryStringParameters"] = {}
        event['httpMethod'] = 'GET'
        event["queryStringParameters"]["action"] = 'getUser'
        event["headers"] = {
            'Cookie': 'jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6InRlc3Q1QHRlc3QuY29tIiwiZXhwIjoxNTgwNTgxODc2fQ.iuyFn7JZ4Ux8CQ0_EB9xotA2uyERM0csiZYZ-zOqUOQ'}
        response = lambda_handler(event, context)
        self.assertEqual(response['statusCode'], 400)

    def test_get_user(self):
        response = get_user(user_object['email'])
        self.assertEqual(response['statusCode'], 200)
        response_data = json.loads(response['response'].replace("'", '"'))
        self.assertEqual(response_data['email'], user_object['email'])

# End of UserTestCase --------------------------------------------------------------------------------------------------------------------


def suite():  # Need to define a suite as setUp and tearDown are called per test otherwise
    suite = unittest.TestSuite()
    suite.addTest(UserTestCase('test_create_user'))
    suite.addTest(UserTestCase('test_return_user'))
    suite.addTest(UserTestCase('test_update_user'))
    suite.addTest(UserTestCase('test_login'))
    suite.addTest(UserTestCase('test_failed_login'))
    suite.addTest(UserTestCase('test_lambda_login'))
    suite.addTest(UserTestCase('test_lambda_getUser'))
    suite.addTest(UserTestCase('test_get_user'))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
