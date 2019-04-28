from unittest import TestCase

from osbot_aws.apis.Lambda import Lambda
from pbx_gs_python_utils.utils.Dev import Dev
from osbot.test_helpers.Test_Data import Test_Data


class test_Check_Main_Commands(TestCase):
    def setUp(self):
        self.osbot = Lambda('osbot.lambdas.osbot')
        self.api_gw_payload = {'token': 'abc',
                           'team_id': 'T7F3AUXGV', 'api_app_id': 'ADKLUAF3M',
                           'event': {'client_msg_id': '9a85fa78-24be-4701-8ff0-5b50dd12738f',
                                     'type': 'message',
                                     'text': 'help',
                                     'user': 'U7ESE1XS7',
                                     'ts': '1554811005.000200',
                                     'channel': 'DDKUZTK6X',
                                     'event_ts': '1554811005.000200',
                                     'channel_type': 'im'},
                           'type': 'event_callback', 'event_id': 'EvHT1YNVU5',
                           'event_time': 1554811005,
                           'authed_users': ['UDK5W7W3T']}

    def test_invoke(self):
        assert self.osbot.invoke() == '500 Error'   # todo: find out the why the error


    def test_send_API_GW_command(self):
        Dev.pprint(self.osbot.invoke(Test_Data.api_gw_payload_help))
