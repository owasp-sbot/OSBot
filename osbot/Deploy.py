from osbot_aws.apis.Lambda import Lambda
from osbot_aws.helpers.Lambda_Package import Lambda_Package
from pbx_gs_python_utils.utils.Dev import Dev
from pbx_gs_python_utils.utils.Files import Files


class Deploy:

    def __init__(self):
        self.osbot         = Lambda_Package('osbot.lambdas.osbot')
        self.tmp_s3_bucket = 'gs-lambda-tests'
        self.tmp_s3_key    = 'gsbot/gsbot.zip'
        self.setup()

    def setup(self):
        self.osbot._lambda.set_s3_bucket(self.tmp_s3_bucket)
        self.osbot._lambda.set_s3_key   (self.tmp_s3_key)


    def deploy(self):
        code_folder = Files.path_combine(__file__,'..')
        self.osbot.add_folder(code_folder)
        self.osbot.add_root_folder()
        self.osbot.add_pbx_gs_python_utils()
        return self.osbot.update()
