from twilio.rest import TwilioRestClient

def sendSMS(sid, tok, sender, reciever, msg):
    account_sid = getenv('TEXTLINK_TWILIO_SID', '')
    auth_token  = getenv('TEXTLINK_TWILIO_AUTH', '')
    client = TwilioRestClient(account_sid, auth_token)
 
    message = client.sms.messages.create(body=msg,
        to=reciever,   
        from_=sender) 
    print message.sid
