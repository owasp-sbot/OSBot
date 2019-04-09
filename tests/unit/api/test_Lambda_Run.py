from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev

from osbot.api.Lambda_Handler import Lambda_Handler
from osbot.test_helpers.Test_Data import Test_Data


class test_Lambda_Run(TestCase):

    def setUp(self):
        self.handler = Lambda_Handler()

    def test_run(self):
        self.handler.run(Test_Data.api_gw_payload_help)

    def test_run__no_team(self):
        Dev.print(self.handler.run(Test_Data.api_gw_payload_no_team))