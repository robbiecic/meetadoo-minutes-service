import unittest
import json
import requests

# Import test data
with open('tests/test-data/create_user.json') as json_file:
    json_data = json.load(json_file)

# Set URL where API calls are made
url = "https://i6vtmh1eq3.execute-api.ap-southeast-2.amazonaws.com/Development"


class E2ETestCase(unittest.TestCase):

    # Remove user first if exists
    def setUp(self):
        try:
            requests.post(url=url + "?action=RemoveUser", data=json.dumps(json_data), headers={
                'content-type': 'application/json'})
        except:
            print('Had to remove user before running test')

    # Remove Test User
    @classmethod
    def tearDownClass(cls):
        requests.post(url=url + "?action=RemoveUser", data=json.dumps(json_data), headers={
            'content-type': 'application/json'})

    # Create test user
    def test_valid_user_registration(self):
        # sending get request and saving the response as response object
        response = requests.post(url=url + "?action=CreateUser", data=json.dumps(json_data), headers={
                                 'content-type': 'application/json'})
        self.assertEqual(response.status_code, 200)

    # Invalid query string parameter
    def test_bad_query_string(self):
        # sending get request and saving the response as response object
        response = requests.post(url=url + "?action=BadString", data=json.dumps(json_data), headers={
                                 'content-type': 'application/json'})
        self.assertEqual(response.status_code, 400)

# End of E2ETestCase --------------------------------------------------------------------------------------------------------------------


def suite():  # Need to define a suite as setUp and tearDown are called per test otherwise
    suite = unittest.TestSuite()
    suite.addTest(E2ETestCase('test_valid_user_registration'))
    suite.addTest(E2ETestCase('test_bad_query_string'))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
