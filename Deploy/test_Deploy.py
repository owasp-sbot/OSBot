
from unittest import TestCase

from osbot_aws.helpers.Lambda_Package import Lambda_Package
from pbx_gs_python_utils.utils.Dev import Dev

from osbot.Deploy import Deploy


class test_Deploy(TestCase):

    def setUp(self):
        self.deploy = Deploy()

    def test__init__(self):
        assert self.deploy.osbot._lambda.s3_key    == 'gsbot/gsbot.zip'
        assert self.deploy.osbot._lambda.s3_bucket == 'gs-lambda-tests'

    def test_deploy_osbot(self):
        #assert self.deploy.deploy().get('status') == 'ok'
        Lambda_Package('osbot.lambdas.osbot').update_code()

    def test_deploy_slack_callback(self):
        Lambda_Package('osbot.lambdas.slack_callback').update_code()
