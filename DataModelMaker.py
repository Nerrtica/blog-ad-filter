import json
import time
import os

sys.path.insert(0, os.getcwd() + "/libsvm-3.20/python")
from auto_svm import *




dateAndTime_current = time.strftime("%Y%m%d%H%M%S")
MODELPATH = "./model/" + dateAndTime_current
MODELRECORD = "./model/model_record.txt"
MODELFILE = "model.txt"
DATAPATH = "./data/" + dateAndTime_current
DATARECORD = "./data/data_record.txt"
DATAFILE = "data.json"




# make new directory of model
if not os.path.exists(MODELPATH):
	os.makedirs(MODELPATH)

# make new directory of data
if not os.path.exists(DATAPATH):
	os.makedirs(DATAPATH)

# append new record to model record file
f_MODELRECORD = open(MODELRECORD, "a+")
f_MODELRECORD.write(dateAndTime_current)
f_MODELRECORD.close()

# read recent data and append new record to data record file
f_DATARECORD = open(DATARECORD, "a+")
recent_DATARECORD = f_DATARECORD.read().splitlines()[-1]
f_DATARECORD.write(dateAndTime_current)
f_DATARECORD.close()

# get recent data
f_recent_DATA = open(DATAPATH + recent_DATARECORD + "/" + DATAFILE, "r")
recentData = json.loads(f_recent_DATA)

# read newData

# 작성중




# make model temp
# print("** start to make model **")
# f_data = open("./data/data.json", "r")
# f_featureList = open("./data/featureList.json", "r")

# data = json.loads(f_data.read())
# featureList = json.loads(f_featureList.read())

# modelMaker = make_model(data, featureList)
# modelMaker.play()
# print("** complete to make model **")