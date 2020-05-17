# -*- coding: utf-8 -*-
import json
import urllib.request,urllib.parse
import os
from tqdm import tqdm

def downloadCase(case):
    '''
    下载题目
    :param case:题目
    :return:
    '''
    filename = urllib.parse.unquote(os.path.basename(case['case_zip']), encoding='utf-8')
    print(filename)
    downloadZIP(case['case_zip'],filename,"题目" + "/" + case['case_type'] + "_","_题目")

def downloadZIP(remote,target,prefix,suffix):
    '''
    下载ZIP文件
    :param remote:OSS地址
    :param target:文件名
    :param suffix:文件夹后缀
    :param prefix:文件夹前缀
    :return:
    '''
    category = target.split("_")[0]
    target_path = "../ZIPS/" + prefix + category + suffix
    if (not os.path.exists(target_path)):
        os.makedirs(target_path)
    if(os.path.exists(target_path + "/" + target)):
        print("Already download!")
        return
    urllib.request.urlretrieve(remote,target_path + "/" + target)

def getCaseUpLoad(user_id,case):
    records = case['upload_records']
    for record in records:
        target = urllib.parse.unquote(os.path.basename(record['code_url']),encoding='utf-8')
        print(target)
        prefix = user_id + "/" + case['case_type'] + "_" + case['case_id'] + "/"
        suffix = ""
        downloadZIP(record['code_url'],target,prefix,suffix)

def getAUserCaseAndRecords(user):
    cases = user['cases']
    supperPrefix = "../ZIPS"
    if(not os.path.exists(supperPrefix)):
        os.mkdir(supperPrefix)
    for case in cases:
        downloadCase(case)
        getCaseUpLoad(user_id, case)

def getAUserRecords(user):
    cases = user['cases']
    supperPrefix = "../ZIPS"
    if(not os.path.exists(supperPrefix)):
        os.mkdir(supperPrefix)
    for case in cases:
        getCaseUpLoad(user_id, case)


if __name__ == '__main__':
    f = open("../Data/sample.json", encoding ='utf-8')
    res = f.read()
    data = json.loads(res)
    userIDS = list(data.keys())
    for user_id in tqdm(userIDS):
        user = data[user_id]
        getAUserRecords(user)
        break
