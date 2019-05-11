import base64
import unittest

from osbot_aws.apis.Lambda import Lambda
from pbx_gs_python_utils.utils.Dev  import Dev
from osbot.api.API_GS_Bot           import API_GS_Bot

class Test_API_GS_Bot(unittest.TestCase):
    def setUp(self):
        self.api = API_GS_Bot()

    def test___init__(self):
        assert self.api.__class__.__name__ == 'API_GS_Bot'
        assert 'xoxb-25' in self.api.bot_token

    def test_handle_command(self):
        result = self.api.handle_command({'text': '<@UDK5W7W3T> hello'})
        Dev.pprint(result)

    def test_handle_command__graph(self):

        result = self.api.handle_command({'text': '<@UDK5W7W3T> graph', 'channel': 'GBMGMK88Z', 'team_id':'T7F3AUXGV'})
        Dev.pprint(result)


    def test_process_event(self):
        slack_event = { "text" : '@gsbot (in test)' , 'channel': 'GBMGMK88Z' ,'type': 'message'}
        response    = self.api.process_event(slack_event)
        assert response.get('text') == ':exclamation: GS bot command `@gsbot` not found. Use `gsbot help` ' \
                                       'to see a list of available commands'
        #assert response['ok'] == True

    def test_resolve_command_method(self):
        assert self.api.resolve_command_method('hello').__class__.__name__   == 'function'
        assert self.api.resolve_command_method('help' ).__class__.__name__   == 'function'
        assert self.api.resolve_command_method('aaaa')  is None
        assert self.api.resolve_command_method('jupyter').__class__.__name__ == 'function'
        assert self.api.resolve_command_method('jupyter').__name__           == 'jupyter'
        assert self.api.resolve_command_method('jp'     ).__name__           == 'jupyter'
        assert self.api.resolve_command_method('g'      ).__name__           == 'graph'

    def test_resolve_command_shortcuts(self):
        assert self.api.resolve_command_shortcuts('aaa') == 'aaa'
        assert self.api.resolve_command_shortcuts('jp' ) == 'jupyter'
        assert self.api.resolve_command_shortcuts('g'  ) == 'graph'

    def test_send_message(self):
        channel_id = 'GBMGMK88Z'
        team_id    = 'T7F3AUXGV'
        message    = ':point_right: an message from test_send_message'
        result     = self.api.send_message(channel_id, team_id,message)
        del result['ts']
        del result['message']['ts']
        assert result == {
                            "ok"        : True          ,
                            "channel"   : channel_id    ,
                            "message"   : {
                                "text"    : message     ,
                                "username": "gs-bot"    ,
                                "bot_id"  : "BDKLUMX4K" ,
                                "type"    : "message"   ,
                                "subtype" : "bot_message"
                            }
                        }

    def create_test_dot_png(self, dot, path_to_pic):
        dot_to_png  = Lambda('utils.dot_to_png')
        png_data    = dot_to_png.invoke({"dot": dot})
        with open(path_to_pic, "wb") as fh:
            fh.write(base64.decodebytes(png_data.encode()))

    def test_upload_image(self):
        channel  = 'GBMGMK88Z'
        text     = 'test uploading an image'
        file     =  '/tmp/slack-upload-test.png'
        dot      = """digraph G {
                                    this [shape=box]
                                    cool [shape=diamond]
                                    nice [shape=cylinder]
                                    
                                    this   -> is
                                    is     -> really
                                    really -> cool
                                    really -> nice;
                                }"""

        self.create_test_dot_png(dot, file)


        result = self.api.upload_png_file(channel, text, file)
        Dev.pprint(result)


    @unittest.skip("[todo - find root cause] throws error: Unable to import module 'lambdas.gs.slack_interaction")
    def test_process_posted_body(self):
        #process_posted_body is an old method that uses an older lambda function
        body   = "payload=%7B%22type%22%3A%22interactive_message%22%2C%22actions%22%3A%5B%7B%22name%22%3A%22game%22%2C%22type%22%3A%22button%22%2C%22value%22%3A%22chess%22%7D%5D%2C%22callback_id%22%3A%22wopr_game%22%2C%22team%22%3A%7B%22id%22%3A%22T7F3AUXGV%22%2C%22domain%22%3A%22gs-cst%22%7D%2C%22channel%22%3A%7B%22id%22%3A%22GDL2EC3EE%22%2C%22name%22%3A%22privategroup%22%7D%2C%22user%22%3A%7B%22id%22%3A%22U7ESE1XS7%22%2C%22name%22%3A%22dinis.cruz%22%7D%2C%22action_ts%22%3A%221541065372.601061%22%2C%22message_ts%22%3A%221541065370.003300%22%2C%22attachment_id%22%3A%221%22%2C%22token%22%3A%22a2J5DIEEJZtKOSZHZBqgDnVz%22%2C%22is_app_unfurl%22%3Afalse%2C%22original_message%22%3A%7B%22text%22%3A%22Would+you+like+to+play+a+game%3F%22%2C%22username%22%3A%22gs-bot%22%2C%22bot_id%22%3A%22BDKLUMX4K%22%2C%22attachments%22%3A%5B%7B%22callback_id%22%3A%22wopr_game%22%2C%22fallback%22%3A%22You+are+unable+to+choose+a+game%22%2C%22text%22%3A%22Choose+a+game+to+play%22%2C%22id%22%3A1%2C%22color%22%3A%223AA3E3%22%2C%22actions%22%3A%5B%7B%22id%22%3A%221%22%2C%22name%22%3A%22game%22%2C%22text%22%3A%22Chess%22%2C%22type%22%3A%22button%22%2C%22value%22%3A%22chess%22%2C%22style%22%3A%22%22%7D%2C%7B%22id%22%3A%222%22%2C%22name%22%3A%22game%22%2C%22text%22%3A%22Falken%27s+Maze%22%2C%22type%22%3A%22button%22%2C%22value%22%3A%22maze%22%2C%22style%22%3A%22%22%7D%2C%7B%22id%22%3A%223%22%2C%22name%22%3A%22game%22%2C%22text%22%3A%22Thermonuclear+War%22%2C%22type%22%3A%22button%22%2C%22value%22%3A%22war%22%2C%22style%22%3A%22danger%22%2C%22confirm%22%3A%7B%22text%22%3A%22Wouldn%27t+you+prefer+a+good+game+of+chess%3F%22%2C%22title%22%3A%22Are+you+sure%3F%22%2C%22ok_text%22%3A%22Yes%22%2C%22dismiss_text%22%3A%22No%22%7D%7D%5D%7D%5D%2C%22type%22%3A%22message%22%2C%22subtype%22%3A%22bot_message%22%2C%22ts%22%3A%221541065370.003300%22%7D%2C%22response_url%22%3A%22https%3A%5C%2F%5C%2Fhooks.slack.com%5C%2Factions%5C%2FT7F3AUXGV%5C%2F470483082583%5C%2FKXtEUP57fU3b70xdgX2gEDJl%22%2C%22trigger_id%22%3A%22469260156548.253112983573.23109aa28271c3a79b6a8a308dc78846%22%7D"
        result = self.api.process_posted_body(body)
        Dev.pprint(result)
        #import json
        #Dev.pprint(json.loads(result))