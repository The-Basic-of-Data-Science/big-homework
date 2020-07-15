# -*- coding: utf-8 -*-
import csv
import urllib
import zipfile
import os
import json
import statistics
from tqdm import tqdm
import urllib.request

class StatisticsClass:
    def __init__(self, name, source, output):
        self.name = name
        self.source = source
        self.output = output

    def local_rm(self, dirpath):
        '''
        递归删除对应目录下所有的文件
        :param dirpath:目标目录
        :return:
        '''
        if os.path.exists(dirpath):
            files = os.listdir(dirpath)
            for file in files:
                filepath = os.path.join(dirpath, file).replace("\\",'/')
                if os.path.isdir(filepath):
                    self.local_rm(filepath)
                else:
                    os.remove(filepath)
            os.rmdir(dirpath)

    def get_tests_number(self, url):
        '''
        这个case的url中有几个测试用例
        :param url:
        :return: eval
        '''
        # 创建临时文件夹
        python_target = './temp/'
        if(not os.path.exists(python_target)):
            os.makedirs(python_target)
        temp = python_target + 'temp.zip'
        urllib.request.urlretrieve(url, temp)
        with zipfile.ZipFile(temp, 'r') as zzz:
            f_name = zzz.namelist()[0]
            zzz.extractall(path=python_target)
            with zipfile.ZipFile(python_target + f_name, 'r') as f:
                f.extract('.mooctest/testCases.json', python_target)
                with open(python_target + '.mooctest/testCases.json', 'r', encoding='utf-8') as f:
                    res = f.read()
                    data = json.loads(res)
        self.local_rm(python_target)
        return len(data)

    def case_score_statistics(self, case_id, scores, user_ids, test_cases_number):
        '''
        表格表头:case_id,平均分，中位数，众数，尝试人数，做对人数，平均提交次数，用例总数
        :param case_id: case的标识
        :param scores: 成绩序列
        :param user_ids: 做了这个题目的user_id
        :param test_cases_number: 用例总数
        :return:
        '''
        number_scores = list(map(eval, scores))
        result = [case_id]
        mean_data = statistics.mean(number_scores)
        result.append(mean_data)
        # 中位数
        median_data = statistics.median(number_scores)
        result.append(median_data)

        # 单独处理众数
        number_cnt = {}
        for num in number_scores:
            if num not in number_cnt.keys():
                number_cnt[num] = 1
            else:
                number_cnt[num] += 1
        keys = list(number_cnt.keys())
        keys.sort(reverse = True, key= lambda x : number_cnt[x])

        maxNumber = number_cnt[keys[0]]
        mode_data = []
        for key in keys:
            if(number_cnt[key] == maxNumber):
                mode_data.append(key)
        mode_data = '|'.join(list(map(str,mode_data)))
        result.append(mode_data)

        # 尝试人数
        number = len(user_ids.keys())
        result.append(number)

        # 做对人数
        correct_number = 0
        for user_id in user_ids:
            if(eval(user_ids[user_id]) == 100):
                correct_number += 1
        result.append(correct_number)

        if(number == 0):
            # 注意这里哟
            result.append("NaN")
        else:
            result.append(len(scores)/number)
        result.append(test_cases_number)

        return result

    def cases_score_statistics(self):
        '''
        我们使用${source}中数据再次之前我们3部分的运算,写入到Statistic下的 分数统计.csv文件夹下
        表格表头:case_id,平均分，中位数，众数，尝试人数，做对人数，平均提交次数，用例总数
        :return:
        '''
        # case_id->score
        scores = {}
        # case_id->(user_ids->final_scores)
        user_ids = {}
        # case_id->test_case_number
        test_cases = {}
        case_id_index = 1
        # 加载基本数据
        with open(self.source, 'r') as f:
            reader = csv.reader(f)
            for line in tqdm(reader):
                if(line[0] == 'user_id'):
                    continue
                if(line[case_id_index] not in scores.keys()):
                    scores[line[case_id_index]] = [line[6]]
                    user_ids[line[case_id_index]] = {line[0]:line[3]}
                    test_cases[line[case_id_index]] = self.get_tests_number(line[5])
                else:
                    scores[line[case_id_index]].append(line[6])
                    if(line[0] not in user_ids[line[case_id_index]].keys()):
                        user_ids[line[case_id_index]][line[0]] = line[3]
        # 开始统计
        result = [['case_id', 'mean_data', 'median_data', 'mode_data', 'try_number', 'pass_number'
                      , 'average_upload_times', 'test_cases_number']]
        case_ids = list(scores.keys())
        for x in range(len(case_ids)):
            case_id = case_ids[x]
            temp = self.case_score_statistics(case_id, scores[case_id], user_ids[case_id]
                                              , test_cases[case_id])
            if(len(temp) == 8):
                result.append(temp)
        # 持久化
        self.list_to_csv("score_statistics", result)

    def usercase_action_statistics(self, user_id, case_id, scores,final_score, test_cases_number):
        '''
        处理一个用户的一个题目的情况
        :param user_id:
        :param case_id:
        :param scores: Eg. [100.0, 0.0]
        :param final_score:
        :param test_cases_number:
        :return: 一个用户一道题的情况
        '''
        result = [user_id, case_id, len(scores)]
        scoreStr = "|".join(scores)
        result.append(scoreStr)
        change_score = []
        for x in range(1,len(scores)):
            change_score.append(eval(scores[x]) - eval(scores[x - 1]))
        change_score_str = '|'.join(list(map(str,change_score)))
        result.append(change_score_str)
        result.append(final_score)
        result.append(test_cases_number)
        return result

    def action_statistics(self):
        '''
        我们使用OurModel/CsvResult/detail.csv中数据再次之前我们3部分的运算,写入到CsvStatistic下的 用户行为统计.csv文件夹下
        表格表头:user_id,case_id,提交次数，每次分数(|分隔，第一个是第一次有效提交分数)，分数变化，最终有效分数, 用例数量，TODO 编码放歌分数
        :return:
        '''
        # 预加载数据并处理
        result = [['user_id', 'case_id', 'upload_times', 'every_scores'
                          , 'scores_change', 'final_score', 'test_cases_number']]
        with open(self.source,'r') as f:
            reader = csv.reader(f)
            temp = []
            for line in tqdm(reader):
                # 忽略第一行
                if(line[0] == 'user_id'):
                    continue
                if(len(temp) == 0):
                    temp.append(line)
                else:
                    if(temp[0][0] == line[0] and temp[0][1] == line[1]):
                        temp.append(line)
                    else:
                        scores = []
                        for t in temp:
                            scores.append(t[6])
                        result_temp = self.usercase_action_statistics(temp[0][0], temp[0][1]
                                                            , scores, temp[0][3], self.get_tests_number(temp[0][5]))
                        if(len(result_temp) == 7):
                            result.append(result_temp)
                        else:
                            print('7 Error!')
                        temp = [line]
            if(len(temp) != 0):
                scores = []
                for t in temp:
                    scores.append(t[6])
                result_temp = self.usercase_action_statistics(temp[0][0], temp[0][1],
                                                         scores, temp[0][3], self.get_tests_number(temp[0][5]))
                if (len(result_temp) == 7):
                    result.append(result_temp)
                else:
                    print('7 Error!')
        self.list_to_csv('action_statistics',result)

    def list_to_csv(self, filename, arrays):
        '''
        将数组加载到CSV
        :param filename: 文件名（不含后缀)
        :param arrays: array
        :return:
        '''
        if(not os.path.exists(self.output)):
            os.makedirs(self.output)
        with open(self.output + filename + ".csv", 'w', newline="") as f:
            writer = csv.writer(f)
            for line in arrays:
                writer.writerow(line)

    def my_statistics(self):
        self.cases_score_statistics()
        self.action_statistics()

    def user_to_case_statistics(self):
        '''
        统计有效情况，不计入多线程计算部分
        :return:
        '''
        # userid -> caseid -> [allUploads, validUploads]
        list_result = []
        for x in range(1, 20):
            # 统计一个模块的部分
            result = {}
            json_path = "../JSON_Chunk/ChunkJSON/test_data_" + str(x) + ".json"
            # 统计总共提交次数
            with open(json_path, 'r') as f:
                text = f.read()
                data = json.loads(text)
                user_ids = list(data.keys())
                for user_id in user_ids:
                    result[user_id] = {}
                    cases = data[user_id]['cases']
                    for case in cases:
                        result[user_id][case['case_id']] = [len(case['upload_records'])]
            # 统计有效次数
            detail_path = "../OurModelOutPut/python_source/test_data_" + str(x) + "/CsvResult/detail.csv"
            with open(detail_path, 'r') as f2:
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
        # 输出到csv文件
        output_path = "../OurModelOutPut/Valid"
        if(not os.path.exists(output_path)):
            os.makedirs(output_path)
        list_result.insert(0,['user_id','case_id','all_uploads_number','valid_uploads_number','valid_rate'])
        with open(output_path + "/" + "valid.csv", 'w', newline="") as f:
            writer = csv.writer(f)
            for line in list_result:
                writer.writerow(line)

if __name__ == '__main__':
    source = "./CsvResult/detail.csv"
    output = "./Statistic/"
    temp = StatisticsClass("temp", source, output)
    # temp.my_statistics()
    temp.user_to_case_statistics()