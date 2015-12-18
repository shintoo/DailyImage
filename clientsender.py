#/usr/bin/python
# senderclient.py - this file is part of dailyimage
#   Log in and send emails to clients

import sys               # argv, exit
import smtplib           # for email ...
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase      import MIMEBase
from email.mime.image    import MIMEImage
from email.MIMEText      import MIMEText
from email               import Encoders
from getimage            import get_image

class Client:
    '''
    class Client
    attributes:
        email   string                            - The user's email
        query   string                            - Image search query
        time    dictionary 'hour', 'minute'       - Time to send
    '''
    def __init__(self, email, timestring, query):
        self.email = email
        # Build the dictionary, i.e timestring='15:35' gives {'hour': 15, 'minute': 35}
        self.time = dict(zip(['hour', 'minute'], [int(i) for i in timestring.split(':', 2)]))
        self.query = query
        # Start the generator to find images of the client's query
        self.image_generator = get_image(query)

class Sender:
    '''
    class Sender
    attributes:
        smtpObj smtplib.SMTP
    '''
    def __init__(self, email, password):
        '''
        arguments:
            email: string
            password: string
    
        Using the email and password, this function logs into the email on the
        provider's SMTP server and returns the generated client
        '''
        self.email = email

        # Contains the SMTP server and the appropriate port depending on the email
        server = []
        with open('.smtp_servers') as f:
            # Find the appropriate server and port from the user's email
            for line in f:
                elems = line.split(None, 3)
                if elems[0] in email:
                    server = dict(zip(['provider', 'server', 'port'], line.split(None, 3)))
                    break

        # Only some email providers work, see .smtp_servers for details
        if not server:
            raise ValueError('Could not find an SMTP server for that email provider: ' + email)

        # Create a client and connect to the SMTP server
        self.smtpObj = smtplib.SMTP(server['server'], server['port'])
        self.smtpObj.ehlo()
        self.smtpObj.starttls()
        self.smtpObj.login(email, password)

    def send(self, client):
        '''Send an image to the email'''

        body = 'Here is your daily ' + client.query[:-1] + '!\n\nRegards, DailyImage'

        # Create the email message
        msg = MIMEMultipart()
        msg['Subject'] = 'Your Daily ' + client.query
        msg['From'] = self.email
        msg['To'] = client.email
        msg.attach(MIMEText(body.encode('utf-8')))

        # Get the next image and attach it
        image = next(client.image_generator)
        attachment = MIMEImage(image, 'daily-' + client.query)
        msg.attach(attachment)

        # Off it goes!
        self.smtpObj.sendmail(self.email, client.email, msg.as_string())

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
