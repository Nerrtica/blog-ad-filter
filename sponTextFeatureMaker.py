
# coding: utf-8

# ## 스폰텍스트 분석

# In[1]:

import copy

# In[2]:

class sponTextFeatureMaker:
    def __init__(self):


        # text Data
        text_object = [{"tag":"NNG", "text":"제품"}, 
                {"tag":"NNG", "text":"메뉴"}, 
                {"tag":"NNG", "text":"상품"}, 
                {"tag":"NNG", "text":"서비스"},
                {"tag":"NNG", "text":"상품권"},
                {"tag":"NNG", "text":"음식"},
                {"tag":"NNG", "text":"지원금"},
                {"tag":"NNG", "text":"혜택"},
                {"tag":"NNG", "text":"대가"},
                {"tag":"NNG", "text":"원고료"}
               ]
        text_ticket = [[{"tag":"NNG", "text":"이용"}, {"tag":"XSN", "text":"권"}], 
                       [{"tag":"NNG", "text":"식사"}, {"tag":"XSN", "text":"권"}],
                       [{"tag":"NNG", "text":"시식"}, {"tag":"XSN", "text":"권"}],
                       [{"tag":"NNG", "text":"체험"}, {"tag":"XSN", "text":"권"}]
                      ]
        text_adverb= [{"tag":"NNG", "text":"무료"},
                    {"tag":"NNG", "text":"무상"}
                    ]
        text_verb_get = [{"tag":"NNG", "text":"제공"},
                       {"tag":"NNG", "text":"지원"},
                       {"tag":"NNG", "text":"지급"}
                       ]
        text_verb_do = [{"tag":"NNG", "text":"체험"},
                   {"tag":"NNG", "text":"이용"},
                   {"tag":"NNG", "text":"시식"}
                  ]
        text_write = [{"tag":"NNG", "text":"작성"},
                   {"tag":"NNP", "text":"포스팅"}
                  ]
        text_receive = [{"tag":"VV", "text":"받"}, 
                        {"tag":"VV", "text":"얻"}
                       ]
        text_not = [{"tag":"VX", "text":"않"}, {"tag":"MAG", "text":"못"}]
        
        text_visit = ["방문"]

        self.text_except = [{"tag":"NNG", "text":"후"}]


