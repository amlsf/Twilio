# https://github.com/twilio/twilio-python
# http://quest.twilio.com/
# (510) 788-2674
# https://twilio-python.readthedocs.org/en/latest/usage/twiml.html
# https://twilio-python.readthedocs.org/en/latest/api/twiml.html
# https://www.twilio.com/docs/quickstart/python/twiml/record-caller-leave-message
# http://flask.pocoo.org/docs/quickstart/
# https://github.com/twilio

import os

from flask import Flask
from flask import Response
from flask import request
from flask import render_template
from twilio import twiml
from twilio.rest import TwilioRestClient

# Pull in configuration from system environment variables
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
TWILIO_NUMBER = os.environ.get('TWILIO_NUMBER')

# create an authenticated client that can make requests to Twilio for your
# account.
client = TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Create a Flask web app
app = Flask(__name__)

# Render the home page
@app.route('/')
def index():
    return render_template('index.html')

# Handle a POST request to send a text message. This is called via ajax
# on our web page
@app.route('/message', methods=['POST'])
def message():
    # Send a text message to the number provided
    message = client.sms.messages.create(to=request.form['to'],
                                         from_=TWILIO_NUMBER,
                                         body='Good luck on your Twilio quest!')

    # Return a message indicating the text message is enroute
    return 'Message on the way!'

# Handle a POST request to make an outbound call. This is called via ajax
# on our web page
@app.route('/call', methods=['POST'])
def call():
    # Make an outbound call to the provided number from your Twilio number
    call = client.calls.create(to=request.form['to'], from_=TWILIO_NUMBER, 
                               url='http://twimlets.com/message?Message%5B0%5D=http://demo.kevinwhinnery.com/audio/zelda.mp3')

    # Return a message indicating the call is coming
    return 'Call inbound!'

# Generate TwiML instructions for an outbound call
@app.route('/hello')
def hello():
    response = twiml.Response()
    response.say('Hello there! You have successfully configured a web hook.')
    response.say('Good luck on your Twilio quest!', voice='woman')
    return Response(str(response), mimetype='text/xml')

# Chapter 1
# Generate TwiML instructions for an outbound call
@app.route('/incoming/sms', methods = ["POST"])
def text():
    response = twiml.Response()
    response.message('I just responded to a text message. Huzzah!.')
    return Response(str(response), mimetype='text/xml')

# Chapter 1
# @app.route('/incoming/call', methods = ["POST"])
# def calls():
#     response = twiml.Response()
#     response.say('I just responded to a phone call.', voice='woman')
#     return Response(str(response), mimetype='text/xml')

# Chapter 2
# @app.route('/incoming/call', methods = ["POST"])
# def ivr():
#     twiml = '<?xml version="1.0" encoding="UTF-8"?> \
# <Response> \
#     <Gather timeout="10" finishOnKey="*" action="/incoming/gather" method="POST"> \
#         <Say>Please enter one for help and two for nothing followed by star.</Say> \
#     </Gather> \
# </Response>'
#     return Response(twiml, mimetype="text/xml")

# @app.route('/incoming/gather', methods = ['POST'])
# def gather():
#     digits = request.form['Digits']

#     if (digits == '1'):
#         response = twiml.Response()
#         response.say('Congrats this is 1 for help option.', voice='woman')
#         return Response(str(response), mimetype='text/xml')
#     elif (digits == '2'):
#         response = twiml.Response()
#         response.say('Congrats this is 2 for Nothing option.', voice='woman')
#         return Response(str(response), mimetype='text/xml')
#     else:
#         response = twiml.Response()
#         response.say('Please select 1 OR 2', voice='woman')
#         response.redirect(url='/incoming/call')
#         return Response(str(response), mimetype='text/xml')


# Chapter 3            
@app.route('/incoming/call', methods = ["POST"])
def ivr():
    twiml = '<?xml version="1.0" encoding="UTF-8"?> \
<Response> \
    <Gather timeout="10" finishOnKey="*" action="/incoming/gather" method="POST"> \
        <Say>Please enter one to listen to a message and two to record followed by star.</Say> \
    </Gather> \
</Response>'
    return Response(twiml, mimetype="text/xml")

@app.route('/incoming/gather', methods = ['POST'])
def gather():
    digits = request.form['Digits']

    if (digits == '1'):
# Play
        recording_url = request.values.get("RecordingUrl", None)
        resp = twiml.Response()
        resp.say("Thanks for howling... take a listen to what you howled.")
        resp.play(recording_url)
        resp.say("Goodbye.")
        return str(resp)

# Record
    elif digits == "2":
        resp = twiml.Response()
        resp.say("Record your monkey howl after the tone.")
        resp.record(maxLength="30", action="/handle-recording")
        return str(resp)
    else:
        response = twiml.Response()
        response.say('Please select 1 OR 2', voice='woman')
        response.redirect(url='/incoming/call')
        return Response(str(response), mimetype='text/xml')


if __name__ == '__main__':
    # Note that in production, you would want to disable debugging
    app.run(debug=True)