#DailyImage
#### Email a new image every day.
WIP

Just started learning python so I thought I'd make something that uses the neat web stuff.

###What this program does
* Searches Google Images with your query
* Downloads an image
* Emails it to the target email at the time specified daily
* Violates Google's terms of service

###The very ugly usage
'''
dailyimage.py email password targetemail hh:mm query
'''

This will email targetemail an image from a Google Image search of query from your email.

Yes, your email password is needed to log in, in order to send emails.

No, this program does not send your email password to me. Go ahead, look.

###What's to come
Working on getting it into a config file instead of all cl args. That way, you could customize the subject line and body of the email. Don't get your hopes up, though.
