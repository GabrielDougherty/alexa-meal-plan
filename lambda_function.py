#!/usr/bin/env python

import urllib.request
import json

def lambda_handler(event, context):
    # check if application ID is right
    if (event['session']['application']['applicationId'] !=
            "amzn1.ask.skill.0b57ef85-b53b-4317-9b55-4f417d83c822"):
        raise ValueError("Invalid Application ID")

    
    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "MyMealPlanIsIntent":
        return set_plan_in_session(intent, session)
    elif intent_name == "GetTargetMealsIntent":
        return gen_target_from_session(intent, session)
    else:
        raise ValueError("Invalid intent: " + intent_name)


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.
    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here

# --------------- Functions that control the skill's behavior ------------------


def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the Meal Planner. First, tell me your meal " \
                    "plan type by saying, \"My meal plan type is Block 210\" " \
                    "or \"My meal plan type is Week 14.\" Then ask me for your " \
                    "target number of meals by saying, \"I have 16 meals, what " \
                    "is my target?"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please tell me your plan type by saying, \"My meal plan " \
                    "type is Week 14.\" See the Alexa App for more examples."

    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def set_plan_in_session(intent, session):
    """ Sets the plan in the session and prepares the speech to reply to the
    user.
    """
    
    card_title = intent['name']
    session_attributes = {}

    # get meal plan type and count, if they exist
    if 'PlanType' in intent['slots'] and intent['slots']['PlanType']['value']:
        plan_type = intent['slots']['PlanType']['value']
        session_attributes.update(create_plan_type_attributes(plan_type))

    if 'PlanMeals' in intent['slots'] and intent['slots']['PlanMeals']['value']:
        plan_meals = intent['slots']['PlanMeals']['value']
        session_attributes.update(create_plan_meals_attributes(plan_meals))

    # build speech_output from above processing
    speech_output = build_speech_from_plan(plan_type, plan_meals)

    reprompt_text = ". You can ask for meal plan information by saying, " \
                    "what's my meal plan?"
    
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


# helper that builds speech_output in above function
def build_speech_from_plan(plan_type, plan_meals):
    if plan_type and plan_meals:
        speech_output = "I now know your meal plan is " + \
                        plan_type + ", and you have " + \
                        plan_meals + " meals. " + \
                        "You can ask for meal plan information by saying, " \
                        "what's my meal plan?"
    elif plan_type:
        speech_output = "I now know your meal plan is " + \
                        plan_type + \
                        ". You can ask for meal plan information by saying, " \
                        "what's my meal plan?"
    elif plan_meals:
        speech_output = "I now know you have " + \
                        plan_type + \
                        " meals. You can ask for meal plan information by saying, " \
                        "what's my meal plan?"
    else:
        speech_output = "I'm not sure what your meal plan is. " \
                        "You can tell me your meal plan by saying, " \
                        "\"My meal plan type is Block 210\", or " \
                        "\"My meal plan type is Week.\""
    return speech_output
    

def create_plan_type_attributes(plan_type):
    return {"planType": plan_type}

def create_plan_meals_attributes(plan_meals):
    return {"planMeals": plan_meals}

def gen_target_from_session(intent, session):
    session_attributes = {}
    reprompt_text = None


    if "PlanMeals" in session.get('attributes', {}) and session['attributes']['PlanMeals']:
        num_meals = session['attributes']['PlanMeals']
        speech_output = "You have " + num_meals + \
                        " meals."
        should_end_session = True
    else:
        speech_output = "I'm not sure what your meal plan is. " \
                        "You can say, I have a block meal plan."
        should_end_session = False

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

# --------------- Helpers that build all of the responses ----------------------


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': 'SessionSpeechlet - ' + title,
            'content': 'SessionSpeechlet - ' + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
}

