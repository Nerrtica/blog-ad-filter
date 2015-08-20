import json
import sys
import os

sys.path.insert(0, os.getcwd() + "/libsvm-3.20/python")
from auto_svm import *


print("** start to make model **")
f_data = open("./data/data.json", "r")
f_featureList = open("./data/featureList.json", "r")

data = json.loads(f_data.read())
featureList = json.loads(f_featureList.read())

modelMaker = make_model(data, featureList)
modelMaker.play()
print("** complete to make model **")