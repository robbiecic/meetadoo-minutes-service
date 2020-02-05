import unittest
import json
from minute_functions import create_minute, get_my_minutes
from index import lambda_handler

# Import test data
with open('tests/create_minute.json') as json_file:
    json_data = json.load(json_file)


class MinuteTestCase(unittest.TestCase):

    # Remove Test User
    @classmethod
    def tearDownClass(cls):
        # remove_user('test@NoteIt.com')
        pass

    # Create minute
    def test_create_minute(self):
        response = create_minute(json_data['data'])
        self.assertEqual(response['statusCode'], 200)

    # Get Minute
    def test_get_my_minutes(self):
        email = json_data['data']['creator']
        response = json.loads(get_my_minutes(email))
        self.assertEqual(response['statusCode'], 200)
        response = json.loads(get_my_minutes('test6@test.com'))
        self.assertEqual(response['statusCode'], 200)

    # GetMeetings from lambda (Can't run in live due to jwt)
    # def test_GetMyMinutes(self):
    #     event = {}
    #     context = {}
    #     event['queryStringParameters'] = {'action': 'GetMyMinutes'}
    #     event['httpMethod'] = 'GET'
    #     email = json_data['data']['creator']
    #     response = lambda_handler(event, context)
    #     self.assertEqual(response['statusCode'], 200)
    #     response = json.loads(get_my_minutes('test6@test.com'))
    #     self.assertEqual(response['statusCode'], 200)

# End of UserTestCase --------------------------------------------------------------------------------------------------------------------


def suite():  # Need to define a suite as setUp and tearDown are called per test otherwise
    suite = unittest.TestSuite()
    suite.addTest(MinuteTestCase('test_create_minute'))
    suite.addTest(MinuteTestCase('test_get_my_minutes'))
    # suite.addTest(MinuteTestCase('test_GetMyMinutes'))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
