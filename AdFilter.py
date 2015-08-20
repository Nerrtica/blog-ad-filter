from PIL import Image

import json

import sys
import os


reload(sys)
sys.setdefaultencoding('utf8')

# determine post with html document
def url_banner(webData):

    with open('./banner_data/ad_agency.json') as f:
        s = f.read()
        adKeyword = json.loads(s)

        for key in adKeyword:
            adKeyword[key] = [e.encode('utf8') for e in adKeyword[key]]

    
    for key in adKeyword:
        for keyword in adKeyword[key]:
            if keyword in webData:
                return key

    return ''

def image_banner_info():
    img_list = os.listdir('./image')

    with open('./banner_data/ad_agency.json') as f:
        img_info = json.load(f, encoding='utf8')
    
    for img_name in img_list:
        img = Image.open('./image/' + img_name)
        l.append({
            'imgName':img_name,
            'histogram':img.histogram(),
            'size':img.size
        })

    with open('img_info.json', 'w') as f:
        json.dump(l, f, ensure_ascii=False, indent=True)

def image_banner_compare(im):
    hist = im.histogram()
    size = im.size

    # withblog
    if size == (320, 24):
        return True
    
    factor = size[0]*size[1]
        
    with open('./banner_data/img_info.json') as f:
        img_info = json.load(f, encoding='utf8')

    for img_data in img_info:
        if size == img_data['size']:
            for i in xrange(256):
                factor += abs(hist[i]-img_data['histogram'][i])
    
    if (float(size[0]*size[1]-factor)/(size[0]*size[1]))*100 > 80:
        return False
    else :
        return True
