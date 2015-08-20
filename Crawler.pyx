from StringIO import StringIO
from PIL import Image

import requests

import datetime
import time
import sys
import os



reload(sys)
sys.setdefaultencoding('utf8')

class Crawler(object):
    def __init__(self):
        pass

    def get_page(self, url):
        return requests.get(url).text

    def get_image(self, url):
        return Image.open(StringIO(requests.get(url).content))
        