#         pattern setting
        self.pattern = []
        self.pattern_except = []


        for obj in [text["text"] for text in text_object]:
            for adv in [text["text"] for text in text_adverb]:
                for v_get in [text["text"] for text in text_verb_get]:
                    if [obj, adv, v_get] not in self.pattern:
                        self.pattern.append([obj, adv, v_get])


        for tic in text_ticket:
            ticket = tic[0]["text"] + tic[1]["text"]
            for adv in [text["text"] for text in text_adverb]:
                for v_get in [text["text"] for text in text_verb_get]:
                    if [ticket, adv, v_get] not in self.pattern:
                        self.pattern.append([obj, adv, v_get])


        for adv in [text["text"] for text in text_adverb]:
            for obj in [text["text"] for text in text_object]:
                for v_get in [text["text"] for text in text_verb_get]:
                    if [adv, obj, v_get] not in self.pattern:
                        self.pattern.append([adv, obj, v_get])

        for obj in [text["text"] for text in text_object]:
            for adv in [text["text"] for text in text_adverb]:
                for v_do in [text["text"] for text in text_verb_do]:
                    if [obj, adv, v_do] not in self.pattern:
                        self.pattern.append([obj, adv, v_do])

        for adv in [text["text"] for text in text_adverb]:
            for obj in [text["text"] for text in text_object]:
                for v_do in [text["text"] for text in text_verb_do]:
                    if [adv, obj, v_do] not in self.pattern:
                        self.pattern.append([adv, obj, v_do])

        for tic in text_ticket:
            ticket = tic[0]["text"] + tic[1]["text"]
            for adv in [text["text"] for text in text_adverb]:
                for v_get in [text["text"] for text in text_verb_get]:
                    if [ticket, adv, v_get] not in self.pattern:
                        self.pattern.append([ticket, adv, v_get])

        for adv in [text["text"] for text in text_adverb]:
            for tic in text_ticket:
                ticket = tic[0]["text"] + tic[1]["text"]
                for v_get in [text["text"] for text in text_verb_get]:
                    if [adv, ticket, v_get] not in self.pattern:
                        self.pattern.append([adv, ticket, v_get])

        for obj in [text["text"] for text in text_object]:
            for v_get in [text["text"] for text in text_verb_get]:
                for v_do in [text["text"] for text in text_verb_do]:
                    if [obj, v_get, v_do] not in self.pattern:
                        self.pattern.append([obj, v_get, v_do])
                    if [obj, v_get, "않", v_do] not in self.pattern_except:
                        self.pattern_except.append([obj, v_get, "않", v_do])
                    if [obj, v_get, "아니", v_do] not in self.pattern_except:
                        self.pattern_except.append([obj, v_get, "아니", v_do])

        for tic in text_ticket:
            ticket = tic[0]["text"] + tic[1]["text"]
            for v_get in [text["text"] for text in text_verb_get]:
                for v_do in [text["text"] for text in text_verb_do]:
                    if [ticket, v_get, v_do] not in self.pattern:
                        self.pattern.append([ticket, v_get, v_do])

        for v_get in [text["text"] for text in text_verb_get]:
            for v_write in [text["text"] for text in text_write]:
                if [v_get, v_write] not in self.pattern:
                    self.pattern.append([v_get, v_write])
                if [v_get, "않", v_write] not in self.pattern_except:
                    self.pattern_except.append([v_get, "않", v_write])
                if [v_get, "아니", v_write] not in self.pattern_except:
                    self.pattern_except.append([v_get, "아니", v_write])

        for visit in text_visit:
            for v_get in [text["text"] for text in text_verb_get]:
                for v_write in [text["text"] for text in text_write]:
                    if [visit, v_get, v_write] not in self.pattern:
                        self.pattern.append([visit, v_get, v_write])


        for v_get in [text["text"] for text in text_verb_get]:
            for visit in text_visit:
                for v_write in [text["text"] for text in text_write]:
                    if [v_get, visit, v_write] not in self.pattern:
                        self.pattern.append([v_get, visit, v_write])
                    if [v_get, "않", visit, v_write] not in self.pattern_except:
                        self.pattern_except.append([v_get, "않", visit, v_write])
                    if [v_get, "아니", visit, v_write] not in self.pattern:
                        self.pattern_except.append([v_get, "아니", visit, v_write])
    
        for pat in self.pattern:
            new_pat = copy.deepcopy(pat)
            new_pat.append("않")
            self.pattern_except.append(new_pat)
            new_pat = copy.deepcopy(pat)
            new_pat.append("아닙니다")
            self.pattern_except.append(new_pat)
            new_pat = copy.deepcopy(pat)
            new_pat.append("아니")
            self.pattern_except.append(new_pat)
        
            
    def sponTextCount(self, target):
        target_extract = [] 
        for t in target:
            if t["tag"] in ["NNG", "NNP", "XSN", "VX", "VCN+EC", "VCN"]:
                if t not in self.text_except:
                    target_extract.append(t["text"])
        
        count = 0
        
        temp = "".join(target_extract)
        for pat in self.pattern:
            pattern_str = "".join(pat)
            count = count + temp.count(pattern_str)
            if temp.count(pattern_str) > 0:
                print("string : " + temp + "\npattern : " + pattern_str)
                
        for pat in self.pattern_except:
            pattern_str = "".join(pat)
            count = count - temp.count(pattern_str)
            if temp.count(pattern_str) > 0:
                print("string : " + temp + "\nexcept pattern : " + pattern_str)
        
        
        return count


# In[27]:

# stpm = sponTextFeatureMaker()


# In[28]:

# test = []
# for text in resultTextSet[0]:
#     if text["tag"] in ["NNG", "XSN", "VX", "MAG"]:
#         test.append(text["text"])

# print(stpm.sponTextCount(test))


# In[29]:

# stpm.pattern


# In[ ]:



