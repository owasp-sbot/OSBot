import  json
from osbot_aws.apis.Lambda import Lambda
from osbot_aws.apis.Secrets import Secrets
from    pbx_gs_python_utils.utils.Dev             import Dev
import  ssl
import  urllib

from pbx_gs_python_utils.utils.Misc import Misc


def log_debug(message, data = None, category = "API_GS_Bot"):
    payload = {
                "index"    : "gs_bot_logs",
                "level"    : "debug"     ,
                "message"  : message     ,
                "category" : category,
                "data"     : data
              }
    Lambda('pbx_gs_python_utils.lambdas.utils.log_to_elk').invoke_async(payload)

def log_error(message, data = None, category = "API_GS_Bot"):
    payload = {
                "index"    : "gs_bot_logs",
                "level"    : "error"     ,
                "message"  : message     ,
                "category" : category,
                "data"     : data
              }

    Lambda('pbx_gs_python_utils.lambdas.utils.log_to_elk').invoke_async(payload)


class API_GS_Bot:
    def __init__(self, team_id = 'T7F3AUXGV'):
        self.bot_token        = self.resolve_bot_token(team_id)
        self.slack_url        = "https://slack.com/api/chat.postMessage"
        self.bot_name         = '@gsbot'
        self.bot_id           = '<@UDK5W7W3T>'
        self.method_shortcuts = { 'jp':'jupyter' , 'g':'graph' }

    def resolve_bot_token(self,team_id):
        if team_id == 'T7F3AUXGV':    return Secrets('slack-gs-bot'       ).value()
        if team_id == 'T0SDK1RA8':    return Secrets('slack-gsbot-for-pbx').value()

    def handle_command(self, slack_event):
        try:
            if slack_event.get('text'):
                command = slack_event.get('text').replace('<@UDK5W7W3T>', '') \
                                                 .replace('<@UG2BHLSSU>', '') \
                                                 .strip()                     # remove the @gsbot names (PBX and GS-CST) from the message (this needs a better solution)
                if not command:
                    return None, None
                log_debug('command: {0}  |  team_id: {1} | channel: {2} | user: {3} '.format(command,
                                                                                             slack_event.get('team_id'),
                                                                                             slack_event.get('channel'),
                                                                                             slack_event.get('user')), category='API_GS_Bot.handle_command')
                #refactor code below to separate method
                method_name = command.split(' ')[0].split('\n')[0]
                if method_name in ['slack','gs_jira']:        # this is the new way to route commands,where a lambda function is invoked
                    lambda_name = 'pbx_gs_python_utils.lambdas.gsbot.gsbot_{0}'.format(method_name)
                    method_params = command.split(' ')[1:]
                    Lambda(lambda_name).invoke_async({'params': method_params, 'data': slack_event})
                    return None, None
                else:
                    method             = self.resolve_command_method(command)                    # find method to invoke
                    if method:
                        method_params      = command.split(' ')[1:]
                        (text,attachments) = method(slack_event,method_params)                       # invoke method
                    else:
                        text = ":exclamation: GS bot command `{0}` not found. Use `gsbot help` to see a list of available commands".format(method_name)
                        attachments = []
            else:
                return None, None

        except Exception as error:
            text = '*GS Bot command execution error in `handle_command` :exclamation:*'
            attachments = [ { 'text': ' ' + str(error) , 'color' :  'danger'}]
        return text, attachments

    def handle_link_shared(self, slack_event):
        from osbot.api.GS_Bot_Commands import GS_Bot_Commands       # due to circular references
        method        = GS_Bot_Commands.jira
        if slack_event.get('links'):
            method_params = ['link_shared', json.dumps(slack_event.get('links'))]
            return method(slack_event, method_params)

        text = ':point_right: unsupported link'
        return text, []

    def process_event(self, slack_event):
        attachments = []
        try:
            event_type            = slack_event.get('type')

            if    event_type == 'message'    : (text,attachments)  = self.handle_command    (slack_event )    # same handled
            elif  event_type == 'app_mention': (text,attachments)  = self.handle_command    (slack_event )    # for these two events
            elif  event_type == 'link_shared': (text,attachments)  = self.handle_link_shared(slack_event )    # special handler for jira links
            else:
                text = ':point_right: Unsupposed Slack bot event type: {0}'.format(event_type)
        except Exception as error:
            text = '*GS Bot command execution error in `process_event` :exclamation:*'
            attachments = [{'text': ' ' + str(error), 'color': 'danger'}]

        if text is None:
            return None, None

        channel_id = slack_event.get("channel")  # channel command was sent in
        team_id    = slack_event.get("team_id")
        #log_debug("team id: {0}".format(team_id))
        if channel_id is None or team_id is None:
            return { "text": text, "attachments": attachments }
        return self.send_message(channel_id, team_id, text, attachments)

    def process_posted_body(self, postdata):                                        # handle the encoding created by API GW, which uses as transformation
        try:                                                                        # { "body" : $input.json('$' ) }
            return Lambda('gs.slack_interaction').invoke( {"body": postdata })
        except Exception as error:
            return  "Error in processing posted data: {0}".format(str(error))

    def resolve_command_method(self, command):
        try:
            method_name = command.split(' ')[0].split('\n')[0]
            method_name = self.resolve_command_shortcuts(method_name)
            from osbot.api.GS_Bot_Commands import GS_Bot_Commands
            return getattr(GS_Bot_Commands,method_name)
        except AttributeError as error:
            Dev.pprint(error)
            return None

    def resolve_command_shortcuts(self, method_name):
        return Misc.get_value(self.method_shortcuts, method_name, method_name)

    def upload_png_file(self, channel_id, text, file):
        my_file = {
            'file': ('/tmp/myfile.pdf', open(file, 'rb'), 'png')
        }

        payload = {
            "filename"  : 'image.png',
            "token"     : self.bot_token,
            "channels"  : [channel_id],
            "text"      : text
        }
        import requests
        r = requests.post("https://slack.com/api/files.upload", params=payload, files=my_file)

        Dev.pprint(r.text)
        return 42

    def send_message(self,channel_id, team_id, text, attachments = []):
        data     = urllib.parse.urlencode((("token"      , self.bot_token  ),               # oauth token
                                           ("channel"    , channel_id      ),               # channel to send message to
                                           ("team_id"    , team_id         ),
                                           ("text"       , text            ),               # message's text
                                           ("attachments", attachments     )))              # message's attachments
        data     = data.encode("ascii")
        request  = urllib.request.Request(self.slack_url, data=data, method="POST" ) # send data back to Slack
        request.add_header("Content-Type","application/x-www-form-urlencoded")
        context  = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        response = urllib.request.urlopen(request,context = context).read()

        return json.loads(response.decode())

    # @staticmethod
    # def send_via_slack_event(slack_event, text, attachments = []):
    #     channel_id = slack_event["channel"]
    #     API_GS_Bot().send_message(channel_id, text, attachments)