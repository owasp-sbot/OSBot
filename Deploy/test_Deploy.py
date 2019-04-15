
from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev

from osbot.Deploy import Deploy


class test_Deploy(TestCase):

    def setUp(self):
        self.deploy = Deploy()

    def test__init__(self):
        assert self.deploy.osbot._lambda.s3_key    == 'gsbot/gsbot.zip'
        assert self.deploy.osbot._lambda.s3_bucket == 'gs-lambda-tests'

    def test_deploy(self):
        assert self.deploy.deploy().get('status') == 'ok'
        #Dev.pprint(self.deploy.osbot.invoke())

        #assert self.deploy.osbot.invoke() == '200 OK'

        #self.deploy.osbot.use_lambda_file('lambdas/dev/hello_world.py')
        #files = self.deploy.osbot.get_files()
        # assert self.deploy.osbot.update().get('status') == 'ok'
        # Dev.pprint(self.deploy.osbot.invoke())


