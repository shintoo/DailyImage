#!/usr/bin/python
# dailyimage.py - Send images from Google Image search to an email daily

import sys      # argv
import datetime # When to email
import time     # Wait until ^
import client   # Login and send emails
import getimage # Search for and download images

def print_usage():
    print('usage: dailyimage.py sender@provider.com senderpassword target@provider.com time query')
    print('time is in the format HH:MM, such as 10:21 or 15:45')

def main(argv):
    # see print_usage()
    if len(argv) < 6:
        print_usage()
        sys.exit()

    # Login the user and generate a client
    user = client.login(argv[1], argv[2])
    # Set the query to the last argument
    user.query = ''
    for term in argv[5:]:
        user.query += term + ' '


    # Set the time to send the email using the time argument
    send_time = dict(zip(['hour', 'minute'], argv[4].split(':', 2)))

    # Begin the generator using the query
    getimage.get_image(user.query)


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
    for image in getimage.get_image(user.query):
       user.send(image, argv[3]) # Get a new image, send to the client
       time.sleep(60 * 60 * 24) # Wait until time

if __name__ == '__main__':
    main(sys.argv)
