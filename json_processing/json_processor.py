import json, operator, os, ssl, sys
from urllib.request import Request, urlopen
from PIL import Image
from shutil import copyfileobj

"""
This file will process the json data from the Instagram Scraper
"""

def process(PATH_TO_JSON_FILE):
    #deleting any non-image type posts and overwriting the file
    with open(PATH_TO_JSON_FILE, 'r') as data_file:
        data = json.load(data_file)
    for element in data:
        if 'type' in element != 'image':
            del element
    with open(PATH_TO_JSON_FILE, 'w') as data_file:
        data = json.dump(data, data_file)
    #sorting data by likes
    with open(PATH_TO_JSON_FILE) as data_file:
        data = json.load(data_file)
        #sorting by likes
        data.sort(reverse=True, key = operator.itemgetter('likesCount'))
        #getting top 300 images
        popular_posts = data[:300]
        #getting bottom 300 images
        not_popular_posts = data[-300:]
        #getting middle images
        starting_point = round(len(data)*0.5)
        medium_posts = data[(starting_point-150):(starting_point+150)]
        #getting medium low images
        starting_point = round(len(data)*0.25)
        medium_low_posts = data[(starting_point-150):(starting_point+150)]
        #getting medium high images
        starting_point = round(len(data)*0.75)
        medium_high_posts = data[(starting_point-150):(starting_point+150)]
    """
    Starting Image Loading
    """


    print('Creating popular images...')
    ssl._create_default_https_context = ssl._create_unverified_context
    os.chdir(os.path.abspath(os.path.join(os.path.abspath(__file__), '..', '..','selfies/popular')))
    for index, post in enumerate(popular_posts):
        req = Request(
            post['displayUrl'],
            data=None,
            headers={
                 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.3'
            }
        )
        with urlopen(req) as instream, open(f'p_img_{index}.jpg', 'wb') as outfile:
            copyfileobj(instream, outfile)
        img = Image.open(f'p_img_{index}.jpg')
        img.save(f'p_img_{index}.jpg')
        

    print('Creating not popular images...')
    os.chdir(os.path.abspath(os.path.join(os.path.abspath(__file__), '..', '..','selfies/not_popular')))
    for index, post in enumerate(not_popular_posts):
        req = Request(
            post['displayUrl'],
            data=None,
            headers={
                 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.3'
            }
        )
        with urlopen(req) as instream, open(f'np_img_{index}.jpg', 'wb') as outfile:
            copyfileobj(instream, outfile)
        img = Image.open(f'np_img_{index}.jpg')
        img.save(f'np_img_{index}.jpg')


    print('Creating medium images...')
    os.chdir(os.path.abspath(os.path.join(os.path.abspath(__file__), '..', '..','selfies/medium')))
    for index, post in enumerate(medium_posts):
        req = Request(
            post['displayUrl'],
            data=None,
            headers={
                 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.3'
            }
        )
        with urlopen(req) as instream, open(f'm_img_{index}.jpg', 'wb') as outfile:
            copyfileobj(instream, outfile)
        img = Image.open(f'm_img_{index}.jpg')
        img.save(f'm_img_{index}.jpg')


    print('Creating medium low images...')
    os.chdir(os.path.abspath(os.path.join(os.path.abspath(__file__), '..', '..','selfies/low_medium')))
    for index, post in enumerate(medium_low_posts):
        req = Request(
            post['displayUrl'],
            data=None,
            headers={
                 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.3'
            }
        )
        with urlopen(req) as instream, open(f'lm_img_{index}.jpg', 'wb') as outfile:
            copyfileobj(instream, outfile)
        img = Image.open(f'lm_img_{index}.jpg')
        img.save(f'lm_img_{index}.jpg')


    print('Creating medium high images...')
    os.chdir(os.path.abspath(os.path.join(os.path.abspath(__file__), '..', '..','selfies/high_medium')))
    for index, post in enumerate(medium_high_posts):
        req = Request(
            post['displayUrl'],
            data=None,
            headers={
                 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.3'
            }
        )
        with urlopen(req) as instream, open(f'hm_img_{index}.jpg', 'wb') as outfile:
            copyfileobj(instream, outfile)
        img = Image.open(f'hm_img_{index}.jpg')
        img.save(f'hm_img_{index}.jpg')

if __name__ == "__main__":
    process('items-ii-final.json')
