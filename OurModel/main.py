# -*- coding: utf-8 -*-
from OurModel import _0_RetrievePython
from OurModel import _1_FindValid
from OurModel import _2_Statisic
import time
import threading
import os
from tqdm import tqdm

class chunk_thread(threading.Thread):
    def __init__(self, thread_id, name, chunk_number):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.chunk_number = chunk_number
        self.source = '../JSON_chunk/ChunkJSON/test_data_' + chunk_number + '.json'
        self.python_source = '../OurModelOutPut/python_source/test_data_' + chunk_number + '/Python/'
        self.valid_csv_output = '../OurModelOutPut/python_source/test_data_' + chunk_number + '/CsvResult'
        self.statistics_output = '../OurModelOutPut/python_source/test_data_' + chunk_number + '/Statistic/'

    def run(self):
        start = time.time()
        print("开始线程{}:{}".format(self.name, self.time_format(start)))
        # 线程检查
        self.chunk_valid()
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


    def chunk_all(self):
        '''
        完整处理一个块的预处理
        :param chunk_number: str
        :return:
        '''
        self.chunk_retrieve()
        self.chunk_valid()
        self.chunk_statistics()

    def chunk_retrieve(self):
        '''
        下载Python
        :param chunk_number:
        :return:
        '''
        print("chunk_number:{}".format(self.chunk_number))
        retrieve_python = _0_RetrievePython.RetrieveClass(self.chunk_number,
                                                          self.source, self.python_source)
        retrieve_python.retrieve_uploads()

    def chunk_valid(self):
        print("chunk_number:{}".format(self.chunk_number))
        find_valid = _1_FindValid.FindValidClass(self.chunk_number,
                                                 self.python_source, self.source, self.valid_csv_output)
        find_valid.findValid()

    def chunk_statistics(self):
        print("chunk_number:{}".format(self.chunk_number))
        my_statistics = _2_Statisic.StatisticsClass(self.chunk_number,
                                                    self.valid_csv_output + "/detail.csv", self.statistics_output)
        my_statistics.my_statistics()

def start_thread_group(chunk_numbers):
    '''
    处理从chunk_start(含)到chunk_end(含)
    :param chunk_start:
    :param chunk_end:
    :return:
    '''
    thread_group = []
    for chunk_number in chunk_numbers:
        thread = chunk_thread(chunk_number, "Thread-" + str(chunk_number), str(chunk_number))
        thread_group.append(thread)
        thread.start()
    for thread in thread_group:
        thread.join()
    # 如果没有出现这句话请再次运行main.py
    print("退出主线程")

def clear_py_cache():
    '''
    清楚所有的__pycache__的文件夹
    :return:
    '''
    path = '../OurModelOutPut/python_source'
    chunks = os.listdir(path)
    for chunk in tqdm(chunks):
        users_path = path + "/" + chunk + "/Python"
        user_ids = os.listdir(users_path)
        for user_id in user_ids:
            user_path = users_path + "/" + user_id
            case_ids = os.listdir(user_path)
            for case_id in case_ids:
                cache_path = user_path + "/" + case_id + "/__pycache__"
                if(os.path.exists(cache_path)):
                    local_rm(cache_path)

def local_rm(dirpath):
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
                local_rm(filepath)
            else:
                os.remove(filepath)
        os.rmdir(dirpath)

if __name__ == '__main__':
    # 建议一次执行偶数个线程
    # start_thread_group([x for x in range(1,20)])
    # start_thread_group([8, 9])
    clear_py_cache()