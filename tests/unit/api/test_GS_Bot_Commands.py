
from unittest import TestCase

from osbot.api.GS_Bot_Commands import GS_Bot_Commands


class test_GS_Bot_Commands(TestCase):

    def test_hello(self):
        assert GS_Bot_Commands.hello({}              ) == ('Hello <@None>, how can I help you?',[])
        assert GS_Bot_Commands.hello({'user' : 'abc'}) == ('Hello <@abc>, how can I help you?',[])

    def test_time(self):
        assert 'Hi <@abc>, the time now is:' in GS_Bot_Commands.time({'user' : 'abc'})[0]

    def test_commands_available(self):
        assert GS_Bot_Commands.help({}) == ( '*Here are the commands available*',[ {  'color': 'good',
                                                                                      'text': ' • browser\n'
                                                                                              ' • dot_render\n'
                                                                                              ' • gdocs\n'
                                                                                              ' • graph\n'
                                                                                            ' • hello\n'
                                                                                              ' • help\n'
                                                                                              ' • jira\n'
                                                                                              ' • jupyter\n'
                                                                                              ' • mindmap\n'
                                                                                              ' • plantuml\n'
                                                                                              ' • sheets\n'
                                                                                              ' • slides\n'
                                                                                              ' • time\n'
                                                                                              ' • version\n'}])


    def test_bad_cmd(self):
        (text, attachment) = GS_Bot_Commands.bad_cmd({'text' : 'bbbb'})
        assert text == (':exclamation: Sorry, could not match provided command to a method: `bbbb`\n'
                        '*Here are the commands available*')

    def test_dot_render(self):
        slack_event = { "text" : "```A->B```", "channel" : "GDL2EC3EE"}
        assert GS_Bot_Commands.dot_render(slack_event, []) == (':information_source:  Rending dot code with size: 19', [])

    def test_dot_mindmap(self):
        slack_event = {}
        assert GS_Bot_Commands.mindmap(slack_event, [ "aaa"]) == (None, None)

    def test_gdocs(self):
        assert GS_Bot_Commands.gdocs({}, ["version"]) == (None,None)

    def test_slides(self):
        assert GS_Bot_Commands.slides({}, ["version"]) == (None,None)

    # def test_public_slack_channels(self):
    #     result = GS_Bot_Commands.public_slack_channels({})
    #     Dev.pprint(result)



    def test_version(self):
        assert GS_Bot_Commands.version({}) == ('The current version of GSBot is {0}'.format(GS_Bot_Commands.gsbot_version),[])

    # def test_update_lambda(self):
    #    Lambdas('pbx_gs_python_utils.lambdas.gsbot.lambda_gs_bot').update_with_src()