# -*- coding: utf-8 -*-
from OurModel import _0_RetrievePython
from OurModel import _1_FindValid
from OurModel import _2_Statisic
from OurModel import _2_UserCodeStyle
from OurModel import _3_Calculate
import time
import threading
import os

class Case_thread(threading.Thread):
    def __init__(self, name, source, python_source, csv_output, statistics_output):
        threading.Thread.__init__(self)
        self.name = name
        self.source = source
        self.python_source = python_source
        self.csv_output = csv_output
        self.statistics_output = statistics_output


    def run(self):
        start = time.time()
        print("开始线程{}:{}".format(self.name, self.time_format(start)))
        # 线程检查
        self.all()
        end = time.time()
        print("退出线程{}:{}".format(self.name, self.time_format(end)))
        duration = end - start

        print("线程{}共计用时{}".format(self.name,
                                  time.strftime("%M minutes %S seconds",time.localtime(duration))))

    def time_format(self, t):
        '''
        输入秒，格式化为字符串
        :param t:
        :return:
        '''
        struct_t = time.localtime(t)
        return time.strftime("%Y-%m-%d %H:%M:%S",struct_t)

    def all(self):
        '''
        完整处理一个块的预处理
        :param chunk_number: str
        :return:
        '''
        self.retrieve_python()
        self.valid_uploads()
        self.statistics()
        self.user_code_style_score()

    def retrieve_python(self):
        '''
        下载Python
        :param chunk_number:
        :return:
        '''
        print("Thread Name:{} begin retrieve python.".format(self.name))
        retrieve_python = _0_RetrievePython.RetrieveClass(self.name,
                                                          self.source, self.python_source)
        retrieve_python.retrieve_uploads()

    def valid_uploads(self):
        print("Thread Name:{} begin check valid uploads.".format(self.name))
        find_valid = _1_FindValid.FindValidClass(self.name,
                                                 self.python_source, self.source, self.csv_output)
        find_valid.findValid()

    def statistics(self):
        print("Thread Name:{} begin statistics.".format(self.name))
        my_statistics = _2_Statisic.StatisticsClass(self.name,
                                                    self.csv_output + "/detail.csv", self.statistics_output)
        my_statistics.my_statistics()

    def user_code_style_score(self):
        print("Thread Name:{} begin user code style statistics.".format(self.name))
        user_code_style = _2_UserCodeStyle.UserCodeStyle(self.name , self.csv_output, self.csv_output + "/detail.csv",
                                                         self.python_source)
        user_code_style.load_code_style()
        user_code_style.all_scores()
        self.__clear_py_cache()

    def __clear_py_cache(self):
        '''
        清楚所有的__pycache__的文件夹
        :return:
        '''
        user_ids = os.listdir(self.python_source)
        for user_id in user_ids:
            user_path = self.python_source + "/" + user_id
            case_ids = os.listdir(user_path)
            for case_id in case_ids:
                cache_path = user_path + "/" + case_id + "/__pycache__"
                if(os.path.exists(cache_path)):
                    self.__local_rm(cache_path)

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
                    self.__local_rm(filepath)
                else:
                    os.remove(filepath)
            os.rmdir(dirpath)

if __name__ == '__main__':
    case_thread = Case_thread("Case-Test", "./JSON_source/CaseTest.json","./python_source/",
                              "./CsvResult", "./Statistic/")
    case_thread.start()
    case_thread.join()
