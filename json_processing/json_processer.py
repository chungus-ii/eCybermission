import json
import urllib.request
from PIL import Image

"""
This page will take the json data from the Instagram Scraper, and use the 100 most liked images and 100 least like images,
and use them to fill the selfies the directory
"""

def process(PATH_TO_JSON_FILE):
    #deleting any non-image type posts and overwriting the file
    with open(PATH_TO_JSON_FILE, 'r') as data_file:
        data = json.load(data_file)
    for element in data:
        if 'type' in element is not 'image':
            del element
    with open(PATH_TO_JSON_FILE, 'w') as data_file:
        data = json.dump(data, data_file)
    #sorting data by likes
    with open(PATH_TO_JSON_FILE) as data_file:
        data = json.load(data_file)
        data.sort(key = lamda x:x['likesCount'])
        #getting top 100 images
        top_posts = data[:100]
        #getting bottom 100 images
        bottom_posts = data[-100:]
    for index, post in enumerate(top_posts):
        urllib.request.urlretrieve(post['displayUrl'], f'img_{index}.jpg')
        img = Image.open(f'img_{index}.jpg')
        img.save(f'eCybermission/dataset/good/img_{index}.jpg')
    for index, post in enumerate(bottom_posts):
        urllib.request.urlretrieve(post['displayUrl'], f'img_{index}.jpg')
        img = Image.open(f'img_{index}.jpg')
        img.save(f'eCybermission/dataset/bad/img_{index}.jpg')
    return

if __name__ == "__main__":
    process('eCybermission/json_processing/data.json')