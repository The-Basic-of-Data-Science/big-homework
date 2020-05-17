# -*- coding: utf-8 -*-

'''
综合能力评估
'''

def score(finalScore,weight):
    '''
    做题分
    :param finalScore 最终得分
    :param weight 权重
    :return:做题分
    '''
    return -1

def raw_difficult(average,median,mode,tryRate):
    '''
    题目生难度
    CsvResult中的分数统计.csv文件中加载
    :param average: 平均分
    :param median: 中位数
    :param mode: 众数
    :param tryRate: 尝试人的比例
    :return: 题目生难度
    '''
    return -1

def difficult(diffcults,rate):
    '''
    题目难度计算,进行离散化到0到rate上
    :param diffcults:dict{case_id:difficult}
    :param rate:这部分的占比，属于0-1
    :return:难度字典:dict{case_id:after_difficult}
    '''

def style(user_id, case_id, rate):
    '''
    获取用户的一道题目的所有提交的编码风格分
    数据来源:OurModel/Python/uid/cid下的所有python文件
    :param user_id:用户的id
    :param case_id:对应的题目的id
    :param rate:这部分占比，0-1
    :return:编码风格分
    '''

def qScore():
    '''
    题目分
    数据来源:其他方法，OurModel/CsvResult下的面向用例.csv
    :return:一道题目的最终标准得分
    '''
    return -1

def userScore(user_id):
    '''
    用户总评分
    数据来源:其他方法
    :param user_id 用户的id
    :return: 用户总评分
    '''
    return -1

if __name__ == '__main__':
    userScore('3544')