import json
import time
import os
import sys
from DataCreater import DataCreater
sys.path.insert(0, os.getcwd() + "/libsvm-3.20/python")
from auto_svm import *



def autoUpdate():
	dateAndTime_current = time.strftime("%Y%m%d%H%M%S")
	MODELPATH = "./model/" + dateAndTime_current
	MODELRECORD = "./model/model_record.txt"
	DATAPATH = "./data/" + dateAndTime_current
	DATARECORD = "./data/data_record.txt"
	DATAFILE_Before = "data_before.json"
	DATAFILE = "data.json"


	# read newData and file reset
	f_feedBack_DATA = open("./db/userFeedBack.json", "r")
	feedBackData = json.loads(f_feedBack_DATA.read())
	f_feedBack_DATA.close()

	if len(feedBackData) < 1:
		return "fail : there is no data"

	f_feedBack_DATA = open("./db/userFeedBack.json", "w")
	f_feedBack_DATA.write("[]")
	f_feedBack_DATA.close()



	# make new directory of model
	if not os.path.exists(MODELPATH):
		os.makedirs(MODELPATH)

	# make new directory of data
	if not os.path.exists(DATAPATH):
		os.makedirs(DATAPATH)

	# append new record to model record file
	f_MODELRECORD = open(MODELRECORD, "a+")
	f_MODELRECORD.write("\n" + dateAndTime_current)
	f_MODELRECORD.close()

	# read recent data and append new record to data record file
	f_DATARECORD = open(DATARECORD, "r")
	recent_DATARECORD = f_DATARECORD.read().splitlines()[-1]
	f_DATARECORD.close()
	f_DATARECORD = open(DATARECORD, "a+")
	f_DATARECORD.write("\n" + dateAndTime_current)
	f_DATARECORD.close()

	# get recent data
	f_recent_DATA = open("./data/" + recent_DATARECORD + "/" + DATAFILE, "r")
	recentData = json.loads(f_recent_DATA.read())
	f_recent_DATA.close()

	# merge
	f_new_DATA = open(DATAPATH + "/" + DATAFILE_Before, "w")
	newData = recentData + feedBackData
	json.dump(newData, f_new_DATA, ensure_ascii=False, indent=4)
	f_new_DATA.close()

	# dataCreater
	dataCreater = DataCreater()


	f_in = open(DATAPATH + "/" + DATAFILE_Before, "r")
	dataCreater.loadData(json.loads(f_in.read()))
	dataCreater.postAnalysis()
	print("*****텍스트 분석 및 Feature 추가 완료*****")
	print("# 텍스트 분석 소요시간 : {} sec".format(dataCreater.time_textAnalysis))
	print("# Feature 추가 소요시간 : {} sec".format(dataCreater.time_addFeature))
	# dataCreater.loadLabelData()
	# print("*****Label 추가 완료*****")
	# print("# Label 추가 소요시간 : {} sec".format(dataCreater.time_loadLabelData))
	f_out = open(DATAPATH + "/" + DATAFILE, "w")
	f_out.write(dataCreater.createDataSet())
	print("create json file")

	f_in.close()
	f_out.close()



	f_featureList = open(DATAPATH + "/featureList.json", "w")
	f_featureList.write(dataCreater.getFeatureList())
	print("create list of feature file")
	dataCreater.createFeatureNgram()
	print("create featureData file")
	# make model temp
	print("** start to make model **")
	f_data = open(DATAPATH + "/" + DATAFILE, "r")
	f_featureList = open(DATAPATH + "/featureList.json", "r")

	data = json.loads(f_data.read())
	featureList = json.loads(f_featureList.read())

	modelMaker = make_model(data, featureList, MODELPATH)
	modelMaker.play()
	print("** complete to make model **")


autoUpdate()