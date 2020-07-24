# -*- coding: utf-8 -*-

'''
综合能力评估
'''

import json
import csv
import numpy as np
from matplotlib import pyplot as plt
import os

# 最低难度
MIN_DIFFICULTY = 0.1
# 最高难度
MAX_DIFFICULTY = 0.8
# 风格分数占比
STYLE_RATE = 1 - MAX_DIFFICULTY
# 根据绝大多数原始编码风格分的分布得到范围 [-25, 10]
MIN_CODE_STYLE_SCORE = -25
MAX_CODE_STYLE_SCORE = 10

class Calculator:
    TEST_DATA = ''
    USER_RESULT = ''
    SCORE_STATISTICS = ''
    CASES_DETAIL = ''
    VALID = ''
    RESULT = ''

    # 原始数据
    raw_data = None
    # 题目难度 [MIN_DIFFICULTY, MAX_DIFFICULTY]
    difficulty = {}
    # 每人每题的最终得分，键名为 "uid,cid"
    final_score = {}
    # 每人每题的编码风格分，键名为 "uid,cid"
    code_style_score = {}
    # 每人每题的有效提交率，键名为 "uid,cid"
    valid_rate = {}
    # 每人每题的最终得分的权重，键名为 "uid,cid"
    test_score = {}
    # 题目的类型，键名为 "cid"
    case_type = {}


    def __init__(self, TEST_DATA, USER_RESULT, SCORE_STATISTICS,
                 CASES_DETAIL, VALID, TEST_SCORE, RESULT, CENTER):
        '''
        类构造方法
        :param TEST_DATA: JSON格式的原始数据
        :param USER_RESULT: 用户的编码风格分数
        :param SCORE_STATISTICS: 用户的题目分数统计情况
        :param CASES_DETAIL: 每人每题提交情况
        :param VALID: 每位每题有效提交信息
        :param TEST_SCORE: 用户的题目分数权重信息
        :param RESULT: 用户最后评分输出位置
        :param CENTER: 将八分类中心读入
        '''
        self.TEST_DATA = TEST_DATA
        self.USER_RESULT = USER_RESULT
        self.SCORE_STATISTICS = SCORE_STATISTICS
        self.CASES_DETAIL = CASES_DETAIL
        self.VALID = VALID
        self.TEST_SCORE = TEST_SCORE
        self.RESULT = RESULT

        # 代码生难度的八分类的中心
        self.RAW_DIFFICULTY_CENTERS = []
        cr = csv.reader(open(CENTER), delimiter=",")
        for line in cr:
            self.RAW_DIFFICULTY_CENTERS.append(list(map(eval,line)))

        with open(self.TEST_DATA, 'r', encoding='utf-8') as f:
            # 获取原始数据
            self.raw_data = json.load(f)
        # 获取题目难度
        self.get_difficulty()
        # 获取每人每题最终得分
        self.get_final_score()
        # 获取每人每题的编码风格分
        self.get_code_style_score()
        # 获取每人每题的有效提交率
        self.get_valid_rate()
        # 获取每人每题的最终得分的权重
        self.get_test_score()
        # 获取题目类型
        self.get_case_type()

    def pre_get_code_style_score_dist(self):
        '''
        预先求出原始编码风格分数的分布情况
        :return:
        '''
        distr = []
        # 布长为5
        for i in range(-1710, 15, 5):
            distr.append(0)
        cr = csv.reader(open(self.USER_RESULT), delimiter=",")
        for row in cr:
            distr[int((float(row[3]) + 1710) // 5)] += 1
        print(distr)
        print(distr.index(212) * 5 - 1710)
        print(distr.index(6114) * 5 - 1710)
        # 画出编码风格分数分布图
        plt.bar(range(len(distr)), distr, color='#6a005f')
        plt.ylim(min(distr), max(distr))
        plt.title('Coding Style Score Distribution')
        plt.ylabel('number')
        plt.xlabel('score ( = x * 5 - 1710 )')
        plt.show()

    def __get_raw_scores(self):
        '''
        读取题目做题分数信息到字典中
        :return: 分数字典{}
        '''
        # 分数数据
        scores = {}
        cr = csv.reader(open(self.SCORE_STATISTICS), delimiter=",")
        next(cr)
        for row in cr:
            # row: 题目编号,平均数,中位数,众数,尝试人数,通过人数,平均提交次数,测试用例数
            scores[row[0]] = row[1:]
        return scores
    

    def __get_raw_difficulty_from_score(self, score):
        '''
        根据分数信息获取题目生难度
        :param score: 一个题目的分数信息
        :return: 一个题目的处理后的数据
        '''
        # 平均数换算难度
        avg = float(score[0])
        # 中位数换算难度
        med = float(score[1])
        # 众数换算难度
        cmn = np.average(list(map(float, score[2].split('|'))))
        # （通过人数：尝试人数）换算难度
        rte = int(score[4]) / int(score[3])
        # （用例总数：平均提交次数）换算难度
        tim = int(score[6]) / float(score[5])
        return [avg, med, cmn, rte, tim]

    def get_difficulty(self):
        '''
        根据八分类结果换算题目难度
        :return:
        '''
        # 计算欧氏距离
        def distance(a, b):
            return np.sqrt(np.sum([((a[i] - b[i]) ** 2) for i in range(len(a))]))
        # 分数数据
        scores = self.__get_raw_scores()
        # cnt = [0 for i in range(8)]
        for case in scores:
            raw_difficulty = self.__get_raw_difficulty_from_score(scores[case])
            # 计算离该题生难度最接近的中心点的下标
            index = np.argmin([distance(raw_difficulty, center) for center in self.RAW_DIFFICULTY_CENTERS])
            # cnt[index] += 1
            # 下标换算难度
            self.difficulty[case] = index / (len(self.RAW_DIFFICULTY_CENTERS) - 1) * (MAX_DIFFICULTY - MIN_DIFFICULTY) + MIN_DIFFICULTY
        # print(self.difficulty)
        # print(cnt)
        # plt.bar(range(len(cnt)), cnt, color='#6a005f')
        # plt.ylim(0, max(cnt))
        # plt.title('Case Difficulty Distribution')
        # plt.ylabel('number')
        # plt.xlabel('difficulty ( x -> X )')
        # plt.show()

    def get_final_score(self):
        '''
        获取用户的最终得分
        :return:
        '''
        cr = csv.reader(open(self.CASES_DETAIL, encoding = 'gb2312'), delimiter=",")
        next(cr)
        for row in cr:
            self.final_score[",".join(row[0:2])] = float(row[3])

    def get_code_style_score(self):
        '''
        获取用户的编码风格分数
        :return:
        '''
        cr = csv.reader(open(self.USER_RESULT), delimiter=",")
        for row in cr:
            score = float(row[3])
            if score < MIN_CODE_STYLE_SCORE: score = MIN_CODE_STYLE_SCORE
            if score > MAX_CODE_STYLE_SCORE: score = MAX_CODE_STYLE_SCORE #规整原始分数
            self.code_style_score[",".join(row[0:2])] = (score - MIN_CODE_STYLE_SCORE) / (MAX_CODE_STYLE_SCORE - MIN_CODE_STYLE_SCORE) * 100 #线性映射到 [0, 100]

    def get_valid_rate(self):
        '''
        获取用户的有效风格分数
        :return:
        '''
        cr = csv.reader(open(self.VALID), delimiter=",")
        next(cr)
        for row in cr:
            self.valid_rate[",".join(row[0:2])] = float(row[4])

    def get_test_score(self):
        '''
        获取用户的得分权重
        :return:
        '''
        cr = csv.reader(open(self.TEST_SCORE), delimiter=",")
        next(cr)
        for row in cr:
            self.test_score[",".join(row[0:2])] = float(row[2])

    def get_case_type(self):
        '''
        获取题目类型
        :return:
        '''
        cr = csv.reader(open(self.CASES_DETAIL, encoding = 'gb2312'), delimiter=",")
        next(cr)
        for row in cr:
            self.case_type[row[1]] = row[2]

    def code_score(self, uid, cid):
        '''
        获取用户的做题分数
        :param uid
        :param cid
        :return:做题分
        '''
        key = ",".join([uid, cid])
        if key in self.final_score and key in self.test_score:
            fs = self.final_score[key]
            wt = self.test_score[key]
            print("最终得分=" + str(fs) + " 权重=" + str(wt))
            return fs * wt
        else:
            print(key + "的最终成绩或权重缺失")
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
        scores = {}
        # 遍历此人交过的每道题目
        for case in self.raw_data[uid]["cases"]:
            cid = case["case_id"]
            print(",".join([uid, cid]))
            try:
                t = self.case_score(uid, cid)
            except Exception as e:
                print(str(e))
                t = 0
            print("题目分为" + str(t))
            # 加上这题的做题分
            score += t
            scores[cid] = t
            print()
        average = score / len(self.raw_data[uid]["cases"])
        return score, average, scores

    def one_user_score(self, user_id):
        '''
        获取某一个用户的成绩,方便执行查询
        :param user_id: str
        :return:
        '''
        row = [user_id]
        row.extend(self.user_score(user_id))
        # 每一类题的综合分的数组
        type_score = {}
        scores = row[3]
        for case in scores:
            type_score[self.case_type[case]] = type_score.get(self.case_type[case], []) + [scores[case]]
        row.append(type_score)
        return row

    def all_user_score(self):
        '''
        获取所有用户的计算后最终得分，并输出
        :return: 所有数据
        '''
        path = "/".join(self.RESULT.split("/")[:-1])
        result = []
        if(not os.path.exists(path)):
            os.mkdir(path)
        with open(self.RESULT, 'w', encoding="utf-8", newline="") as f:
            writer = csv.writer(f, delimiter = ",")
            writer.writerow(["用户编号", "作业完成情况", "总评分", "每题综合分的字典", "每一类题的综合分的数组"])
            for user in self.raw_data:
                row = self.one_user_score(user)
                writer.writerow(row)
                result.append(row)
        return result

if __name__ == '__main__':
    calculator = Calculator(
        "../JSON/test_data.json",
        "../OurModelOutPut/Users/user_result_0_36421.csv",
        "../OurModelOutPut/Cases/score_statistics.csv",
        "../OurModelOutPut/Cases/cases_detail.csv",
        "../OurModelOutPut/Valid/valid.csv",
        "../OurModelOutPut/Cases/user_weight.csv",
        "../OurModelOutPut/Result/all.csv",
        '../OurModelOutPut/Cases/difficulty_center.csv'
        )
    # calculator.pre_get_raw_difficulty_centers()
    # print(calculator.user_score('60699'))
    # calculator.all_user_score()
    print(calculator.one_user_score('3544'))
