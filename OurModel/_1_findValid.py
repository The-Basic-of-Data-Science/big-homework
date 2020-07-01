# -*- coding: utf-8 -*-
# 有效性分析
import json
import os
import csv
# ['user_id', 'case_id', 'upload_id']
brief_result = [['user_id', 'case_id', 'upload_id']]
# ['user_id', 'case_id', 'case_type','final_score','upload_id','code_url','upload_score','upload_time']
detail_result = [['user_id', 'case_id', 'case_type','final_score','upload_id','code_url','upload_score','upload_time']]

def checkIfElse(text):
    '''
    检查该文本是否满足if-else-print阈值>=3?
    :param text:
    :return: boolean
    '''
    return True

def checkSpecific(text):
    '''
    检查该文本是否使用了特殊的库
    :param text:
    :return: boolean
    '''
    return True

def validToCsv(user_id, case_id, upload):
    '''
    将有效提交记录到csv表格中去
    :param user_id:
    :param case_id:
    :param upload:
    :return:
    '''
    upload_id = upload.split("_")[0] # 加载upload_id
    brief_result.append([user_id, case_id, upload_id])

def checkOneValid(user_id, case_id, upload, python_source):
    '''
    1. 检查一个提交的有效性,从url拿到ZIP，再拿到Python中的文本
    使用checkIfElse 和 checkSpecific
    2. 将全部Python文件按照uid/cid/upLoadId.py的文件名存储到Python文件夹下
    :param user_id: 用户的id
    :param case_id: 题目的id
    :param upload: Python的文件名
    :return: boolean
    '''
    with open(python_source + "/" + user_id + "/" + case_id + "/" + upload, 'r') as f:
        try:
            text = f.read()
            # 根据情况进行过滤 TODO
            if(checkIfElse(text) and checkSpecific(text)):
                validToCsv(user_id,case_id,upload)
        except Exception as e:
            #一般是不能通过编译，英文符号
            print(str(e))
            print(python_source + "/" + user_id + "/" + case_id + "/" + upload)
    return True

def checkAllUploads(python_source, output):
    '''
    对本地已经加载出来的Python文件夹中的用户提交的数据进行统计
    本地的存储为为Python/user_id/case_id/xxx.py
    :param filename:json文件
    :param python_source valid-Python存放的位置
    :param output 输出文件夹
    :return: boolean
    '''
    user_ids = os.listdir(python_source)
    for user_id in user_ids:
        # 每一个用户
        if(user_id == 'main.py'):
            continue
        case_ids = os.listdir(python_source + "/" + user_id)
        for case_id in case_ids:
            # 每一道题目
            uploads = os.listdir(python_source + "/" + user_id + "/" + case_id)
            for upload in uploads:
                # 每一次提交
                checkOneValid(user_id, case_id, upload, python_source)
    refreshCSV('brief', brief_result, output)

def filter(alpha = 0.8):
    '''
    TODO
    从OurModel/JSON/filename.json中加载数据，筛选出80%的数据，写入到OurModel/AfterData/filename.json文件中
    :param alpha:我们统计的数据占整体的比例
    alpha [0,1],比如alpha = 0.8 -> 我们选择有效数据中间80%的数据
    :return: boolean
    '''
    return True

def refreshCSV(filename, source, output):
    '''
    将source中的数据格式化到CsvResult/filename.csv中去
    :param filename: 文件名
    :param source: 源文件
    :param output: 输出文件夹
    :return:
    '''
    if(not os.path.exists(output)):
        os.makedirs(output)
    with open(output + "/" + filename + ".csv",'w',newline="") as f:
        writer = csv.writer(f)
        for br in source:
            if(len(br) != 0 and len(br[0]) != 0):
                writer.writerow(br)

def briefToDetail(source, output):
    # 加载出Json格式的data数据
    with open(source, 'r', encoding='utf-8') as f:
        res = f.read()
        data = json.loads(res)
    now_uid = ''
    with open(output + "/brief.csv",'r') as f:
        reader = csv.reader(f)
        for line in reader:
            # 排除第一行
            if(line[0] == 'user_id'):
                continue
            # line [user_id, case_id, upload_id]
            if (now_uid != line[0]):
                now_uid = line[0]
                user = data[line[0]]
            result = getOneLine(user['cases'], line[0],line[1], line[2])
            if(len(result) != 0):
                detail_result.append(result)
    refreshCSV('detail',detail_result, output)

def getOneLine(cases, user_id, case_id, upload_id):
    '''
    从cases中找到对应case_id和upload_id的情况来
    :param cases:
    :param user_id:
    :param case_id:
    :param upload_id:
    :return:
    '''
    result = [user_id, case_id]
    for case in cases:
        if(str(case['case_id']) == case_id):
            result.append(case['case_type'])
            result.append(case['final_score'])
            result.append(upload_id)
            for upload in case['upload_records']:
                if(str(upload['upload_id']) == upload_id):
                    result.append(upload['code_url'])
                    result.append(upload['score'])
                    result.append(upload['upload_time'])
                    if(len(result) != 8):
                        print("长度不为8")
                        return []
                    return result
    print('failed to find!')
    return []

def findValid(python_source, source, output):
    checkAllUploads(python_source, output)
    briefToDetail(source, output)
    filter()

if __name__ == '__main__':
    # 检查每一个应用的有效性
    findValid("./Python", '../JSON/test_data.json', './CsvResult')
