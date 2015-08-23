# insert crawler data to ./crawlingData/data.json



from DataCreater import DataCreater



dataCreater = DataCreater()



f_in = open("./crawlingData/data.json", "r")
dataCreater.loadData(f_in.read())
dataCreater.postAnalysis()
print("*****텍스트 분석 및 Feature 추가 완료*****")
print("# 텍스트 분석 소요시간 : {} sec".format(dataCreater.time_textAnalysis))
print("# Feature 추가 소요시간 : {} sec".format(dataCreater.time_addFeature))
# dataCreater.loadLabelData(path)
print("*****Label 추가 완료*****")
print("# Label 추가 소요시간 : {} sec".format(dataCreater.time_loadLabelData))
f_out = open("./data/data.json", "w")
f_out.write(dataCreater.createDataSet())
print("create json file")

f_in.close()
f_out.close()



f_featureList = open("./data/featureList.json", "w")
f_featureList.write(dataCreater.getFeatureList())
print("create list of feature file")



