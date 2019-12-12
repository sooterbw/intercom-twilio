# intercom-twilio
A basic Flask app that integrates Twilio with Intercom. This allows admins to interact with users via text message through Intercom.

## Install Dependencies
```
pip install Flask
pip install Twilio
pip install python-intercom
```

## Setup app.py
Begin with the basic Hello World file found in the Flask documentation with ```debug=True```.
```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World!'

if __name__ == '__main__':
    app.run(debug=True)
```

## Setup Phone # and Twilio Credential
If you have not already, then you will need to create a Programmable SMS account with [Twilio](https://www.twilio.com/sms/pricing/us). 
Purchase a phone number and grab your API credentials.
This information can be found on your Text Support Dashboard within [Twilio's console](https://www.twilio.com/console).

img placeholder

## Setup Twilio Client
Input your credentials and phone number from your Twilio account. 
We will also need to import the ```request``` method from flask so that we can capture the data from Twilio's webhook.


```python
# app.py
from flask import Flask, request
from twilio.rest import Client as twil_Client

TWILLIO_ACCOUNT_SID = 'Your_Twilio_SID'
TWILIO_AUTH_TOKEN = 'Your_Auth_Token'
TWILIO_PHONE_NUMBER = 'Your_Twilio_Number'

# Twilio Client
twilio = twil_Client(TWILLIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
```


