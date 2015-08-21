# -*- encoding:utf8 -*-

# all the imports
from flask import Flask, request, session, g, redirect
from flask import url_for, abort, render_template, flash

import json
import sys
import os

import NaverBlog

from DataCreater import DataCreater

sys.path.insert(0, os.getcwd() + "/libsvm-3.20/python")
from auto_svm import *

reload(sys)
sys.setdefaultencoding('utf8')
# configuration
DATABASE = '/db/user_opinion.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'admin'

# create flask application 
app = Flask(__name__)
app.config.from_object(__name__)

# View function
@app.route('/')
def blog_search():
	return render_template('blog_search.html')

@app.route('/crawling', methods=['GET', 'POST'])
def crawling():
	error = None
	if request.method == 'POST':
		url = request.form['url']
	if url == '':
		return 'please input url'
	if url.startswith('http://') is False:
		url = 'http://' + url
		
	crawler = NaverBlog.post_crawling(url)
		
	data = crawler.write_data_as_dict()
	dataCreater = DataCreater()
	dataCreater.loadData(data)
	dataCreater.loadNgramData()
	dataCreater.postAnalysis()
	# return dataCreater.createDataSet()
	predictor = predict_label(json.loads(dataCreater.createDataSet()), 
		json.loads(dataCreater.getFeatureList()))
	score = str(predictor.play()[0])
	return render_template('filter_result.html', url=url, adscore=score)
	# return data/Creater.createDataSet()\

if __name__ == '__main__':
	app.run()
