
# coding: utf-8

# In[2]:




# In[3]:
import time
import json
import MeCab
import os

from sponTextFeatureMaker import sponTextFeatureMaker


# In[4]:

class DataCreater:
	def __init__(self):
		self.wordTag = ["NNG", "NNP", "VA", "VV", "VCP", "VCN"] # 사용할 품사
		self.postData = []
		# feature를 추출하기위한 임시 리스트
		self.feature_title_unigram = []
		self.feature_content_unigram = []
		self.feature_content_bigram = []
		self.feature_content_trigram = []
		
		# featureList
		self.featureList = ["text_len", "include_map", "img_cnt", "sponser", "f_title_unigram", "f_content_unigram", "f_content_bigram", "f_content_trigram", "sentence_cnt", "word_cnt", "wordInSentence_avg", "external_banner_cnt", "comment_cnt", "tag_cnt"]
		self.stpm = sponTextFeatureMaker()


	def loadData(self, data):
		self.postData.append(data)

	def postAnalysis(self):
		# self.postData = json.loads(post_jsonFormat)
		t = MeCab.Tagger ('-d /usr/local/lib/mecab/dic/mecab-ko-dic')
		try:
			# 시간측정 start
			self.time_textAnalysis = time.time()

			for index, post in enumerate(self.postData):
				title_text = str(post["title"])
				# title 텍스트
				textList = []
				unigramList = []
				result_MeCab = t.parse(str(title_text))
				separate_Line = result_MeCab.splitlines()
				for line in separate_Line:
					if line != "EOS" and line.replace(" ","").replace("\t", "") != "":
						currentText = line.split("\t")
						currentTag = currentText[1].split(",")
						text = {"text":currentText[0].strip(), "tag":currentTag[0]}
						textList.append(text)
				
				# title unigram
				for i in range(0, len(textList)):
					text = textList[i]
					if text["tag"] in self.wordTag: # unigram 추가
						if text["text"] not in self.feature_title_unigram:
							self.feature_title_unigram.append(text["text"])
						unigramList.append(text["text"])
				post["title_unigramList"] = unigramList
				
				
				
				# contents 텍스트(unigram, bigram, trigram)
				contents_text = str(post["contents"])
				result_MeCab = t.parse(str(contents_text))

				textList = []

				sentenceList = []
				sentence = []

				unigramList = [] # unigramList
				bigramList = [] # bi-gramList
				trigramList = [] # tri-gramList
				separate_Line = result_MeCab.splitlines()
				for line in separate_Line:
					if line != "EOS" and line.replace(" ","").replace("\t", "") != "":
						currentText = line.split("\t")
						currentTag = currentText[1].split(",")
						text = {"text":currentText[0].strip(), "tag":currentTag[0]}
						textList.append(text)

				# 형태소 단위로
				for i in range(0, len(textList)):
					text = textList[i]
					if text["tag"] in self.wordTag: # unigram 추가
						if text["text"] not in self.feature_content_unigram:
							self.feature_content_unigram.append(text["text"])
						unigramList.append(text["text"])
					
					# 문장 나누기    
					if text["tag"] not in ["EF", "SY"] and text["text"] != "" and i != len(textList)-1:
						sentence.append(text)
					# elif i == len(textList)-1:
					#     if len(sentence) != 0:
					#         sentenceList.append(sentence)
					#         sentence = []
					else:
						if len(sentence) != 0:
							sentenceList.append(sentence)
							sentence = []



				post["content_sentenceList"] = sentenceList
				post["content_unigramList"] = unigramList
				
				for s in range(0, len(sentenceList)):
					stc = sentenceList[s]
					for i in range(0, len(stc)):
						text = stc[i]
						if i >= 1: # bigram 추가
							pre_Text = stc[i-1]
							bi_element = str(pre_Text["text"] + text["text"])
							if bi_element not in self.feature_content_bigram:
								self.feature_content_bigram.append(bi_element)
							bigramList.append(bi_element)
			   
						if i >= 2: # trigram 추가
							pre_2_Text = stc[i-2]
							pre_Text = stc[i-1]
							tri_element = str(pre_2_Text["text"] + pre_Text["text"] + text["text"])
							if tri_element not in self.feature_content_trigram:
								self.feature_content_trigram.append(tri_element)
							trigramList.append(tri_element)
				post["content_bigramList"] = bigramList
				post["content_trigramList"] = trigramList
				# 시간측정
				self.time_textAnalysis = time.time() - self.time_textAnalysis
				print("({}/{})[1 step : 텍스트 분석 완료] {}_{}".format(index+1, len(self.postData), post["blogId"], post["logNo"]))
				
				# 시간측정
				self.time_addFeature = time.time()


				
			# feature 추가
			for index, post in enumerate(self.postData):
				# text길이
				post["text_len"] = "1:" + str(len(str(post["contents"])))
				
				# 지도 유무
				if "{mapId" in str(post["contents"]):
					post["include_map"] = "2:1"
				else:
					post["include_map"] = "2:0"
				
				# 이미지 갯수(임시)
				post["img_cnt"] = "3:" + str(post["img_cnt"])
				


				# 댓가성 포스팅 분류
				post["sponser"] = "4:0"

				if post["ad_agency_banner"] != "" or post["image_banner"] == True:
					post["sponser"] = "4:1"
				else:
					spontext_cnt = 0
					for stc in post["content_sentenceList"]:
						print(",".join([text["text"] for text in stc]))
						spontext_cnt = spontext_cnt + self.stpm.sponTextCount(stc)
						if spontext_cnt > 0:
							post["sponser"] = "4:1"
							break
						

				# 문장수
				post["sentence_cnt"] = "5:" + str(len(post["content_sentenceList"]))

				# 단어수
				post["word_cnt"] = "6:" + str(len(contents_text.split()))

				# 문장내 평균 단어수
				post["wordInSentence_avg"] = "7:" + str(len(contents_text.split())/len(post["content_sentenceList"]))

				# 외부 위젯 배너 수
				post["external_banner_cnt"] = "8:" + str(post["external_banner"])

				# 코멘트수
				post["comment_cnt"] = "9:" + str(len(post["comment"]))

				# 태그수
				post["tag_cnt"] = "10:" + str(len(post["tag"]))




				# title_unigram
				f_title_unigram = []
				for index_feature, feature in enumerate(self.feature_title_unigram):
					count = post["title_unigramList"].count(feature)
					if count != 0:
						f_title_unigram.append(str(index_feature + 1 + 10) + ":" + str(count))
				post["f_title_unigram"] = " ".join(f_title_unigram)
				
				# content_unigram
				f_content_unigram = []
				for index_feature, feature in enumerate(self.feature_content_unigram):
					count = post["content_unigramList"].count(feature)
					if count != 0:
						f_content_unigram.append(str(len(self.feature_title_unigram) + index_feature + 1 + 10) + ":" + str(count))
				post["f_content_unigram"] = " ".join(f_content_unigram)

				# content_bigram
				f_content_bigram = []
				for index_feature, feature in enumerate(self.feature_content_bigram):
					count = post["content_bigramList"].count(feature)
					if count != 0:
						f_content_bigram.append(str(len(self.feature_title_unigram) + len(self.feature_content_unigram) + index_feature + 1 + 10) + ":" + str(count))
				post["f_content_bigram"] = " ".join(f_content_bigram)

				# content_trigram
				f_content_trigram = []
				for index_feature, feature in enumerate(self.feature_content_trigram):
					count = post["content_trigramList"].count(feature)
					if count != 0:
						f_content_trigram.append(str(len(self.feature_title_unigram) + len(self.feature_content_unigram) + len(self.feature_content_bigram) + index_feature + 1 + 10) + ":" + str(count))
				post["f_content_trigram"] = " ".join(f_content_trigram)
				
				# unigramList, bigramList, trigramList 제거
				post.pop("title_unigramList", None)
				post.pop("content_unigramList", None)
				post.pop("content_bigramList", None)
				post.pop("content_trigramList", None)
				post.pop("content_sentenceList", None)


				# label = 0
				post["label"] = "0"

				# 시간측정
				self.time_addFeature = time.time() - self.time_addFeature

				print("({}/{})[2 step : feature 추가 완료] {}_{}".format(index+1, len(self.postData), post["blogId"], post["logNo"]))
		except RuntimeError as e:
			return str(e)



	def loadLabelData(self):
		self.time_loadLabelData = time.time()
		f = open("./crawlingData/label.csv", "r")
		loadLabel = f.read().splitlines()
		f.close()
		labelList = []
		for data in loadLabel:
			temp = data.split(",")
			toDict = {"url":temp[0], "label": temp[1]}
			labelList.append(toDict)

		for index, post in enumerate(self.postData):
			for i,labelData in enumerate(labelList):
				if post["blogId"] in labelData["url"] and post["logNo"] in labelData["url"]:
					post["label"] = labelData["label"]
					labelList.pop(i)
					print("({}/{})[3 step : label 추가완료] {}_{}".format(index+1, len(self.postData), post["blogId"], post["logNo"]))
					break



		# 시간측정
		self.time_loadLabelData = time.time() - self.time_loadLabelData
	
	def loadNgramData(self):
		f_feature_title_unigram = open("./data/feature_title_unigram.txt", "r")
		self.feature_title_unigram = f_feature_title_unigram.read().split()
		f_feature_title_unigram.close()

		f_feature_content_unigram = open("./data/feature_content_unigram.txt", "r")
		self.feature_content_unigram = f_feature_content_unigram.read().split()
		f_feature_content_unigram.close()

		f_feature_content_bigram = open("./data/feature_content_bigram.txt", "r")
		self.feature_content_bigram = f_feature_content_bigram.read().split()
		f_feature_content_bigram.close()

		f_feature_content_trigram = open("./data/feature_content_trigram.txt", "r")
		self.feature_content_trigram = f_feature_content_trigram.read().split()
		f_feature_content_trigram.close()


	def createDataSet(self):
		return str(json.dumps(self.postData, ensure_ascii=False, indent=4))


	def getFeatureList(self):
		return str(json.dumps(self.featureList, ensure_ascii=False, indent=4))



	def createFeatureNgram(self):
		f_feature_title_unigram = open("./result/feature_title_unigram.txt", "w")
		f_feature_title_unigram.write(" ".join(self.feature_title_unigram))
		f_feature_title_unigram.close()

		f_feature_content_unigram = open("./result/feature_content_unigram.txt", "w")
		f_feature_content_unigram.write(" ".join(self.feature_content_unigram))
		f_feature_content_unigram.close()

		f_feature_content_bigram = open("./result/feature_content_bigram.txt", "w")
		f_feature_content_bigram.write(" ".join(self.feature_content_bigram))
		f_feature_content_bigram.close()

		f_feature_content_trigram = open("./result/feature_content_trigram.txt", "w")
		f_feature_content_trigram.write(" ".join(self.feature_content_trigram))
		f_feature_content_trigram.close()




# # In[5]:

# dataCreater = DataCreater()


# # In[6]:

# f_in = open("./crawlingData/data2.json", "r")
# dataCreater.loadData(f_in.read())
# dataCreater.postAnalysis()
# print("*****텍스트 분석 및 Feature 추가 완료*****")
# print("# 텍스트 분석 소요시간 : {} sec".format(dataCreater.time_textAnalysis))
# print("# Feature 추가 소요시간 : {} sec".format(dataCreater.time_addFeature))
# dataCreater.loadLabelData()
# print("*****Label 추가 완료*****")
# print("# Label 추가 소요시간 : {} sec".format(dataCreater.time_loadLabelData))
# f_out = open("./result/data.json", "w")
# f_out.write(dataCreater.createDataSet())
# print("create json file")

# f_in.close()
# f_out.close()


# # In[7]:

# f_featureList = open("./result/featureList.json", "w")
# f_featureList.write(dataCreater.getFeatureList())
# print("create list of feature file")

