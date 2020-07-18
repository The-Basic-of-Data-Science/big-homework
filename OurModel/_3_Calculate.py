# -*- coding: utf-8 -*-

'''
综合能力评估
'''
        

import json
import csv
import numpy as np

MIN_DIFFICULTY = 0.1 #最小难度
MAX_DIFFICULTY = 0.8 #最大难度，也就是分数部分占比
STYLE_RATE = 1 - MAX_DIFFICULTY #风格分占比

class Calculator:

    raw_data = None #原始数据
    difficulty = {} #题目难度 [MIN_DIFFICULTY, MAX_DIFFICULTY]
    final_score = {} #每人每题的最终得分，键名为 "uid,cid"
    code_style_score = {} #每人每题的编码风格分，键名为 "uid,cid"
    valid_rate = {} #每人每题的有效提交率，键名为 "uid,cid"


    def __init__(self):
        with open("../JSON/test_data.json", 'r', encoding='utf-8') as f:
            self.raw_data = json.load(f) #获取原始数据
        self.get_difficulty(MIN_DIFFICULTY, MAX_DIFFICULTY) #获取题目难度
        self.get_final_score() #获取每人每题最终得分
        self.get_code_style_score() #获取每人每题的编码风格分
        self.get_valid_rate() #获取每人每题的有效提交率


    def get_difficulty(self, x2, y2):
        scores = {} #分数数据
        raw_difficulty = {} #生难度

        cr = csv.reader(open("../OurModelOutPut/Cases/score_statistics.csv"), delimiter=",")
        next(cr)
        for row in cr:
            #row: 题目编号,平均数,中位数,众数,尝试人数,通过人数,平均提交次数,测试用例数
            scores[row[0]] = row[1:]
        
        for case in scores:
            avg = float(scores[case][0]) #平均数换算难度
            med = float(scores[case][1]) #中位数换算难度
            cmn = np.average(list(map(float, scores[case][2].split('|')))) #众数换算难度
            rte = int(scores[case][4]) / int(scores[case][3]) #（通过人数：尝试人数）换算难度
            tim = int(scores[case][6]) / float(scores[case][5]) #（用例总数：平均提交次数）换算难度
            raw_difficulty[case] = avg + med + cmn + rte + tim
        #TODO 聚类，人工标注
        x1 = min(raw_difficulty.values()) #最小生难度
        y1 = max(raw_difficulty.values()) #最大生难度

        k = (y2 - x2) / (y1 - x1)
        b = (x2 * y1 - x1 * y2) / (y1 - x1)

        for case in raw_difficulty:
            self.difficulty[case] = raw_difficulty[case] * k + b


    def get_final_score(self):
        cr = csv.reader(open("../OurModelOutPut/Cases/cases_detail.csv", encoding = 'gb2312'), delimiter=",")
        next(cr)
        for row in cr:
            self.final_score[",".join(row[0:2])] = float(row[3])

    
    def get_code_style_score(self):
        #TODO 取绝大部分人的风格分为区间，映射到 [0, 100] 
        cr = csv.reader(open("../OurModelOutPut/Users/user_result_0_36421.csv"), delimiter=",")
        for row in cr:
            self.code_style_score[",".join(row[0:2])] = float(row[3])


    def get_valid_rate(self):
        cr = csv.reader(open("../OurModelOutPut/Valid/valid.csv"), delimiter=",")
        next(cr)
        for row in cr:
            self.valid_rate[",".join(row[0:2])] = float(row[4])


    def code_score(self, uid, cid):
        '''
        做题分
        :param uid
        :param cid
        :return:做题分
        '''
        key = ",".join([uid, cid])
        # TODO 得到weight
        weight = 1
        if key in self.final_score:
            print("最终得分=" + str(self.final_score[key]) + " 权重=" + str(weight))
            return self.final_score[key] * weight
        else:
            print(key + "的最终成绩缺失")
            return 0


    def style_score(self, uid, cid):
        '''
        编码风格分
        :param uid:用户的id
        :param cid:对应的题目的id
        :return:编码风格分
        '''
        key = ",".join([uid, cid])
        if key in self.code_style_score:
            ss = STYLE_RATE * self.code_style_score[",".join([uid, cid])]
            print("编码风格分=" + str(ss))
        else:
            ss = 0
            print(key + "的编码风格分缺失")
        return ss


    def case_score(self, uid, cid):
        '''
        题目分=（做题分*题目难度+编码风格分）*（有效提交比例）
        :return:一道题目的最终标准得分
        '''
        scr = self.code_score(uid, cid) * self.difficulty[cid] + self.style_score(uid, cid)
        rte = self.valid_rate[",".join([uid, cid])]
        print("（做题分*题目难度+编码风格分）=" + str(scr) + " （有效提交比例）" + str(rte))
        return scr * rte


    def user_score(self, uid):
        '''
        用户总评分=所有做过的题目的题目分总和
        数据来源:其他方法
        :param uid 用户的id
        :return: 用户总评分
        '''
        if not uid in self.raw_data:
            print("没有这个人")
            return
        score = 0
        for case in self.raw_data[uid]["cases"]: #遍历此人交过的每道题目
            print(",".join([uid, case["case_id"]]))
            t = self.case_score(uid, case["case_id"])
            print("题目分为" + str(t))
            score += t #加上这题的做题分
            print()
        return score, score / len(self.raw_data[uid]["cases"])

if __name__ == '__main__':
    calculator = Calculator()
    print(calculator.user_score('60699'))
