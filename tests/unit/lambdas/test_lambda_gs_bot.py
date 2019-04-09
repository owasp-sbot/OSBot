import unittest

from osbot_aws.apis.Lambda import Lambda
from pbx_gs_python_utils.utils.Dev import Dev

from osbot.lambdas.osbot import run


class test_lambda_gs_bot(unittest.TestCase):

    def setUp(self):
        self.step_lambda   = Lambda('gsbot')

    #def test_lambda_update(self):
    #    self.step_lambda.update_with_lib()

    def test_invoke_directly(self):
        response = run({},{})
        assert response == '200 OK'

    def _send_command_message(self,command):
        payload = {'team_id': 'T7F3AUXGV',
                   'event': {'type': 'message',
                             'text': command,
                             'channel': 'GDL2EC3EE',
                             'user': 'U7ESE1XS7'}}
        return self.step_lambda.invoke(payload)          # see answer in slack (add method to hook send_message method)

    def test_hello(self):
        response = self._send_command_message('hello')
        assert response == '200 OK'

    def test_version(self):
        response = self._send_command_message('version')
        assert response == '200 OK'
        #Dev.pprint(response)

    # def test_graph(self):
    #     response = self._send_command_message('graph')
    #     Dev.pprint(response)
    #
    # def test_graph(self):
    #     response = self._send_command_message('slack test')
    #     Dev.pprint(response)


    # def test_test_posted_data(self):
    #     body = "payload=..."
    #
    #     payload = {"body" : body}
    #
    #     response = self.step_lambda.upload_and_invoke(payload)  # == '200 OK'
    #     Dev.pprint(response)
    #
    #
    # def test_jira_test_buttons(self):
    #     payload = {'event': {'text': 'jira test', 'channel': 'GDL2EC3EE', "user": 'U7ESE1XS7', 'type':'message'}}
    #     response = self.step_lambda.upload_and_invoke(payload)  # == '200 OK'
    #
    #     Dev.pprint(response)
    #
    #
    # def test_time(self):
    #     payload = { 'event': { 'type':'message', 'text': '<@UDK5W7W3T> time' , 'channel':'GDL2EC3EE', 'user': 'U7ESE1XS7'} }
    #     assert self.step_lambda.upload_and_invoke(payload)  == '200 OK'