# -*- coding: utf-8 -*-

from sklearn import cluster
import csv
import numpy as np

'''
题目难度聚类分析,输出八分类中心
'''
class CaseCalculator:
    def __init__(self, score_statistics,  output):
        self.score_statistics = score_statistics
        self.output = output

    def __get_raw_scores(self):
        '''
        读取题目做题分数信息到字典中
        :return: 分数字典{}
        '''
        # 分数数据
        scores = {}
        cr = csv.reader(open(self.score_statistics), delimiter=",")
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

    def pre_get_raw_difficulty_centers(self):
        '''
        预先使用K-mean++方法求出生难度的分类中心
        :return:
        '''
        # 分数数据
        scores = self.__get_raw_scores()
        # 生难度
        raw_difficulty = []
        for case in scores:
            raw_difficulty.append(self.__get_raw_difficulty_from_score(scores[case]))
        data = raw_difficulty
        # 进行八分类
        clf = cluster.KMeans(init='k-means++', n_clusters=8, random_state=794780360)
        # 执行聚类算法
        clf.fit(data)
        # 输出八分类点
        result = [list(center) for center in clf.cluster_centers_]
        result.sort(reverse = True)
        with open(self.output, 'w', newline="") as f:
            writer = csv.writer(f)
            for center in result:
                writer.writerow(center)

if __name__ == '__main__':
    caseCalculator = CaseCalculator("../OurModelOutPut/Cases/score_statistics.csv",
                                    "../OurModelOutPut/Cases/difficulty_center.csv")
    caseCalculator.pre_get_raw_difficulty_centers()