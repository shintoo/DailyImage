#/usr/bin/python
# client.py - this file is part of dailyimage
#   Log in and send emails

import sys               # argv, exit
import smtplib           # for email ...
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase      import MIMEBase
from email.mime.image    import MIMEImage
from email.MIMEText      import MIMEText
from email               import Encoders

class Client:
    '''
    class Client
    attributes:
        email   string       - The user's email
        smtpObj smtplib.SMTP - SMTP client
        query   string       - Image search query
    
    methods:
        send(self, target_email, image
            The client sends an email with the image attached to the target email
    '''
    def __init__(self, email, smtpObj, query):
        self.email = email
        self.smtpObj = smtpObj
        self.query = query

    def send(self, image, target_email):
        '''Send an image to the email'''

        body = 'Here is your daily ' + self.query[:-1] + '!\n\nRegards, DailyImage'

        # Create the email message
        msg = MIMEMultipart()
        msg['Subject'] = 'Your Daily ' + self.query
        msg['From'] = self.email
        msg['To'] = target_email
        msg.attach(MIMEText(body.encode('utf-8')))

        # attach the image
        attachment = MIMEImage(image, 'daily-' + self.query)
        msg.attach(attachment)

        # Off it goes!
        self.smtpObj.sendmail(self.email, target_email, msg.as_string())

def login(email, password):
    '''
    function login
    
    arguments:
        email: string
        password: string
    
    returns:
        class Client
    
    Using the email and password, this function logs into the email on the
    provider's SMTP server and returns the generated client
    '''

    # Contains the SMTP server and the appropriate port depending on the email
    f = open('.dailyimage_servers')

    # Find the appropriate server and port from the user's email
    for line in f:
        elems = line.split(None, 3)
        if elems[0] in email:
            server = dict(zip(['provider', 'server', 'port'], line.split(None, 3)))
            break

    # Create a client and connect to the SMTP server
    client = Client(email, smtplib.SMTP(server['server'], server['port']), None)
    client.smtpObj.ehlo()
    client.smtpObj.starttls()
    client.smtpObj.login(email, password)

    return client

def main(argv):
    if len(argv) != 3:
        print('usage: login.py email password')
        sys.exit()

    try:
        client = login(argv[1], argv[2])
    except smtplib.SMTPAuthenticationError as e:
        print('Error: Could not log in. ')
        print((e.__str__().split('\'')[1]))
        sys.exit()

    print('Login successful')
    client.smtpObj.quit()

if __name__ == '__main__':
    import sys
    main(sys.argv)
