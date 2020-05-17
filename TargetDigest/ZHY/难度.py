# -*- coding: utf-8 -*-
import json
import numpy as np
import csv
from OriginDigest import UserDigest

data = {}
all_uploads = []

def loadJson(filename):
    global data
    with open(filename,encoding='utf-8') as f:
        data = json.load(f)

def getUserUpload(user):
    for case in user['cases']:
        res = [user['user_id'], case['case_id']]
        uploads = case['upload_records']
        res.append(len(uploads))
        scores = []
        for upload in uploads:
            scores.append(str(upload['score']))
        res.append('|'.join(scores))
        all_uploads.append(res)

def writeCsv(filename = '难度.csv'):
    head = ['user_id','case_id','提交次数','分数(用|分隔）']
    with open(filename,'w',encoding='utf-8',newline="") as f:
        writer = csv.writer(f)
        writer.writerow(head)
        for upload in all_uploads:
            writer.writerow(upload)

if __name__ == '__main__':
    loadJson('../../data/test_data.json')
    keys = list(data.keys())
    for user_id in keys:
        getUserUpload(data[user_id])
    writeCsv()




