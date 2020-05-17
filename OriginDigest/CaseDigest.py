# -*- coding: utf-8 -*-
from OriginDigest import UploadDigest
from OriginDigest import OutPut

cnt_Case = {}
cnt_Upload = {}

def aUserUpLoad(user_id,cases):
    # 获取一个用户的Cases
    for case in cases:
        UploadDigest.uploadRecords(user_id,case["case_id"],case["upload_records"])

def cntCase(cases):
    # 统计cases
    global cnt_Case
    cnt_Case = {} # 清空
    for case in cases:
        cid = case['case_id']
        if(cid in cnt_Case):
            cnt_Case[cid] += 1
        else:
            cnt_Case[cid] = 1
    keys = list(cnt_Case.keys())
    keys.sort(key=lambda x:cnt_Case[x],reverse=True)
    OutPut.printDict(cnt_Case,keys)
    return cnt_Case

def cntUpload(cases):
    global cnt_Upload
    cnt_Upload = {} # 清空
    for case in cases:
        cid = case['case_id']
        if(cid in cnt_Upload):
            cnt_Upload[cid] += len(case['upload_records'])
        else:
            cnt_Upload[cid] = len(case['upload_records'])
    keys = list(cnt_Upload.keys())
    keys.sort(key=lambda x:cnt_Upload[x],reverse=True)
    OutPut.printDict(cnt_Upload,keys)
    return cnt_Upload