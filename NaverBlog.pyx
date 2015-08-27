# -*- coding:utf8 -*-

from bs4 import BeautifulSoup

import urllib
import time
import json
import sys
import os
import re

import AdFilter
import Crawler

reload(sys)
sys.setdefaultencoding('utf8')

class BlogPost(object):

    def __init__(self):

    # crawling from mobile page
        self.title = ''
        self.date = ''
        self.time = ''
        self.contents = ''
        self.tag = {}

        self.comment = []
    # crawling from pc page
        self.image = ''

    # crawling from url
        self.blogId = ''
        self.logNo = ''
    # url
        self.pc_url = ''
        self.m_url = ''
    # determine whether ad. or not from banner
        self.ad_agency_banner = ''
        self.image_banner = ''
        self.img_cnt = ''
        self.external_banner = ''

    def redirect_url(self, url):
        if url.startswith('http://'):
            protocol = url.split('//')[0] + '//'
            url = url.split('//')[-1]
        protocol = 'http://'
        if url.startswith('m.'):
            url = url[2:]

        # http://blog.naver.com/'blogId'?Redirect=Log&logNo='logNo'
        if '?' in url:
            self.logNo = url.split('=')[-1]
            self.blogId = url.split('?')[0].split('/')[-1]            
        else:
            url_element = url.split('/')
            # http://'blogId'.blog.me/'logNo'
            if len(url_element) == 2:
                self.blogId = url_element[0].split('.')[0]
                self.logNo = url_element[-1]
                
            # this url type's redirecting is more than others
                crawler = Crawler.Crawler()
                web_data = crawler.get_page(protocol+url)
                soup = BeautifulSoup(web_data, 'html.parser')
                url = soup('frameset')[0].find('frame')['src'].split('//')[-1]
                
            # http://blog.naver.com/'blogId'/'logNo'
            elif len(url_element) == 3:
                self.blogId = url_element[1]
                self.logNo = url_element[2]
            else:
                err_msg = ''' [supported url type] blog.naver.com/blogId/logNo
                                blodId.blog.me/logNo'''
                return err_msg
        # set mobile url type 
        m_url = protocol + 'm.blog.naver.com/'+self.blogId+'/'+self.logNo

        # set real pc url type
        crawler = Crawler.Crawler()
        web_data = crawler.get_page(protocol+url)
        soup = BeautifulSoup(web_data, 'html.parser')
        pc_url = protocol + 'blog.naver.com'+soup('frameset')[0].find('frame')['src']

        comment_url = 'http://blog.naver.com/CommentList.nhn?blogId=%s&logNo=%s'%(self.blogId, self.logNo)

        return pc_url, m_url, comment_url
        

    # requst to mobile page
    def get_m_post(self, url):
        self.m_url = url

        # get page 
        crawler = Crawler.Crawler()
        web_data = crawler.get_page(url)

        # search agency banner html tag
        self.ad_agency_banner = AdFilter.url_banner(web_data)

        soup = BeautifulSoup(web_data, 'html.parser')
        # title
        self.title = soup('h3', {'class':'tit_h3'})[0].text.strip()

        # date and time
        date_time = soup('em', {'class':'num'})[0].text
        self.date = date_time.split(' ')[0]
        self.time = date_time.split(' ')[1]

        # contents
        self.contents = soup('div', {'class':'post_ct'})[0].text.strip()

        # tag
        if len(soup('div', {'class':'post_tag'})) > 0:
            tag = [ (e.text, e.find('a')['href']) for e in soup('div', {'class':'post_tag'})[0]('li')]
            for e in tag:
                self.tag[e[0].encode('utf8')] = e[1].encode('utf8')
            del tag

        
    def get_pc_post(self, url):
        self.pc_url = url

        # get page
        crawler = Crawler.Crawler()
        web_data = crawler.get_page(url)
        soup = BeautifulSoup(web_data, 'html.parser')

        # invalid time is entered before
        if ':' not in self.time:
            dateTime = soup('p', {'class':'date'})[0].text.split()
            self.date = dateTime[0]
            self.time = dateTime[1]

        # search External widget
        widget = soup('span', {'id':'widget'})

        self.external_banner = 0
        for w in widget:
            iframe = w.findAll('iframe')
            if iframe :
                self.external_banner += 1
       
        # get image url
        contents = soup('div', {'id':'post-view'+self.logNo})[0]
        contents_image = [e['src'].encode('utf8') for e in contents.findAll('img')]

        self.img_cnt = len(contents_image)

        for image in contents_image:
            img = crawler.get_image(image)
            self.image_banner = AdFilter.image_banner_compare(img)

    # post comment crawling
    def get_comment(self, url):
        # get web data
        crawler = Crawler.Crawler()
        web_data = crawler.get_page(url)
        soup = BeautifulSoup(web_data, 'html.parser')

        # get comment list
        comment_list = soup('li', {'class':'_countableComment'})
        for comment in comment_list:
            d = {
                'nick':'',
                'date':'',
                'time':'',
                'comment':''
            }
            # private comment 
            if len(comment.findAll('dt')) < 2:
                continue
            # comment parsing
            data = comment.findAll('dt')[1].text
            data = data.split('\n')
            
            d['nick'] =data[1]
            dateTime = data[2].split()
            d['date'] = dateTime[0]
            d['time'] = dateTime[1]
            d['comment'] = comment.find('dd').text.strip()

            self.comment.append(d)
            
    def write_data_as_dict(self):
        d = {
            'title':self.title,
            'date':self.date,
            'time':self.time,
            'contents':self.contents,
            'tag':self.tag,
            'comment':self.comment,
            'image':self.image,
            'blogId':self.blogId,
            'logNo':self.logNo,
            'pc_url':self.pc_url,
            'm_url':self.m_url,
            'ad_agency_banner':self.ad_agency_banner,
            'image_banner':self.image_banner,
            'img_cnt':self.img_cnt,
            'external_banner':self.external_banner,
        }
        return d

