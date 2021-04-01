### Required Libraries ###
from datetime import datetime
from dateutil.relativedelta import relativedelta


### Functionality Helper Functions ###

def parse_int(n):
    """Securely converts a non-integer value to integer."""
    try:
        return int(n)
    except ValueError:
        return float("nan")

def build_validation_result(is_valid, violated_slot, message_content):
    """Define a result message structured as Lex response."""
    if message_content is None:
        return {"isValid": is_valid, "violatedSlot": violated_slot}
    return {
        "isValid": is_valid,
        "violatedSlot": violated_slot,
        "message": {"contentType": "PlainText", "content": message_content},
    }


### Dialog Actions Helper Functions ###

def get_slots(intent_request):
    """Fetch all the slots and their values from the current intent."""
    return intent_request["currentIntent"]["slots"]

def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    """Defines an elicit slot type response."""
    return {"sessionAttributes":session_attributes,"dialogAction":{"type":"ElicitSlot","intentName":intent_name,"slots":slots,"slotToElicit":slot_to_elicit,"message":message},
    }
    
# Define delegate slot type response:
def delegate(session_attributes, slots):
    return {"sessionAttributes":session_attributes,"dialogAction":{"type":"Delegate","slots":slots}}

def close(session_attributes, fulfillment_state, message):
    """Defines a close slot type response."""
    response = {
        "sessionAttributes":session_attributes,
        "dialogAction": {
            "type":"Close",
            "fulfillmentState":fulfillment_state,
            "message":message,
        },
    }
    return response

### Intent Handler ###

def recommend_portfolio(intent_request):
    first_name = get_slots(intent_request)["firstName"]
    age = get_slots(intent_request)["age"]
    investment_amount = get_slots(intent_request)["investmentAmount"]
    risk_level = get_slots(intent_request)["riskLevel"]
    source = intent_request["invocationSource"]
    output_session_attributes = intent_request["sessionAttributes"]
    
    """Performs dialog management and fulfillment for recommending a portfolio."""
    if source == "DialogCodeHook":
        if not first_name:
            return elicit_slot(
                output_session_attributes,
                intent_request['currentIntent']['name'],
                intent_request['currentIntent']['slots'],
                'firstName',
                {'contentType':'PlainText', 'content': 'Thank you for trusting me to help, can you please provide your name?'},
                )
        if first_name and not age:
            return elicit_slot(
                output_session_attributes,
                intent_request['currentIntent']['name'],
                intent_request['currentIntent']['slots'],
                'age',
                {'contentType':'PlainText','content':'How old are you?'},
            )
        if (first_name and age) and (parse_int(age) <= 0) and not investment_amount:
            return elicit_slot(
                intent_request["sessionAttributes"],
                intent_request['currentIntent']['name'],
                intent_request['currentIntent']['slots'],
                'age',
                {'contentType':'PlainText','content':"Age must be greater than 0; let's try that again. How old are you?"},
            )
        if (first_name and age) and (parse_int(age) >= 65) and not investment_amount:
            return elicit_slot(
                intent_request["sessionAttributes"],
                intent_request['currentIntent']['name'],
                intent_request['currentIntent']['slots'],
                'age',
                {'contentType':'PlainText','content':'Sorry, the maximum age to use this service is 64. Please provide an age between 1 and 64.'},
            )
        if first_name and age and not investment_amount:
            return elicit_slot(
                output_session_attributes,
                intent_request['currentIntent']['name'],
                intent_request['currentIntent']['slots'],
                'investmentAmount',
                {'contentType':'PlainText','content':'How much do you want to invest?'},
            )
        if (first_name and age) and (parse_int(investment_amount) < 5000):
            return elicit_slot(
                output_session_attributes,
                intent_request['currentIntent']['name'],
                intent_request['currentIntent']['slots'],
                'investmentAmount',
                {'contentType':'PlainText','content':'The minimum investment amount is $5,000 USD; please provide a greater amount to use our service.'},
            )
        return delegate(output_session_attributes, get_slots(intent_request))
    
    if risk_level:
        if risk_level == 'None':
            initial_recommendation = "100% bonds (AGG), 0% equities (SPY)"
        elif risk_level == 'Very Low':
            initial_recommendation = "80% bonds (AGG), 20% equities (SPY)"
        elif risk_level == 'Low':
            initial_recommendation = "60% bonds (AGG), 40% equities (SPY)"
        elif risk_level == 'Medium':
            initial_recommendation = "40% bonds (AGG), 60% equities (SPY)"
        elif risk_level == 'High':
            initial_recommendation = "20% bonds (AGG), 80% equities (SPY)"
        elif risk_level == 'Very High':
            initial_recommendation = "0% bonds (AGG), 100% equities (SPY)"

    # Return a message with the initial recommendation based on the risk level:
    return close(
        intent_request["sessionAttributes"],
        "Fulfilled",
        {
            "contentType": "PlainText",
            "content": """{} thank you for your information.
            Based on the risk level you defined, my recommendation is to choose an investment portfolio with {}
            """.format(first_name, initial_recommendation),
        },
    )

### Intents Dispatcher ###

def dispatch(intent_request):
    """Called when the user specifies an intent for this bot."""
    intent_name = intent_request["currentIntent"]["name"]
    if intent_name == "RecommendPortfolio":
        return recommend_portfolio(intent_request)
    raise Exception("Intent with name " + intent_name + " not supported")


### Main Handler ###

def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """
    return dispatch(event)