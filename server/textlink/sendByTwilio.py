from twilio.rest import TwilioRestClient


def sendSMS(sid, tok, sender, reciever, msg):
    account_sid = sid
    auth_token  = tok
    client = TwilioRestClient(account_sid, auth_token)
 
    message = client.sms.messages.create(body=msg,
        to=reciever,   
        from_=sender) 
    print message.sid

sendSMS("AC0955b5ae6e4e14861d9e1f61e7d0680f","ee7833a07032d4a600f47a12aa6af464", "+17324105138", "+19086702635", "Yo") 
