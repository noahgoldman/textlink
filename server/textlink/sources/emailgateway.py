import urllib2,urllib
import smtplib
from email.mime.text import MIMEText

providers = ['%s@message.alltel.com',
'%s@paging.acswireless.com',
'%s@txt.att.net',
'%s@myboostmobile.com',
'%s@messaging.sprintpcs.com',
'%s@tmomail.net',
'%s@mymetropcs.com',
'%s@messaging.nextel.com',
'%s@mobile.celloneusa.com',
'%s@qwestmp.com',
'%s@pcs.rogers.com',
'%s@msg.telus.com',
'%s@email.uscc.net',
'%s@vtext.com',
'%s@vmobl.com',
'%s@txt.windmobile.ca']

def find_email_gateway(_to):
    return ""
    


def text_by_email(_to,_from,_message, carrier_email = '', attachment = 0):
    p = providers
    if carrier_email != '':
        p = [carrier_email]
    p = [ x.replace('%s', _to) for x in p ]
    msg = MIMEText(_message)

    msg['Subject'] = 'TextLink Text'
    msg['From'] = _from
    msg['To'] = _to
    if attachment != 0:
        msg.attach(attachment)

    s = smtplib.SMTP('localhost')
    s.set_debuglevel(1)
    try:
        r = s.sendmail(_from, p, msg.as_string())
        s.quit()
        return r
    except:
        print "FAILURE"
        return -1

#   text_by_email("8023422051", "micmoo@me.com","Things and Stuff")