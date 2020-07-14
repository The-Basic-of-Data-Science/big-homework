# -*- coding: utf-8 -*-
import json

def count(source = "../JSON/test_data.json"):
    with open(source, 'r', encoding='utf-8') as f:
        res = f.read()
        data = json.loads(res)
    user_ids = list(data.keys())
    print("用户共有 {} 位。".format(len(user_ids)))
    result = {}
    uploads_count = 0
    no_uploads = 0
    for user_id in user_ids:
        cases = data[user_id]['cases']
        for case in cases:
            type = case['case_type']
            uploads_count += len(case['upload_records'])
            if(len(case['upload_records']) == 0):
                no_uploads += 1
            if(type in result.keys()):
                result[type] += 1
            else:
                result[type] = 1

    cnt = 0
    for key in result.keys():
        cnt += result[key]
        print("{} 类题型的题目共被计算了 {} 次。".format(key, result[key]))
    print("一共有 {} 条提交记录。".format(uploads_count))
    print("一共有 {} 次做题记录，其中 {} 次做题记录没有提交记录。".format(cnt, no_uploads))

if __name__ == '__main__':
    count()