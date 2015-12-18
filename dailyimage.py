#!/usr/bin/python

import sys
import time
import datetime
import json
import dailyimage
from clientsender import Client, Sender

def main(argv):
    if len(argv) > 2:
        print('usage: dailyimage.py [alternative-config.json]')
        sys.exit()

    # Default to the file 'config.json' if no alternative provided
    if len(argv) == 1:
        client_file_path = 'config.json'
    else:
        # Use user-provided json file path
        client_file_path = argv[1]

    # Load the sender email and client list from the json file
    with open(client_file_path, 'r') as config:
        config_json = json.load(config)

    # For convenience
    clients_json = config_json['clients']
    sender_json = config_json['sender']

    # Create the sender from the dictionary
    sender = Sender(sender_json['email'], sender_json['password'])

    # Convert the dictionaries into usable Client class instances
    clients = []
    for client_json in clients_json:
        clients.append(Client(client_json['email'], client_json['time'], client_json['query']))
    
    # Wait until the current second is 0. Makes it easier.
    while True:
        if datetime.datetime.now().second == 0:
            break

    # Main loop
    while True:
        # Get the current time
        now = datetime.datetime.now()
        for client in clients:
            # If the current time is the client's send time, send the next image
            if now.hour == client.time['hour'] and now.minute == client.time['minute'] and now.second == 0:
                sender.send(client)
        time.sleep(1)

if __name__ == '__main__':
    main(sys.argv)
