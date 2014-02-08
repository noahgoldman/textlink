import urllib2,urllib
import smtplib
from email.mime.text import MIMEText
from textlink import Session
from sqlalchemy.orm.exc import NoResultFound
from textlink.models import Entry, Phone, List, PhoneCarrier


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
        print str(e)
        print "MIKEY2"

def get_possible_carriers(number):
    session = Session()
    try:
        phone = session.query(Phone).filter_by(number=number).one()
        carriers = session.query(PhoneCarrier).filter_by(phone_id=phone.id, possible=True).all()
    except NoResultFound:
        return None
    else:
        return carriers

def text_by_email(_to,_from, _message, carrier_email = '', attachment = 0):
    session = Session()
    if carrier_email != '':
        tos = [carrier_email]
    else:
        carriers = get_possible_carriers(_to)
        tos = [x.email for x in carriers]
    if tos == []:
        return None
    msg = MIMEText(_message)

    msg['Subject'] = 'TextLink Text'
    msg['From'] = _from
    msg['To'] = _to
    if attachment != 0:
        msg.attach(attachment)

    s = smtplib.SMTP('mail.micmoo.org')
    s.login('tmp@micmoo.org','luigi193')
    s.set_debuglevel(1)
    try:
        r = s.sendmail(_from, p, msg.as_string())
        print r
        s.quit()
        return r or None
    except:
        print "FAILURE"
        return -1


#   text_by_email("8023422051", "micmoo@me.com","Things and Stuff")