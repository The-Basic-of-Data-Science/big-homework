# -*- coding: utf-8 -*-
from OurModel import _0_retrievePython
from OurModel import _1_findValid
from OurModel import _2_statics
import time
import threading

'''
下载
'''
class chunk_thread(threading.Thread):
    def __init__(self, threadID, name, chunkNumber):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.chunkNumber = chunkNumber
        self.source = '../JSON_chunk/ChunkJSON/test_data_' + chunkNumber + '.json'
        self.python_source = '../OurModelOutPut/test_data_' + chunkNumber + '/Python/'
        self.valid_csv_output = '../OurModelOutPut/test_data_' + chunkNumber + '/CsvResult'
        self.statistics_output = '../OurModelOutPut/test_data_' + chunkNumber + '/Statistic/'

    def run(self):
        start = time.time()
        print("开始线程{}:{}".format(self.name, time_format(start)))
        # 线程执行下载
        download = _0_retrievePython.RetrieveClass(self.chunkNumber, self.source, self.python_source)
        download.retrieve_uploads()
        # chunk_digest(self.chunkNumber)
        end = time.time()
        print("退出线程{}:{}".format(self.name, time_format(end)))
        duration = end - start

        print("线程{}共计用时{}".format(self.name,
                                  time.strftime("%M minutes %S seconds",time.localtime(duration))))

def time_format(t):
    '''
    输入秒，格式化为字符串
    :param t:
    :return:
    '''
    struct_t = time.localtime(t)
    return time.strftime("%Y-%m-%d %H:%M:%S",struct_t)

def chunk_digest(chunk_number):
    '''
    完整处理一个块的预处理
    :param chunk_number: str
    :return:
    '''
    print("chunk_number:{}".format(chunk_number))
    source = '../JSON_chunk/ChunkJSON/test_data_' + chunk_number + '.json'
    python_source = '../OurModelOutPut/test_data_' + chunk_number + '/Python/'
    valid_csv_output = '../OurModelOutPut/test_data_' + chunk_number + '/CsvResult'
    statistics_output = '../OurModelOutPut/test_data_' + chunk_number + '/Statistic/'
    retrieve_python = _0_retrievePython.RetrieveClass(chunk_number,
                                                   source, python_source)
    retrieve_python.retrieve_uploads()
    print("chunk_number:{}".format(chunk_number))
    find_valid = _1_findValid.FindValidClass(chunk_number,
                                            python_source, source, valid_csv_output)
    find_valid.findValid()
    print("chunk_number:{}".format(chunk_number))
    my_statistics = _2_statics.StatisticsClass(chunk_number,
                                              valid_csv_output + "/detail.csv", statistics_output)
    my_statistics.my_statistics()

def startThreeThread(chunk_1, chunk_2, chunk_3):
    '''
    处理三个块
    :param chunk_1: int
    :param chunk_2: int
    :param chunk_3: int
    :return:
    '''
    chunkThread1 = chunk_thread(chunk_1, "Thread-" + str(chunk_1), str(chunk_1))
    chunkThread2 = chunk_thread(chunk_2, "Thread-" + str(chunk_2), str(chunk_2))
    chunkThread3 = chunk_thread(chunk_3, "Thread-" + str(chunk_3), str(chunk_3))
    chunkThread1.start()
    chunkThread2.start()
    chunkThread3.start()
    chunkThread1.join()
    chunkThread2.join()
    chunkThread3.join()
    print("退出主线程")

if __name__ == '__main__':
    # startThreeThread(5, 6, 7)
    chunkThread = chunk_thread(5, "Thread-" + str(5), str(5))
    chunkThread.start()
    chunkThread.join()
    print("退出主线程")