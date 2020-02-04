import unittest
import json
from minute_functions import create_minute, get_my_minutes

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
    def test_create_minute(self):
        email = json_data['data']['creator']
        response = get_my_minutes(email)
        print(response)
        self.assertEqual(response['statusCode'], 200)


# End of UserTestCase --------------------------------------------------------------------------------------------------------------------


def suite():  # Need to define a suite as setUp and tearDown are called per test otherwise
    suite = unittest.TestSuite()
    suite.addTest(MinuteTestCase('test_create_minute'))
    suite.addTest(MinuteTestCase('get_my_minutes'))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
