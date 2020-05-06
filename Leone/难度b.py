# -*- coding: utf-8 -*-

import json
import numpy as np
import csv

with open('../data/test_data.json') as f:
    res = json.load(f)

commit_of_case = {}
time_of_case = {}

for uid in res:
    cases = res[uid]['cases']
    for case in cases:
        cid = case['case_id']
        if not cid in all_score_of_case: all_score_of_case[cid] = []
        if not cid in final_score_of_case: final_score_of_case[cid] = []

        for upload in case['upload_records']:
            commit_of_case[cid].append(len(upload))

        if case['final_score'] == 100:
            for upload in case['upload_records']:
                time_of_case[cid].append(upload[upload_time])

head = ['case_id', '平均做对时间', '平均提交次数']

with open('./难度b.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerow(head)
    for cid in commit_of_case:
        c = commit_of_case[cid]
        t = time_of_case[cid]
        writer.writerow([cid, np.mean(c), np.ptp(t, axis = 1)])
