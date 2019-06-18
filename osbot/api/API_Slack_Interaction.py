import datetime
import json
import urllib
from osbot_aws.apis.Lambda import Lambda
from pbx_gs_python_utils.utils.Lambdas_Helpers  import log_to_elk

class API_Slack_Interaction:

    def callback_view_jira_issue(self, data):
        actions     = data['actions']
        key         = actions.pop(0)['value']                    # only handle the first answer
        channel     = data['channel']['id']

        user_id     = data['user']['id']
        params      = ["issue", key]

        return Lambda('pbx_gs_python_utils.lambdas.gs.elastic_jira').invoke( {"params": params, "user": user_id, "channel": channel})

    # def callback_change_issue_status(self, data):
    #     action    = data['actions'].pop(0)
    #     value     = json.loads(action['value'].replace('+',' '))          # bug: replace required due to slash command decoding bug
    #     key       = value['key']
    #     status    = value['status']
    #     status_id = str(value['status_id'])
    #
    #     #key = 'GSBOT-20'
    #     #status = 'Done' #'In Progress'
    #
    #     from gs_jira.API_Jira_GS_CST import API_Jira_GS_CST     # need to make this support hosted JIRA too
    #     api = API_Jira_GS_CST().setup()
    #     api.jira.issue_transition_to(key, status)
    #
    #     return { 'text': 'changing issue status: on key *{0}* to status *{1}* (id: {2})'.format(key, status, status_id)  , 'attachments': [] , 'replace_original': False}

    def callback_jira_dialog_action(self, data):
        return Lambda('gs.jira_dialog').invoke({"type": "jira_dialog_action", "data": data})

    def callback_button_dialog_test(self, data):
        return Lambda('gs.jira_dialog').invoke({"type": "button_dialog_test", "data": data})

    def process_slash_command(self, data):
        try:
            log_to_elk('process_slash_command',data)
            command     = data.get('command')
            attachments = []
            #if command =='/cst':
            #    (text, attachments) = Slash_Cst().process_command(data)
            if command == '/jira':
                result = Lambda('gs.jira_dialog').invoke({ 'type' : 'jira_slash_command', 'data': data })
                if (result                    is not None and \
                    type(result)              is not str  and \
                    result.get('text')        is not None and \
                    result.get('attachments') is not None     ):
                    text        = result.get('text')
                    attachments = result.get('attachments')
                else:
                    text = result
            else:
                text        = ':point_right: unrecongnised Slash Command: {0}'.format(command)
            return { 'text': text, 'attachments':attachments }
        except Exception as error:
            error_message = 'Error in API_Slack_Integration.process slash command: {0}'.format(error)
            log_to_elk(error_message, level='error')
            return {'text': error_message, 'attachments': []}

    def process_dialog_submission(self, data):
        self.save_message_in_elk(data)                                                  # keep a copy of the data submitted in ELK
        Lambda('gs.jira_dialog').invoke({'type': 'dialog_submission', 'data': data})   # if we want to show dialoge validation errors to users then we will need to return this value (see note below)
        #log_to_elk('dialog submission', data)
        #API_Jira_Dialog().handle_dialog_submission(data)
        return { }                                                                      # this is really important or the user will get a nasty error in Slack


    def process_dialog_suggestion(self,data, field_name):

        response = {"options": []}
        callback_id =  data.get("callback_id")
        if callback_id == "issue-suggestion" or callback_id =='issue-search-dialog':

            log_to_elk("data received: {0}".format(data))
            max = 50
            payload = {"action": "search", "data": {"text": data.get('value').strip() , "field" : "Summary", "size" : max}}
            results = Lambda('gs.elastic_search').invoke(payload)
            log_to_elk('Got {0} results from elk'.format(len(results)))

            try:
                for item in results:
                     key        = item.get("Key")
                     summary    = item.get("Summary")
                     if field_name == "label":
                         if len(summary) > 42:
                             summary = summary[0:42] + "..."
                         label_text = "{0:12}   {1}".format(key, summary)
                     else:
                         label_text = summary

                     response['options'].append({field_name: label_text, "value":key })
                if len(response['options']) == max:
                    response['options'].append({field_name: ".... note: max search limit reached: {0}".format(max),"value": "EEEE-1111" })
            except Exception as error:
                response['options'].append({field_name: "Error : {0}".format(error),"value": "AAAAA-1111" })
        else:
            response['options'].append({field_name: "... unsupported  suggestion callback_id: {0}".format(callback_id), "value": "UUUU-1111"})
        #response['options'] = response['options']
        return response

    def process_interactive_action(self,data):
        text        = 'interactive action received'
        attachments = []
        requests.post(data['response_url'],
                      headers={'Content-Type': 'application/json'},
                      data=json.dumps({'text': text, 'attachments': attachments}))
        return {}

    def decode_body_with_payload(self,body):
        raw_json = urllib.parse.unquote(body).split('=').pop()  # convert the data back to json (need to pick the 2nd parameter
        return json.loads(raw_json)  # load into Python object

    def decode_body_form_encoded(self, body):
        unquoted = urllib.parse.unquote(body)  # convert into python object
        data = {}
        for item in unquoted.split('&'):
            key_value = item.split('=')
            data[key_value[0]] = key_value[1]
        return data

    def handle_request(self, event):
        try:
            body     = event.get('body')
            raw_json = urllib.parse.unquote(body).split('=').pop()  # convert the data back to json (need to pick the 2nd parameter
            data     = json.loads(raw_json)                         # load into Python object
            log_to_elk('osbot.lambdas.slack_callback_handle_request', data=data, index='slack_interaction', category='API_Slack_Interaction')
            return Lambda('osbot_jira.lambdas.slack_actions').invoke(data)

            # if body:
            #     if   'type%22%3A%22interactive_message' in body: return self.process_action            (self.decode_body_with_payload(body)) # this is an interactive_message response
            #     elif 'type%22%3A%22dialog_submission'   in body: return self.process_dialog_submission (self.decode_body_with_payload(body))
            #     elif 'type%22%3A%22message_action'      in body: return self.process_interactive_action(self.decode_body_with_payload(body))
            #     elif 'type%22%3A%22dialog_suggestion'   in body: return self.process_dialog_suggestion (self.decode_body_with_payload(body), "label")
            #     else                                           : return self.process_slash_command     (self.decode_body_form_encoded(body))
        except Exception as error:
            message = 'Sorry could not process request, the error was: {0}'.format(error)
            log_to_elk('Error in osbot.lambdas.slack_callback_handle_request',
                       data     = message                ,
                       level    = 'error'                ,
                       index    = 'slack_integrations'   ,
                       category = 'API_Slack_Interaction')
            log_to_elk(message)
            return message
        return 'Sorry could not process the request'