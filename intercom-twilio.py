from flask import Flask, request
from twilio.rest import Client as twil_Client
from intercom.client import Client as int_Client
import json
import re

TWILLIO_ACCOUNT_SID = 'Twilio Account SID'
TWILIO_AUTH_TOKEN = 'Twilio Authentication Token'
INTERCOM_AUTH_TOKEN = 'Intercom Authentication Token'
TWILIO_PHONE_NUMBER = 'Phone Number'

# API Clients
twilio = twil_Client(TWILLIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
intercom = int_Client(INTERCOM_AUTH_TOKEN)

# remove html tags from body of Intercom messages
def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

app = Flask(__name__)

@app.route('/sms', methods=['POST'])
def twilio_webhook():
    if request.method == 'POST':
        # twilio content is x-www-form-urlencoded
        sender = request.form['From']
        body = request.form['Body']
        user = intercom.users.create(user_id=sender)

        if intercom.users.find(user_id=sender):
            conversations = intercom.conversations.find_all(type='user', user_id=sender)
            last_convo = conversations[0].id
            intercom.conversations.reply(
                id=last_convo,
                type='user',
                user_id=sender,
                body=body,
                message_type='comment'
            )
        else:
            intercom.messages.create(**{
                "from": {
                    "type": "user",
                    "id": user.id
                },
                "body": body
            })
        print(sender)
        return '', 200

@app.route('/intercom', methods=['POST'])
def intercom_webhook():
    try:
        if request.method == 'POST':
            data = json.loads(request.data)
            user_phone = data['data']['item']['user']['user_id']
            if user_phone[0] == '+':
                # conversation parts is used in replies
                conv_parts = data['data']['item']['conversation_parts']['conversation_parts']
                # conversation message is used in new messages created in Intercom
                conv_message = data['data']['item']['conversation_message']['body']
                bodyhtml = conv_parts[0]['body'] if len(conv_parts) > 0 else conv_message
                # purge element tags
                body = cleanhtml(bodyhtml)
                twilio.messages.create(
                    body=body,
                    from_=TWILIO_PHONE_NUMBER,
                    to=user_phone
                )
                return '', 200
            else:
                print("Non-SMS Message")
                return '', 200
    except:
        return '', 200

if __name__ == '__main__':
    app.run(debug=True)