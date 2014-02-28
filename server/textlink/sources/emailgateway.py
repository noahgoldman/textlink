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
  print send_mail('Subject: hello\n\nmessage', 'tmp@micmoo.org', [ '8023422051@vtext.com', '8023422051@txt.att.net' ], 'mail.micmoo.org',25,'normal','tmp@micmoo.org','luigi193') 
  return ""
  
  
class EmailBox(object):
    current = 0
    def __init__(self,box):
        self.mail = imaplib.IMAP4_SSL('mail.micmoo.org')
        self.email = box + "@micmoo.org"
        self.mail.login(box + '@micmoo.org', 'micmoo40')
        self.mail.select("inbox") # connect to inbox.
        result, self.items = mail.uid('search', None, "ALL") # search and return uids instead
        self.items = items[0].split() # getting the mails id
    
    def next(self):
        if (len(self.items) == 0):
            return False
        emailid = self.items.pop(0)
        try:
            resp, data = self.mail.fetch(emailid, "(RFC822)") #
        except Exception as e:
            next
        email_body = data[0][1]     
        damail = email.message_from_string(email_body) # parsing the mail content to get a mail object
        return damail, emailid
        
    def parseForReturns(self, damail = 0, emailid = 0 ):
        if (damail == 0):
            damail, emailid = self.next()
        fails = scan_message(damail)
        if len(fails) != 0:
            mail.store(emailid, '+FLAGS', '\\Deleted')
        for fail_s in fails:
            r = session.query(PhoneCarrier).filter_by(email=fail_s).all()
            if len(r) == 0:
                continue
            r = r[0]
            session.delete(r)
        return fails      
    
    def parseForResponse(self, damail, emailid):
        if (damail == 0):
            damail, emailid = self.next()
        # Do Email Parsing for Email Responses from Texts.
        
    def parseReturns():
        email, emailid = self.next()
        while (email != False):
            self.parseForReturns(email, emailid)
            email, emailid = self.next()
        
    def parseAll():
        email, emailid = self.next()
        while (email != False):
            self.parseForResponse(email, emailid)
            email, emailid = self.next()
        
    
def check_for_responces():
    box = EmailBox("textlink")
    box.parseAll()
    

def checkForBounces():
    box = EmailBox("textlink")
    box.parseReturns()
    

def init_possible_carriers(number):
    session = Session()
    try:
        phone = session.query(Phone).filter_by(number=number).one()
    except NoResultFound:
        return None
    try:
        for p in providers:
            carrier = PhoneCarrier(phone.phone_id, p.replace('%s', number))
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


