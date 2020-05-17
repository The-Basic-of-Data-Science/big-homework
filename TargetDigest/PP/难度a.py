#!/bin/python3

import json
import numpy as np
import csv
from scipy import stats

with open('../../data/test_data.json') as f:
    res = json.load(f)

all_score_of_case = {} #某一题，所有人的所有提交的分数
final_score_of_case = {} #某一题，所有人的最终分数

for uid in res:
    cases = res[uid]['cases']
    for case in cases:
        cid = case['case_id']
        if not cid in all_score_of_case: all_score_of_case[cid] = []
        if not cid in final_score_of_case: final_score_of_case[cid] = []

        final_score_of_case[cid].append(case['final_score'])

        for upload in case['upload_records']:
            all_score_of_case[cid].append(upload['score'])

head = ['case_id', '所有提交平均分', '所有提交中位数', '所有提交众数', '最终分数平均分', '最终分数中位数', '最终分数众数', '做的人数', '做对人数']

with open('难度a.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerow(head)
    for cid in all_score_of_case:
        a = all_score_of_case[cid]
        f = final_score_of_case[cid]
        writer.writerow([cid, np.mean(a), np.median(a), stats.mode(a)[0][0], np.mean(f), np.median(f), stats.mode(f)[0][0], len(f), f.count(100)])
