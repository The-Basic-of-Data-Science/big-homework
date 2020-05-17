# -*- coding: utf-8 -*-
import json
import numpy as np
import csv
from tqdm import tqdm

if __name__ == '__main__':
    with open('../../data/test_data.json', encoding='utf-8') as f:
        res = json.load(f)

    commit_of_case = {}
    time_of_case = {}

    for uid in tqdm(res):
        # 每一个用户
        cases = res[uid]['cases']
        # 拿到用户的所有的cases
        for case in cases:
            # 对于某一个用户做的一道题目
            cid = case['case_id']
            if not cid in commit_of_case: commit_of_case[cid] = []
            if not cid in time_of_case: time_of_case[cid] = []

            commit_of_case[cid].append(len(case['upload_records']))

            if(len(case['upload_records']) == 0):
                time_of_case[cid].append(0)
            else:
                small = case['upload_records'][0]['upload_time']
                duration = 0
                for upload in case['upload_records']:
                    if(upload['score'] == 100):
                        duration = upload['upload_time'] - small
                time_of_case[cid].append(duration)
    head = ['case_id', '平均做对时间', '平均提交次数']
    with open('难度b.csv', 'w', newline="") as file:
        writer = csv.writer(file)
        writer.writerow(head)
        for cid in commit_of_case:
            c = commit_of_case[cid]
            t = time_of_case[cid]
            writer.writerow([cid, np.mean(t), np.mean(c)])
