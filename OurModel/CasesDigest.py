# -*- coding: utf-8 -*-
import csv
import os
from tqdm import tqdm
from OurModel import _2_Statisic

'''
统计题目难度，将各块的brief汇总生成detail,在FindValid之后进行，之后根据汇总的detail进行处理
'''
class CaseDigestClass:
    def __init__(self, name, json_path, source, output):
        '''
        类构造方法
        :param name: 类备注名
        :param source: Python输出的根目录 OurModelOutPut
        :param output: 输出的目标目录
        '''
        self.name = name
        self.json_path = json_path
        self.source = source
        self.output = output
        # 暂时加载到内存
        self.cases = []
        self.titles = [["user_id", "case_id", "upload_id"],
                      ['user_id', 'case_id', 'case_type', 'final_score', 'upload_id', 'code_url', 'upload_score', 'upload_time']]

    def all_cases_by_type(self, type):
        if type not in ["detail", "brief"]:
            print("Type must be \"detail\" or \"brief\".")
            return
        list_dir = os.listdir(self.source)
        for chunk in tqdm(list_dir):
            # 避开统计结果
            if chunk == "Cases" :
                continue
            with open(self.source + "/" + chunk + "/CsvResult/" + type + ".csv", 'r') as f:
                reader = csv.reader(f)
                for line in reader:
                    if(line[0] == 'user_id'):
                        continue
                    self.cases.append(line)
        self.cases.sort(key = lambda x : x[1])
        if(type == "brief"):
            title = self.titles[0]
        else:
            title = self.titles[1]
        self.cases.insert(0, title)
        self.list_to_csv('cases_' + type, self.cases)
        print("有效提交次数为 {} 次".format(len(self.cases)))
        self.cases.clear()

    def cases_statistics(self):
        my_statistics = _2_Statisic.StatisticsClass("题目分数统计", self.output + "/cases_detail.csv",self.output)
        # 统计题目难度
        # my_statistics.cases_score_statistics()
        # 统计用户行为
        my_statistics.action_statistics()

    def list_to_csv(self, filename, data):
        '''
        将source中的数据格式化到CsvResult/filename.csv中去
        :param filename: 文件名
        :param source: 源文件
        :param output: 输出文件夹
        :return:
        '''
        with open(self.output + "/" + filename + ".csv",'w',newline="") as f:
            writer = csv.writer(f)
            for br in data:
                writer.writerow(br)

    def all_cases(self):
        # 如果没有目录则创建
        if not os.path.exists(self.output):
            os.makedirs(self.output)
        print("Brief Union!")
        # self.all_cases_by_type("brief")
        print("Detail Union!")
        # self.all_cases_by_type('detail')
        print("Statistics for Cases!")
        self.cases_statistics()

if __name__ == '__main__':
    temp = CaseDigestClass("题目难度统计", '../JSON/test_data.json', "../OurModelOutPut/python_source"
                           , "../OurModelOutPut/Cases/")
    temp.all_cases()
