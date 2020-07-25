# -*- coding: utf-8 -*-
from OurModel import _2_Statisic
from OurModel import _3_Calculate
from OurModel import _3_User_Weight
from OurModel import _3_Case_Difficulty
from OurModel import _4_Rank
import os
import csv
from tqdm import tqdm
import json
import threading
import time

class VerifyClass(threading.Thread):
    def __init__(self, name, reserve, output):
        '''
        reserve是测试集块号
        :param reserve:
        :param output:
        '''
        threading.Thread.__init__(self)
        self.name = name
        self.reserve = reserve
        self.output = output + "without_" + str(reserve) + "/"
        self.chunk_user_ids = []

        if (not os.path.exists(output)):
            os.mkdir(output)

        if(not os.path.exists(self.output)):
            os.mkdir(self.output)

        if(not os.path.exists(self.output + "source/")):
            os.mkdir(self.output + "source/")

    def run(self):
        start = time.time()
        print("开始线程{}:{}".format(self.name, self.__time_format(start)))
        self.verify()
        end = time.time()
        print("退出线程{}:{}".format(self.name, self.__time_format(end)))
        duration = end - start

        print("线程{}共计用时{}".format(self.name,
                                  time.strftime("%M minutes %S seconds",time.localtime(duration))))

    def verify(self):
        self.__my_init()
        print("开始计算用户得分")
        calculator = _3_Calculate.Calculator(
            self.output + "source/part.json",
            self.output + "source/user_code_style.csv",
            self.output + "source/score_statistics.csv",
            self.output + "source/detail_without_" + str(self.reserve) +".csv",
            self.output + "source/valid.csv",
            self.output + "source/user_weight.csv",
            self.output + "Result.csv",
            self.output + "source/difficulty_center.csv"
        )
        calculator.all_user_score()
        # 拉取rank表
        if(not os.path.exists(self.output + "rank/")):
            os.mkdir(self.output + "rank/")
        rank = _4_Rank.Rank(self.output + "source/user_code_style.csv",
                    self.output + "Result.csv",
                    self.output + "rank/")
        rank.rank_score()
        # 清理
        self.__local_rm(self.output + "source/")

    def __my_init(self):
        print(self.name + " 合并所有的JSON文件,并统计用户ID")
        self.user_ids = []
        self.json_source = {}
        for x in tqdm(range(1, 20)):
            if (x == self.reserve):
                with open("../JSON_Chunk/ChunkJSON/test_data_" + str(self.reserve) + ".json") as f2:
                    txt = f2.read()
                    temp = json.loads(txt)
                    self.chunk_user_ids = list(temp.keys())
                continue
            with open("../JSON_Chunk/ChunkJSON/test_data_" + str(x) + ".json") as f2:
                txt = f2.read()
                temp = json.loads(txt)
                self.user_ids.extend(list(temp.keys()))
                for user_id in temp.keys():
                    self.json_source[user_id] = temp[user_id]

        with open(self.output + "source/part.json", 'w') as f:
            txt = json.dumps(self.json_source, indent=4)
            f.write(txt)
        self.json_source.clear()

        print(self.name + " 筛选编码风格分数情况")
        user_code_style_score = []
        with open("../OurModelOutPut/Users/user_result_0_36421.csv", 'r', encoding='utf-8') as f2:
            reader = csv.reader(f2)
            next(reader)
            for line in reader:
                if (line[0] in self.user_ids):
                    user_code_style_score.append(line)
        with open(self.output + "source/user_code_style.csv", 'w', newline = "", encoding="utf-8") as f:
            writer = csv.writer(f)
            for line in user_code_style_score:
                writer.writerow(line)

        print(self.name + " 合并所有的提交记录")
        uploads = [["user_id", "case_id", "case_type", "final_score",
                             "upload_id", "code_url", "upload_score", "upload_time"]]
        for x in tqdm(range(1, 20)):
            if (x == self.reserve):
                continue
            with open("../OurModelOutPut/python_source/test_data_" + str(x) + "/CsvResult/detail.csv",
                      'r', encoding="gb2312") as f1:
                reader = csv.reader(f1)
                next(reader)
                for line in reader:
                    uploads.append(line)

        with open(self.output + "source/detail_without_" + str(self.reserve) + ".csv"
                , 'w', newline="", encoding="gb2312") as f:
            writer = csv.writer(f)
            for line in uploads:
                writer.writerow(line)
        uploads.clear()

        print(self.name + " 统计题目信息")
        score_statistics = _2_Statisic.StatisticsClass(self.name,
                                                       self.output + "source/detail_without_" + str(self.reserve) + ".csv",
                                                       self.output + "source/")
        score_statistics.my_statistics()

        print(self.name + " 统计有效提交情况")
        valid_uploads = [["user_id", "case_id", "all_uploads_number",
                                 "valid_uploads_number", "valid_rate"]]
        with open("../OurModelOutPut/Valid/valid.csv", 'r', encoding='utf-8') as f2:
            reader = csv.reader(f2)
            next(reader)
            for line in reader:
                if (line[0] in self.user_ids):
                    valid_uploads.append(line)

        with open(self.output + "source/valid.csv", 'w', encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            for line in valid_uploads:
                writer.writerow(line)
        valid_uploads.clear()

        print(self.name + " 处理用户做题权重")
        user_weight = _3_User_Weight.GetWeightClass(self.output + "source/action_statistics.csv",
                                                    self.output + "source/user_weight.csv")
        user_weight.get_weight()
        print(self.name + " 计算分类中心情况")
        caseCalculator = _3_Case_Difficulty.CaseCalculator(self.output + "source/score_statistics.csv",
                                                           self.output + "source/difficulty_center.csv")
        caseCalculator.pre_get_raw_difficulty_centers()


    def __time_format(self, t):
        '''
        输入秒，格式化为字符串
        :param t:
        :return:
        '''
        struct_t = time.localtime(t)
        return time.strftime("%Y-%m-%d %H:%M:%S",struct_t)

    def __local_rm(self, dirpath):
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

if __name__ == '__main__':
    chunk_number = 18
    thread = VerifyClass(str(chunk_number) + "号交叉检验法", chunk_number, "./VerifyOutPut/")
    thread.start()
    thread.join()