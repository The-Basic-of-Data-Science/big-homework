# -*- coding: utf-8 -*-
import json
import os
import csv

class ValidCheck:
    def __init__(self, json_source, detail_path, output):
        self.json_source = json_source
        self.detail_path = detail_path
        self.output = output

    def user_valid(self):
        '''
        统计用户有效提交情况，不计入多线程计算部分
        :return: 当前块的信息
        '''
        # userid -> caseid -> [allUploads, validUploads]
        list_result = []
        # 统计一个模块的部分
        result = {}
        # 统计总共提交次数
        with open(self.json_source, 'r') as f:
            text = f.read()
            data = json.loads(text)
            user_ids = list(data.keys())
            for user_id in user_ids:
                result[user_id] = {}
                cases = data[user_id]['cases']
                for case in cases:
                    result[user_id][case['case_id']] = [len(case['upload_records'])]
        # 统计有效次数
        with open(self.detail_path, 'r') as f2:
            data2 = csv.reader(f2)
            for line in data2:
                if(line[0] == 'user_id'):
                    continue
                if(len(result[line[0]][line[1]]) == 1):
                    result[line[0]][line[1]].append(1)
                elif(len(result[line[0]][line[1]]) == 2):
                    result[line[0]][line[1]][1] += 1
                else:
                    print("ERROR!")
        for user in result:
            for case in result[user]:
                if(len(result[user][case]) == 1):
                    result[user][case].append(0)
                valid = result[user][case][1]
                all = result[user][case][0]
                if(all == 0):
                    valid_rate = 0
                else:
                    valid_rate = valid / all
                list_result.append([user, case, all, valid, valid_rate])
        return list_result

def check_all_chunks(output):
    list_result = []
    for x in range(1, 2):
        valid_check = ValidCheck("../JSON_Chunk/ChunkJSON/test_data_" + str(x) + ".json",
                                 "../OurModelOutPut/python_source/test_data_" + str(x) + "/CsvResult/detail.csv",
                                 output)
        temp = valid_check.user_valid()
        list_result.extend(temp)
    # 输出到csv文件
    if (not os.path.exists(output)):
        os.makedirs(output)
    list_result.insert(0, ['user_id', 'case_id', 'all_uploads_number', 'valid_uploads_number', 'valid_rate'])
    with open(output + "/valid.csv", 'w', newline="") as f:
        writer = csv.writer(f)
        for line in list_result:
            writer.writerow(line)

if __name__ == '__main__':
    check_all_chunks("../OurModelOutPut/Valid")
