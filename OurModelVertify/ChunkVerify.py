# -*- coding: utf-8 -*-
from OurModel import _2_Statisic
from OurModel import _3_Calculate
from OurModel import _3_User_Weight
from OurModel import _3_Case_Difficulty
import os
import csv
from tqdm import tqdm
import json
import threading
import time

class VerifyClass(threading.Thread):
    def __init__(self, name, reserve, output):
        '''
        reserve鏄笉鍙傚姞璁＄畻鐨勯儴鍒�
        :param reserve:
        :param output:
        '''
        threading.Thread.__init__(self)
        self.name = name
        self.reserve = reserve
        self.output = output + "without_" + str(reserve) + "/"

        if(not os.path.exists(self.output)):
            os.mkdir(self.output)

        if(not os.path.exists(self.output + "source/")):
            os.mkdir(self.output + "source/")

    def __my_init(self):
        print(self.name + " 鍚堝苟鎵�鏈夌殑JSON鏂囦欢,骞剁粺璁＄敤鎴稩D")
        self.user_ids = []
        self.json_source = {}
        for x in tqdm(range(1, 20)):
            if (x == self.reserve):
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

        print(self.name + " 鍚堝苟鎵�鏈夌殑鎻愪氦璁板綍")
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

        print(self.name + " 缁熻棰樼洰淇℃伅")
        score_statistics = _2_Statisic.StatisticsClass(self.name,
                                                       self.output + "source/detail_without_" + str(self.reserve) + ".csv",
                                                       self.output + "source/")
        score_statistics.my_statistics()

        print(self.name + " 缁熻鏈夋晥鎻愪氦鎯呭喌")
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

        print(self.name + " 澶勭悊鐢ㄦ埛鍋氶鏉冮噸")
        user_weight = _3_User_Weight.GetWeightClass(self.output + "source/action_statistics.csv",
                                                    self.output + "source/user_weight.csv")
        user_weight.get_weight()
        print(self.name + " 璁＄畻鍒嗙被涓績鎯呭喌")
        caseCalculator = _3_Case_Difficulty.CaseCalculator(self.output + "source/score_statistics.csv",
                                                           self.output + "source/difficulty_center.csv")
        caseCalculator.pre_get_raw_difficulty_centers()

    def run(self):
        start = time.time()
        print("寮�濮嬬嚎绋媨}:{}".format(self.name, self.__time_format(start)))
        self.verify()
        end = time.time()
        print("閫�鍑虹嚎绋媨}:{}".format(self.name, self.__time_format(end)))
        duration = end - start

        print("绾跨▼{}鍏辫鐢ㄦ椂{}".format(self.name,
                                  time.strftime("%M minutes %S seconds",time.localtime(duration))))

    def __time_format(self, t):
        '''
        杈撳叆绉掞紝鏍煎紡鍖栦负瀛楃涓�
        :param t:
        :return:
        '''
        struct_t = time.localtime(t)
        return time.strftime("%Y-%m-%d %H:%M:%S",struct_t)

    def verify(self):
        self.__my_init()
        print("寮�濮嬭绠楃敤鎴峰緱鍒�")
        calculator = _3_Calculate.Calculator(
            self.output + "source/part.json",
            "../OurModelOutPut/Users/user_result_0_36421.csv",
            self.output + "source/score_statistics.csv",
            self.output + "source/detail_without_" + str(self.reserve) +".csv",
            self.output + "source/valid.csv",
            self.output + "source/user_weight.csv",
            self.output + "Result.csv",
            self.output + "source/difficulty_center.csv"
        )
        calculator.all_user_score()
        # 娓呯悊鎺�
        self.__local_rm(self.output + "source/")

    def __local_rm(self, dirpath):
        '''
        閫掑綊鍒犻櫎瀵瑰簲鐩綍涓嬫墍鏈夌殑鏂囦欢
        :param dirpath:鐩爣鐩綍
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
    basic_path = "./VerifyOutPut/"
    if(not os.path.exists(basic_path)):
        os.mkdir(basic_path)
    chunk_number = 19
    thread = VerifyClass(str(chunk_number) + "鍙蜂氦鍙夋楠屾硶", chunk_number, basic_path)
    thread.start()
    thread.join()