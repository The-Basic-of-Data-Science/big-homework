# -*- coding: utf-8 -*-
from digest import CaseDigest

category = '查找算法'

def digestAUser(user_id,user):
    # 按照用户分类进行处理
    cases = user['cases']
    CaseDigest.aUserUpLoad(user_id,cases)

def filter_Cases(case):
    # 添加筛选添加，目前筛选出了等于100的
    # if (case['final_score'] == 100):
    global category
    if(category == '*'):
        return True
    if(case['case_type'] == category and case['final_score'] == 100):
        return True

def getUserCases(user):
    # 获取一个用户的全部case
    cases = user['cases']
    after_Cases = []
    for case in cases:
        if(filter_Cases(case)):
            after_Cases.append(case)
    return after_Cases

def getByUidAndCid(uid,cid,cases):
    # 按照uid，cid获取cases
    result = []
    for case in cases:
        if(case['case_id'] == cid):
            result.append(case)
    print(uid,result)
    return result