import urllib2,urllib
import smtplib
from email.mime.text import MIMEText
from textlink import Session
from sqlalchemy.orm.exc import NoResultFound
from textlink.models import Entry, Phone, List, PhoneCarrier 
import mailbox
import getpass
from sqlalchemy import delete
from flufl.bounce import all_failures, scan_message
import imaplib
import email


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
  #  print send_mail('Subject: hello\n\nmessage', 'tmp@micmoo.org', [ '8023422051@vtext.com', '8023422051@txt.att.net' ], 'mail.micmoo.org',25,'normal','tmp@micmoo.org','luigi193') 
  return ""
  

def checkMailForBounce():
    mail = imaplib.IMAP4_SSL('mail.micmoo.org')
    mail.login('textlink@micmoo.org', 'micmoo40')
    #mail.list()
    mail.select("inbox") # connect to inbox.
    result, items = mail.uid('search', None, "ALL") # search and return uids instead
    items = items[0].split() # getting the mails id
    session = Session()
    for emailid in items:
        resp, data = mail.fetch(emailid, "(RFC822)") #
        email_body = data[0][1]     
        damail = email.message_from_string(email_body) # parsing the mail content to get a mail object
        fails = scan_message(damail)
        mail.store(emailid, '+FLAGS', '\\Deleted')
        if len(fails) == 0: 
            continue
        for fail_s in fails:
            r = session.query(PhoneCarrier).filter_by(email=fail_s).all()
            if len(r) == 0:
                continue
            r = r[0]
            session.delete(r)
    session.commit()
    return None
        
        

def init_possible_carriers(number):
    session = Session()
    try:
        phone = session.query(Phone).filter_by(number=number).one()
    except NoResultFound:
        return None
    try:
        for p in providers:
            carrier = PhoneCarrier(phone.phone_id, p.replace('%s', number))
            print "MIKEY\n"
            session.add(carrier)
        session.commit()
    except Exception ,e:
        pass

def get_possible_carriers(number):
    session = Session()
    try:
        phone = session.query(Phone).filter_by(number=number).one()
        carriers = session.query(PhoneCarrier).filter_by(phone_id=phone.phone_id, possible=True).all()
    except NoResultFound:
        return None
    else:
        return carriers

def text_by_email(_to,_from, _message, carrier_email = '', attachment = 0):
    session = Session()
    if 0:#carrier_email != '':
        tos = [carrier_email]
    else:
        carriers = get_possible_carriers(_to)
        tos = [x.email for x in carriers]
        print tos
    if tos == []:
        return None
    msg = MIMEText(_message)

    msg['Subject'] = 'TextLink Text'
    f = "textlink@micmoo.org"
    
    msg['From'] = f
    msg['To'] = str(_to)
        
    if attachment != 0:
        msg.attach(attachment)

    s = smtplib.SMTP('mail.micmoo.org')
    s.login('textlink@micmoo.org','micmoo40')
    s.set_debuglevel(1)
    try:
        r = s.sendmail(f, tos, msg.as_string())
        s.quit()
        return r or None
    except Exception, e:
        print "FAILURE"
        print e
        return -1


