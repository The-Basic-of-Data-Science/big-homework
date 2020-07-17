# -*- coding: utf-8 -*-

'''
综合能力评估
'''

# TODO 调试参数
MIN_DIFFICULTY = 0.1 #最小难度
MAX_DIFFICULTY = 0.8 #最大难度，也就是分数部分占比
STYLE_RATE = 1 - MAX_DIFFICULTY #风格分占比



import json
import csv
import numpy as np

usage_count = {} #每题用例数量
difficulty = {} #难度
final_score = {} #每人每题的最终得分，键名为 "uid,cid"
valid_rate = {} #每人每题的有效提交率，键名为 "uid,cid"

def get_difficulty(x2, y2):
    scores = {} #读取分数文件
    raw_difficulty = {} #生难度

    cr = csv.reader(open("../OurModelOutPut/Cases/score_statistics.csv"), delimiter=",")
    next(cr)
    for row in cr:
        scores[row[0]] = row[1:]
        usage_count[row[0]] = row[7]
    
    for case in scores:
        avg = (100 - float(scores[case][0])) / 100 #平均数换算难度
        med = (100 - float(scores[case][1])) / 100 #中位数换算难度
        cmn = (100 - max(list(map(float, scores[case][2].split('|'))))) / 100 #众数换算难度
        rte = (int(scores[case][3]) - int(scores[case][4])) / int(scores[case][4]) #（做错人数：做对人数）换算难度
        tim = float(scores[case][5]) / int(scores[case][6]) #（平均提交次数：用例总数）换算难度
        # TODO 这里只是单纯地加起来，后期再调试 PCA AHP
        raw_difficulty[case] = avg + med + cmn + rte + tim
    
    x1 = min(raw_difficulty.values()) #最小生难度
    y1 = max(raw_difficulty.values()) #最大生难度

    # TODO 这里用的直线的映射，是否有其他关系，待调试
    k = (y2 - x2) / (y1 - x1)
    b = (x2 * y1 - x1 * y2) / (y1 - x1)

    for case in raw_difficulty:
        difficulty[case] = raw_difficulty[case] * k + b

def get_final_score():
    # TODO
    cr = csv.reader(open("../OurModelOutPut/Cases/cases_detail.csv", encoding = 'gb2312'), delimiter=",")
    next(cr)
    for row in cr:
        final_score[",".join(row[0:2])] = float(row[3])

def get_valid_rate():
    cr = csv.reader(open("../OurModelOutPut/Valid/valid.csv"), delimiter=",")
    next(cr)
    for row in cr:
        valid_rate[",".join(row[0:2])] = float(row[4])

with open("../JSON/test_data.json", 'r', encoding='utf-8') as f:
    rd = json.load(f)
    # raw_data, 这里我先用脏数据

get_difficulty(MIN_DIFFICULTY, MAX_DIFFICULTY) #获取难度，映射在 [MIN_DIFFICULTY, MAX_DIFFICULTY] 上
get_final_score() #获取每人每题最终得分
get_valid_rate()

def score(uid, cid):
    '''
    做题分
    :param uid
    :param cid
    :return:做题分
    '''
    # TODO 得到weight
    weight = 1
    if ",".join([uid, cid]) in final_score:
        print("最终得分=" + str(final_score[",".join([uid, cid])]) + " 权重=" + str(weight))
        return final_score[",".join([uid, cid])] * weight
    else:
        print(",".join([uid, cid]) + "的最终成绩缺失")
        return 0

def style(uid, cid):
    '''
    获取用户的一道题目的所有提交的编码风格分
    数据来源:OurModel/Python/uid/cid下的所有python文件
    :param user_id:用户的id
    :param case_id:对应的题目的id
    :param rate:这部分占比，0-1
    :return:编码风格分
    '''
    ss = STYLE_RATE * 100
    # TODO 计算风格分
    print("编码风格分=" + str(ss))
    return ss

def qScore(uid, cid):
    '''
    题目分=（做题分*题目难度+编码风格分）*（有效提交比例）
    数据来源:其他方法，OurModel/CsvResult下的面向用例.csv
    :return:一道题目的最终标准得分
    '''
    scr = score(uid, cid) * difficulty[cid] + style(uid, cid)
    rte = valid_rate[",".join([uid, cid])]
    print("（做题分*题目难度+编码风格分）=" + str(scr) + " （有效提交比例）" + str(rte))
    return scr * rte

def userScore(uid):
    '''
    用户总评分=所有做过的题目的题目分总和
    数据来源:其他方法
    :param uid 用户的id
    :return: 用户总评分
    '''
    if not uid in rd:
        print("没有这个人")
        return
    score = 0
    for case in rd[uid]["cases"]: #遍历此人交过的每道题目
        print(",".join([uid, case["case_id"]]))
        t = qScore(uid, case["case_id"])
        print("题目分为" + str(t))
        score += t #加上这题的做题分
        print()
    return score

if __name__ == '__main__':
    print(userScore('60699'))
