# -*- coding: utf-8 -*-
from OriginDigest import OutPut

file_prefix = "../AfterData/"

def filter_Record(record):
    # 添加条件计算
    return True

def uploadRecords(user_id,case_id,records):
    # 对于record进行检查计算
    cnt = len(records)
    if(cnt == 0):
        return
    res = 0
    for record in records:
        if(filter_Record(record)):
            res += record["score"]
    average = res/cnt
    temp = [user_id,case_id,cnt,average]
    OutPut.writeCSV(file_prefix + "average.csv",temp)

