#!/usr/bin/python
# getimage.py - this file is part of dailyimage
#   Retrieve an image from a google image search

import sys          # argv
import re           # finding images
import requests     # downloading results and images
import bs4          # finding images

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

def main(argv):
    if len(argv) != 2:
        print('usage: getimage.py query')

    get_image(argv[1]) # begin generator
    
    print('Saving ' + argv[1] + '_image...')
    fp = open(argv[1] + '_image', 'wb')
    fp.write(next(get_image(argv[1])))
    fp.close()

if __name__ == '__main__':
    main(sys.argv)
