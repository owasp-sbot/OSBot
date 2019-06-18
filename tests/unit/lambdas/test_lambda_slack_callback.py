from unittest import TestCase

from osbot_aws.apis.Lambda import Lambda
from osbot_aws.helpers.Lambda_Package import Lambda_Package
from pbx_gs_python_utils.utils.Dev import Dev

from osbot.lambdas.slack_callback import run


class test_lambda_gs_bot(TestCase):

    def setUp(self):
        self.lambda_name = 'osbot.lambdas.slack_callback'
        self.aws_lambda = Lambda(self.lambda_name)
        self.response = None

    def tearDown(self):
        if self.response is not None:
            Dev.pprint(self.response)

    def test_lambda_update(self):
        Lambda_Package(self.lambda_name).update_code()

    def test_invoke_directly(self):
        self.response = run({},{})

    def test_invoke_lambda(self):
        self.test_lambda_update()
        self.response = self.aws_lambda.invoke()
        #assert response == '500 Error'


    def test__create_button_to_test_dialog(self):
        self.test_lambda_update()
        from pbx_gs_python_utils.utils.Lambdas_Helpers import slack_message
        from pbx_gs_python_utils.utils.slack.API_Slack_Attachment import API_Slack_Attachment
        self.api_attach = API_Slack_Attachment()
        self.api_attach.set_text       ('Click on button below to test dialog'          )   \
                       .set_callback_id("button-dialog-test"                            )   \
                       .add_button     ("button 1", "click-me-1", "open 1", "primary"   )   \
                       .add_button     ("button 2", "click-me-2", "open 2", "primary"   )
        attachments = self.api_attach.render()

        slack_message("one message", attachments, 'DDKUZTK6X')