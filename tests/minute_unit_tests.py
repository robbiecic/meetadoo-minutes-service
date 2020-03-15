import unittest
import json
from minute_functions import create_minute, get_my_minutes, mock_GetMyMinutes, create_action, get_actions, remove_action, get_history, update_minute, supplement_minutes, get_my_actions, complete_action, get_minute_detail

# Import test data
with open('tests/create_minute.json') as json_file:
    json_data = json.load(json_file)
with open('tests/create_action.json') as json_file:
    action_json_data = json.load(json_file)
with open('tests/update_minute.json') as json_file:
    update_json_data = json.load(json_file)
with open('tests/supplement_minute.json') as json_file:
    supplement_json_data = json.load(json_file)
with open('tests/complete_action.json') as json_file:
    checked_json_data = json.load(json_file)


class MinuteTestCase(unittest.TestCase):

    # Remove Test User
    @classmethod
    def tearDownClass(cls):
        # remove_user('test@NoteIt.com')
        pass

    # Create minute
    def test_create_minute(self):
        response = create_minute(
            json_data['data'], json_data['data']['creator'])
        self.assertEqual(response['statusCode'], 200)

    # Get Minute
    def test_get_my_minutes(self):
        email = json_data['data']['creator']
        response = json.loads(get_my_minutes(email))
        self.assertEqual(response['statusCode'], 200)
        response = json.loads(get_my_minutes('test6@test.com'))
        self.assertEqual(response['statusCode'], 200)

    # GetMeetings from lambda (Can't run in live due to jwt)
    def test_mock_GetMyMinutes(self):
        email = json_data['data']['creator']
        response = mock_GetMyMinutes(email)
        self.assertEqual(response['statusCode'], 200)

    # create_action
    def test_create_action(self):
        body = action_json_data['data']
        response = create_action(body, json_data['data']['creator'])
        self.assertEqual(response['statusCode'], 200)

    # get_actions
    def test_get_actions(self):
        meeting_id = action_json_data['data']['meeting_id']
        response = json.loads(get_actions(meeting_id))
        self.assertEqual(response['statusCode'], 200)

    # def test_delete_action(self):
    #     response = remove_action(
    #         '0339d6d6-09b1-4b89-878e-42cadc6a96c5', '1234567')
    #     self.assertEqual(response['statusCode'], 200)

    def test_get_history(self):
        meeting_id = action_json_data['data']['meeting_id']
        response = json.loads(get_history(meeting_id))
        self.assertEqual(response['statusCode'], 200)

    def test_update_minute(self):
        response = update_minute(update_json_data['data'], 'test5@test.com')
        self.assertEqual(response['statusCode'], 200)

    def test_supplementing_minutes(self):
        # Try and supplement
        response = supplement_minutes(supplement_json_data, 'test5@test.com')
        self.assertEqual(response['statusCode'], 200)

    def test_get_my_actions(self):
        response = json.loads(get_my_actions('test5@test.com'))
        self.assertEqual(response['statusCode'], 200)

    def test_complete_action(self):
        response = complete_action(checked_json_data, 'test5@test.com')
        self.assertEqual(response['statusCode'], 200)

    def test_get_minute_detail(self):
        response = json.loads(get_minute_detail(
            '1bd4cdea-bd6c-4eca-96d0-d0a2450cd7bc', '2019-02-04'))
        self.assertEqual(response['statusCode'], 200)


# End of UserTestCase --------------------------------------------------------------------------------------------------------------------


def suite():  # Need to define a suite as setUp and tearDown are called per test otherwise
    suite = unittest.TestSuite()
    suite.addTest(MinuteTestCase('test_create_minute'))
    suite.addTest(MinuteTestCase('test_get_my_minutes'))
    suite.addTest(MinuteTestCase('test_mock_GetMyMinutes'))
    suite.addTest(MinuteTestCase('test_create_action'))
    suite.addTest(MinuteTestCase('test_get_actions'))
    # suite.addTest(MinuteTestCase('test_delete_action'))
    suite.addTest(MinuteTestCase('test_get_history'))
    suite.addTest(MinuteTestCase('test_update_minute'))
    suite.addTest(MinuteTestCase('test_supplementing_minutes'))
    suite.addTest(MinuteTestCase('test_get_my_actions'))
    suite.addTest(MinuteTestCase('test_complete_action'))
    suite.addTest(MinuteTestCase('test_get_minute_detail'))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
