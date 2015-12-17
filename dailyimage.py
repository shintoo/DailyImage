#/usr/bin/python
# dailyimage.py - Recieve images of whatever you like in your email every day.

import sys               # argv, exit
import datetime          # when to email
import time              # wait until ^
import smtplib           # for email ...
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase      import MIMEBase
from email.mime.image    import MIMEImage
from email               import Encoders
import requests          # for downloading search results, images
import bs4               # for finding images in search results
import re                # "

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

        # Create the email message
        msg = MIMEMultipart()
        msg['Subject'] = 'Your Daily ' + self.query
        msg['From'] = self.email
        msg['To'] = target_email

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

def get_image(query):
    '''
    function get_image
    generator

    arguments:
        query: string

    yields:
        Raw image data retrieved from a google image search of the query
    '''

    # URL for the image search
    url = 'https://www.google.com/search?tbm=isch&q=' + query
    # Download the result
    res = requests.get(url)
    # Check for error code
    res.raise_for_status()

    # Generate the parser
    Soup = bs4.BeautifulSoup(res.text, 'lxml')

    # Find each image - in this case, the thumbnail of each result
    images = Soup.findAll('img')
    for img in images:
        # Find all images with 'gstatic.com' in their src
        search = re.search('gstatic.com', img['src'])
        if search:
            # Download the image
            raw_image = requests.get(img['src'])
            raw_image.raise_for_status()
            # yield the raw binary data
            yield raw_image.content

def print_usage():
    print('usage: dailyimage you@mail.com yourpassword target@mail.com time query') 
    print('It is perfectly acceptable for you to send the emails to yourself.')

def main(argv):
    # see print_usage()
    if len(argv) < 6:
        print_usage()
        sys.exit()

    # Login the user and generate a client
    client = login(argv[1], argv[2])
    # Set the query to the last argument
    client.query = ''
    for term in argv[5:]:
        client.query += term + ' '


    # Set the time to send the email using the time argument
    send_time = dict(zip(['hour', 'minute'], argv[4].split(':', 2)))

    # Begin the generator using the query
    get_image(client.query)


    # Wait until the correct time to begin
    while True:
        # break if at the correct time
        now = datetime.datetime.now()
        if now.hour == int(send_time['hour']) and now.minute == int(send_time['minute']):
            break
        # Check every 15 seconds
        time.sleep(15)
 
    print('starting')

    # Send the first image, wait one day, send next image, ad infinitum
    for image in get_image(client.query):
       client.send(image, argv[3]) # Get a new image, send to the client
       time.sleep(60 * 60 * 24) # Wait until time

if __name__ == '__main__':
    main(sys.argv)