def post_url_list(query, date):
    list_search_url = 'http://cafeblog.search.naver.com/search.naver?'
    parameter = {
            'where':'post',
            'sm':'tab_pge',
            'query':query,
            'st':'date',
            'date_option':'6',      # 0, 1, 2, 3, 4, 5, 6
            'date_from':date,
            'date_to':date,
            'dup_remove':'1',
            'post_blogurl':'blog.naver.com',
            'post_blogurl_without':'',
            'srchby':'all',
            'nso':'so%3Add%2Cp%3Afrom20150710to20150710',
            'ie':'utf8',
            'start':'1'
    }
    
    url = list_search_url + urllib.urlencode(parameter)
    print url
    crawler = Crawler.Crawler()
    web_data = crawler.get_page(url)
    
    soup = BeautifulSoup(web_data, 'html.parser')
    max_page = soup('span', {'class':'title_num'})[0].text.split('/')[1]
    
    max_page = int(re.sub(u'[^0-9]', u'',max_page))
    max_page = max_page/10*10 + 1

    if max_page > 1000:
        max_page = 1000

    post_list = []
    for start in xrange(1, max_page+1, 10):
        parameter['start'] = str(start)
        url = list_search_url + urllib.urlencode(parameter)
        web_data = crawler.get_page(url)

        soup = BeautifulSoup(web_data, 'html.parser')
        post_list += list(soup('li', {'class':'sh_blog_top'}))

    url_list = []
    for post in post_list:
        url_list.append(post.find('a')['href'])

    return url_list

def post_crawling(url):
    
    blog = BlogPost()

    pc_url, m_url, comment_url = blog.redirect_url(url)

    blog.get_m_post(m_url)
    blog.get_comment(comment_url)
    blog.get_pc_post(pc_url)
    
    return blog


if __name__ == '__main__':
    total = time.time()

    url_list = post_url_list('맛집', '20150826')
    

    data = []

    for url in url_list:
        try :
            post = post_crawling(url)
            data.append(post.write_data_as_dict())
        except IndexError:
            with open('error.txt', 'a') as f:
                f.write('[error] ' + url)
        except IOError:
            with open('error.txt', 'a') as f:
                f.write('[error] ' + url)
    with open('./crawlingData/data.json', 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=True)

    print 'total ', time.time()-total
