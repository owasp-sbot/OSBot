from osbot_aws.apis.Lambda import load_dependency


def run(event, context):
    # this Lambda function is triggered by this API GW method https://545ojrb6r0.execute-api.eu-west-2.amazonaws.com/dev/event-handler
    try:
        from osbot.api.API_GS_Bot import log_debug
        #log_debug("In slack callback {0} :".format(event), category='gs_bot')
        #load_dependency('elastic-slack')
        #load_dependency('requests')

        from osbot.api.API_Slack_Interaction import API_Slack_Interaction
        return API_Slack_Interaction().handle_request(event)

    except Exception as error:
        from osbot.api.API_GS_Bot import log_debug
        log_debug("Error processing request: {0}".format(error), data=event, category='gs_bot')
        return "500 Error: {0}".format(error)