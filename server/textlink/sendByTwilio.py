from twilio.rest import TwilioRestClient


def sendSMS(sid, tok, sender, reciever, msg):
    account_sid = sid
    auth_token  = tok
    client = TwilioRestClient(account_sid, auth_token)
 
    message = client.sms.messages.create(body=msg,
        to=reciever,   
        from_=sender) 
    print message.sid
