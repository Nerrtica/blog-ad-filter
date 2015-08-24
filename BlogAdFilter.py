# -*- encoding:utf8 -*-

# all the imports
from flask import Flask, request, session, g, redirect, jsonify
from flask import url_for, abort, render_template, flash

from sqlite3 import dbapi2 as sqlite3
from hashlib import md5

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

# # View function
# @app.route('/')
# def blog_search():
# 	return render_template('blog_search.html')

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
	data = json.loads(dataCreater.createDataSet())
	if data[0]["label"] == "5":
		score = "5"
	else:
		predictor = predict_label(data, json.loads(dataCreater.getFeatureList()))
		score = str(predictor.play()[0])
	return render_template('filter_result.html', url=url, adscore=score)
	# return data/Creater.createDataSet()\

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
	error = None
	if request.method == 'POST':
		user_score = str(request.form['user_score'])
	if user_score in ["1", "2", "3", "4", "5"]:
		return '잘못된 데이터 입력'
	


	return render_template('feedback_ok.html', score=score)
	# return data/Creater.createDataSet()


# Ajax Ver

@app.route('/_extractData')
def extractData():
	url = request.args.get('url', 0, type=str)
	if url.startswith('http://') is False:
		url = 'http://' + url
	crawler = NaverBlog.post_crawling(url)
		
	data = crawler.write_data_as_dict()
	dataCreater = DataCreater()
	dataCreater.loadData(data)
	dataCreater.loadNgramData()
	dataCreater.postAnalysis()
	# return dataCreater.createDataSet()
	data = json.loads(dataCreater.createDataSet())
	data_0_jsonFormat = str(json.dumps(data[0], ensure_ascii=False, indent=4))
	return data_0_jsonFormat

@app.route('/_predict')
def predict():
	featureList = ["text_len", "include_map", "img_cnt", "sponser", "f_title_unigram", "f_content_unigram", "f_content_bigram", "f_content_trigram", "sentence_cnt", "word_cnt", "wordInSentence_avg", "external_banner_cnt", "comment_cnt", "tag_cnt"]
	data = request.args.get('data', 0, type=str)
	data = json.loads(data)
	data_list = []
	data_list.append(data)
	if data_list[0]["label"] == "5":
		score = "5"
	else:
		predictor = predict_label(data_list, featureList)
		score = str(predictor.play()[0])
	return score


@app.route('/_addToDB')
def addToDB():
	data = request.args.get('data', 0, type=str)
	user_score = str(request.args.get('user_score', 0, type=str))
	print("**********\n\n\n\n" + type(user_score).__name__ + "**********\n\n" + user_score + "\n\n")
	if user_score not in ["1", "2", "3", "4", "5"]:
		return "fail : invalid data"

	f = open("./db/userFeedBack.json", "r")
	
	originData = json.loads(f.read())
	newData_json = json.loads(data)
	newData_json["label"] = user_score
	newData_json["labelList"].append(newData_json["label"])
	f.close()
	overlabCheck = False
	for ori in originData:
		if ori["blogId"] == newData_json["blogId"] and ori["logNo"] == newData_json["logNo"]:
			ori["labelList"].append(newData_json["label"])
			if len(ori["labelList"]) > 1:
				ori["label"] = str(sum([int(x) for x in ori["labelList"]])/float(len(ori["labelList"])))
			overlabCheck = True
			break

	f = open("./db/userFeedBack.json", "w+")
	if overlabCheck == False:
		originData.append(newData_json)

	json.dump(originData, f, ensure_ascii=False, indent=4)
	f.close()
	return "success"


@app.route('/')
def index():
	return render_template('index.html')


if __name__ == '__main__':
	app.run()
