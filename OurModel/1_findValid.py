# -*- coding: utf-8 -*-
# 有效性分析
target = '../../test_data.json'

def checkIfElse(txt):
    '''
    检查该文本是否满足if-else-print阈值>=3?
    :param txt:
    :return: 布尔类型
    '''
    return True

def checkSpecific(txt):
    '''
    检查该文本是否使用了特殊的库
    :param txt:
    :return: 布尔类型
    '''
    return True

def checkOneValid(url):
    '''
    1. 检查一个提交的有效性,从url拿到ZIP，再拿到Python中的文本
    使用checkIfElse 和 checkSpecific
    2. (有效提交)将Python文件按照uid/cid/upLoadId.py的文件名存储到Python文件夹下
    :param url: oss远端的ZIP地址
    :return: 布尔类型
    '''
    return True

def checkAllUploads(filename = target):
    '''
    1. 检查filename中的所有提交
    2. 使用checkOneValid方法
    3. 将结果的全新的Json文件加载到 OurModel/Data/filename.json
    4. 对于每一个用户每一道题目，统计面向用例次数和提交总数，并且写入到CsvResult下的 面向用例.csv 文件中
       表头:uid,case_id,面向用例次数,提交次数(这部分不受alpha的影响)

    :param filename:json文件
    :return:
    '''
    return True

def filter(alpha = 0.8):
    '''
    从OurModel/Data/filename.json中加载数据，筛选出80%的数据，写入到OurModel/AfterData/filename.json文件中
    :param alpha:我们统计的数据占整体的比例
    alpha [0,1],比如alpha = 0.8 -> 我们选择有效数据中间80%的数据
    :return:
    '''
    return True


if __name__ == '__main__':
    '''
    从target中加载原始数据
    '''
    checkAllUploads()
    filter()
