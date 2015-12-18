#DailyImage
### Subscribe with a query to recieve a new image daily.

## How do I use DailyImage?
First, you have to enter your information into the JSON file.

```
{
    "sender": {
        "email"   : "your.email@your.provider.com",
        "password": "your-password"
    },
    
    "clients": [
        {
            "email": "client1@emailprovider.com",
            "query": "Client 1 Image Query",
            "time" : "12:00"
        },
        {
            "email": "client2@emailprovider.com",
            "query": "Client 2 Image Query",
            "time" : "15:30"
        }
    ]
}
```

### Sender

This field holds your email information, and is used to send the emails.
"email" is your email, "password" is your email's password.

If this sounds sketchy, you're welcome to make an additional email just for use with this program.

### Clients

"clients" is a list of clients that will be receiving service from DailyImage. The "email" field is the client's email. This is where the image will be sent to. The "query" field is the query for the image. DailyImage will grab a new image each day from Google Images using this query. "time" is the time that the image will be sent each day.

### Usage

```
# Simply run dailyimage.py to use 'config.json'
$ ./dailyimage.py
# Or, use an alternative JSON file:
$ ./dailyimage.py alternative.json
```

### Installation

```
git clone https://github.com/shintoo/DailyImage.git
# optional:
cd DailyImage
chmod +x dailyimage.py
```

### Dependencies

DailyImage is a Python 2 program. It requires the following Python modules:

* BeautifulSoup (bs4)
* requests
* json
