from twilio.rest import TwilioRestClient
import os

def sendSMS(sid, tok, sender, reciever, msg):
    account_sid = os.getenv('TEXTLINK_TWILIO_SID', '')
    auth_token  = os.getenv('TEXTLINK_TWILIO_AUTH', '')
    client = TwilioRestClient(account_sid, auth_token)
 
    message = client.sms.messages.create(body=msg,
        to=reciever,   
        from_=sender) 
    print message.sid
