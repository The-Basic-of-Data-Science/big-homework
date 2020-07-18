# -*- coding: utf-8 -*-

'''
综合能力评估
'''
        

import json
import csv
import numpy as np
from matplotlib import pyplot as plt
from sklearn import cluster



MIN_DIFFICULTY = 0.1 #最小难度
MAX_DIFFICULTY = 0.8 #最大难度，也就是分数部分占比
STYLE_RATE = 1 - MAX_DIFFICULTY #风格分占比
RAW_DIFFICULTY_CENTERS = [
    [89.31476036273146, 99.95670995670996, 99.99999999999999, 0.9887123025710105, 3.8244682935767487],
    [77.08557872195003, 99.42182170542635, 99.89662790697673, 0.9784128098927094, 3.272016744783012],
    [63.93237323484452, 99.30656934306569, 99.99999999999999, 0.9840112671523445, 2.648851686595397],
    [62.38312388242798, 75.79144444444445, 99.42588888888889, 0.9526370988656747, 2.155258789004564],
    [54.40148769029594, 50.440916666666666, 100.0, 0.9395351423012342, 2.047442274587258],
    [51.79772540650981, 50.629333333333335, 52.444333333333326, 0.8997904525730938, 1.749359650333929],
    [45.28810501196811, 46.45368421052632, 0.43855263157897184, 0.903700362948732, 1.5345727988329327],
    [35.63325519664818, 7.505283018867928, 0.37735849056606696, 0.933955219472865, 1.6191765029745437]
] #代码生难度的八分类的中心
#根据绝大多数原始编码风格分的分布得到范围 [-25, 10]
MIN_CODE_STYLE_SCORE = -25
MAX_CODE_STYLE_SCORE = 10

class Calculator:

    raw_data = None #原始数据
    difficulty = {} #题目难度 [MIN_DIFFICULTY, MAX_DIFFICULTY]
    final_score = {} #每人每题的最终得分，键名为 "uid,cid"
    code_style_score = {} #每人每题的编码风格分，键名为 "uid,cid"
    valid_rate = {} #每人每题的有效提交率，键名为 "uid,cid"


    def __init__(self):
        with open("../JSON/test_data.json", 'r', encoding='utf-8') as f:
            self.raw_data = json.load(f) #获取原始数据
        self.get_difficulty() #获取题目难度
        self.get_final_score() #获取每人每题最终得分
        self.get_code_style_score() #获取每人每题的编码风格分
        self.get_valid_rate() #获取每人每题的有效提交率


    def pre_get_raw_difficulty_centers(self): #预先求出生难度的分类中心
        scores = self.__get_raw_scores() #分数数据
        raw_difficulty = [] #生难度
        for case in scores:
            raw_difficulty.append(self.__get_raw_difficulty_from_score(scores[case]))
        data = raw_difficulty
        clf = cluster.KMeans(init='k-means++', n_clusters=8, random_state=794780360) #八分类
        clf.fit(data) #跑聚类
        print([list(center) for center in clf.cluster_centers_]) #输出八个中心点


    def pre_get_code_style_score_dist(self): #预先求出原始编码风格分的分布
        distr = []
        for i in range(-1710, 15, 5):
            distr.append(0)
        cr = csv.reader(open("../OurModelOutPut/Users/user_result_0_36421.csv"), delimiter=",")
        for row in cr:
            distr[int((float(row[3]) + 1710) // 5)] += 1
        print(distr)
        print(distr.index(212) * 5 - 1710)
        print(distr.index(6114) * 5 - 1710)
        plt.bar(range(len(distr)), distr, color='#6a005f')
        plt.ylim(min(distr), max(distr))
        plt.title('Coding Style Score Distribution')
        plt.ylabel('number')
        plt.xlabel('score ( = x * 5 - 1710 )')
        plt.show()


    def __get_raw_scores(self): #读取分数数据到字典
        scores = {} #分数数据
        cr = csv.reader(open("../OurModelOutPut/Cases/score_statistics.csv"), delimiter=",")
        next(cr)
        for row in cr:
            #row: 题目编号,平均数,中位数,众数,尝试人数,通过人数,平均提交次数,测试用例数
            scores[row[0]] = row[1:]
        return scores
    

    def __get_raw_difficulty_from_score(self, score): #根据分数数据求生难度
        avg = float(score[0]) #平均数换算难度
        med = float(score[1]) #中位数换算难度
        cmn = np.average(list(map(float, score[2].split('|')))) #众数换算难度
        rte = int(score[4]) / int(score[3]) #（通过人数：尝试人数）换算难度
        tim = int(score[6]) / float(score[5]) #（用例总数：平均提交次数）换算难度
        return [avg, med, cmn, rte, tim]
        

    def get_difficulty(self):
        def distance(a, b): #计算欧氏距离
            return np.sqrt(np.sum([((a[i] - b[i]) ** 2) for i in range(len(a))]))
        scores = self.__get_raw_scores() #分数数据
        # cnt = [0 for i in range(8)]
        for case in scores:
            raw_difficulty = self.__get_raw_difficulty_from_score(scores[case])
            index = np.argmin([distance(raw_difficulty, center) for center in RAW_DIFFICULTY_CENTERS]) #计算离该题生难度最接近的中心点的下标
            # cnt[index] += 1
            self.difficulty[case] = index / (len(RAW_DIFFICULTY_CENTERS) - 1) * (MAX_DIFFICULTY - MIN_DIFFICULTY) + MIN_DIFFICULTY #下标换算难度
        # print(self.difficulty)
        # print(cnt)


    def get_final_score(self):
        cr = csv.reader(open("../OurModelOutPut/Cases/cases_detail.csv", encoding = 'gb2312'), delimiter=",")
        next(cr)
        for row in cr:
            self.final_score[",".join(row[0:2])] = float(row[3])

    
    def get_code_style_score(self):
        cr = csv.reader(open("../OurModelOutPut/Users/user_result_0_36421.csv"), delimiter=",")
        for row in cr:
            score = float(row[3])
            if score < MIN_CODE_STYLE_SCORE: score = MIN_CODE_STYLE_SCORE
            if score > MAX_CODE_STYLE_SCORE: score = MAX_CODE_STYLE_SCORE #规整原始分数
            self.code_style_score[",".join(row[0:2])] = (score - MIN_CODE_STYLE_SCORE) / (MAX_CODE_STYLE_SCORE - MIN_CODE_STYLE_SCORE) * 100 #线性映射到 [0, 100]


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
    # calculator.pre_get_raw_difficulty_centers()
    print(calculator.user_score('60699'))
