import json, operator, os
import urllib.request
from PIL import Image
import ssl

"""
This file will take the json data from the Instagram Scraper, use the 100 most liked images and 100 least like images,
and use them to fill the selfies the directory
"""

def process(PATH_TO_JSON_FILE):
    #to use an unverified ssl for url retrieving
    ssl._create_default_https_context = ssl._create_unverified_context
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
        #data.sort(key = lamda x:x['likesCount'])
        data.sort(key = operator.itemgetter('likesCount'))
        #getting top 100 images
        top_posts = data[:100]
        #getting bottom 100 images
        bottom_posts = data[-100:]
    os.chdir(os.path.abspath(os.path.join(os.path.abspath(__file__), '..', '..','selfies/good')))
    for index, post in enumerate(top_posts):
        urllib.request.urlretrieve(post['displayUrl'], f'good_img_{index}.jpg')
        img = Image.open(f'good_img_{index}.jpg')
        img.save(f'good_img_{index}.jpg')
    os.chdir(os.path.abspath(os.path.join(os.path.abspath(__file__), '..', '..','bad')))
    for index, post in enumerate(bottom_posts):
        urllib.request.urlretrieve(post['displayUrl'], f'bad_img_{index}.jpg')
        img = Image.open(f'bad_img_{index}.jpg')
        img.save(f'bad_img_{index}.jpg')
    return

if __name__ == "__main__":
    process('data.json')