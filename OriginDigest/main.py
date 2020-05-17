# -*- coding: utf-8 -*-
import json
from OriginDigest import UserDigest
from OriginDigest import CaseDigest
from OriginDigest import OutPut

data = {}
file1 = "../Data/sample.json"
file2 = "../Data/test_data.json"

def load(fileName):
    # 加载数据到内存
    global data
    with open(fileName,encoding = 'utf-8') as f:
        res = f.read()
        data = json.loads(res)

def retrive():
    # 按照用户、题目拉取获得均分
    global data
    for user_id in data.keys():
        user = data[user_id]
        UserDigest.digestAUser(user_id,user)

def getAllcases():
    # 获取全部的题目
    global data
    cases = []
    for user_id in data.keys():
        user = data[user_id]
        userCases = UserDigest.getUserCases(user)
        for userCase in userCases:
            cases.append(userCase)
    return cases

def getByUidAndCid(uid,cid):
    '''
    根据Uid和Cid查找对应的case
    :param uid: str
    :param cid: str
    :return:
    '''
    user = data[uid]
    cases = UserDigest.getUserCases(user) # 含有filter条件
    afterCases = UserDigest.getByUidAndCid(uid,cid,cases)
    print(uid,cid,afterCases)
    return afterCases

def mergeCaseAndUpload(cases):
    # 合并Case和Upload
    print("___________________")
    cnt_Case = CaseDigest.cntCase(cases)
    print("___________________")
    cnt_Upload = CaseDigest.cntUpload(cases)
    print("___________________")
    keys = list(cnt_Case.keys())
    cnt_after = {}
    for key in keys:
        temp = [cnt_Case[key], cnt_Upload[key]]
        cnt_after[key] = temp
    afterKeys = list(cnt_after.keys())
    afterKeys.sort(key = lambda x:cnt_after[x][1],reverse = True)
    # key -> case_id value ->[cnt_case[id],cnt_upload[id]]
    OutPut.printDict(cnt_after,afterKeys)
    return cnt_after

def getSpecificCategory(category):
    UserDigest.category = category
    cases = getAllcases()
    print(len(cases))
    mergeCaseAndUpload(cases)

def getAllCategory():
    print('排序算法')
    getSpecificCategory('排序算法')
    print('查找算法')
    getSpecificCategory('查找算法')
    print('图结构')
    getSpecificCategory('图结构')
    print('树结构')
    getSpecificCategory('树结构')
    print('数字操作')
    getSpecificCategory('数字操作')
    print('字符串')
    getSpecificCategory('字符串')
    print('线性表')
    getSpecificCategory('线性表')
    print('数组')
    getSpecificCategory('数组')


if __name__ == '__main__':
    load(file2)
    # getAllCategory()

