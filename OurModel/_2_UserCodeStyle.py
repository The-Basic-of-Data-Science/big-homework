# -*- coding: utf-8 -*-
from pylint import epylint as lint
from tqdm import tqdm
import re
import csv
import os
import threading
import time

class UserCodeStyle:
    def __init__(self, name, output, detail_csv, python_origin):
        self.name = name
        self.output = output
        self.code_style = self.output + "/code_style_" + self.name + ".csv"
        self.detail_csv = detail_csv
        self.python_origin = python_origin
        self.userResult = []
        self.origin = []

    def get_score(self, path):
        '''
        计算出路径指向的位置的用户的成绩
        :param path:
        :return:
        '''
        (pylint_stdout, pylint_stderr) = lint.py_run(path, return_std=True)

        pylint_stdout.seek(0)
        stdout = []
        while True:
            strBuf = pylint_stdout.readline()
            if strBuf == "":
                break
            stdout.append(strBuf.strip())
        stdout = '\n'.join(stdout)
        matchObj = re.search('Your code has been rated at (.*)/10', stdout)

        if (matchObj == None):
            score = -1
        else:
            score = eval(matchObj.group(0).split("/")[0].split(" ")[-1])
        return score

    def load_code_style_score(self, path):
        '''
        将用户的需要被统计成绩的部分保存起来
        :param path:
        :return:
        '''
        if(path == ""):
            return
        user_id = path.split("/")[-3]
        case_id = path.split("/")[-2]
        upload_id = path.split("/")[-1].split("_")[0]
        self.userResult.append([user_id, case_id, upload_id, path])

    def list_to_csv(self, filename,  data):
        '''
        将source中的数据格式化到${self.output}中的filename去
        :param filename: 文件名
        :param source: 源文件
        :param output: 输出文件夹
        :return:
        '''
        if(not os.path.exists(self.output)):
            os.makedirs(self.output)
        with open(self.output + "/" + filename + ".csv",'w',newline="") as f:
            writer = csv.writer(f)
            for br in data:
                if(len(br) != 0 and len(br[0]) != 0):
                    writer.writerow(br)

    def load_code_style(self):
        '''
        计算所有的用户编码风格分数
        :return:
        '''
        # 清理code_style文件
        with open(self.code_style,'w') as f:
            print("Clear Output!")

        with open(self.detail_csv, 'r') as f:
            reader = csv.reader(f)
            user_id = -1
            case_id = -1
            user_score = -1
            user_path = ""
            for line in reader:
                if(line[0] == "user_id"):
                    continue
                if(user_id != eval(line[0]) or case_id != eval(line[1])):
                    user_id = eval(line[0])
                    case_id = eval(line[1])
                    user_score = eval(line[3])
                    self.load_code_style_score(user_path)
                    pys = os.listdir(self.python_origin + line[0] + "/" + line[1])
                    for py in pys:
                        if (py.startswith(line[4] + "_result")):
                            user_path = self.python_origin + line[0] + "/" + line[1] + "/" + py
                else:
                    if(eval(line[3]) >= user_score):
                        user_score = eval(line[3])
                        pys = os.listdir(self.python_origin + line[0] + "/" + line[1])
                        for py in pys:
                            if(py.startswith(line[4] + "_result")):
                                user_path = self.python_origin + line[0] + "/" + line[1] + "/" + py
        self.load_code_style_score(user_path)
        self.list_to_csv("code_style_" + self.name, self.userResult)

    # 之后计算答案和结果的部分

    def all_scores(self):
        '''
        获取所有的结果
        :param start: 包含
        :param end: 不含
        :return:
        '''
        self.init()
        after_results = []
        for temp in tqdm(self.origin):
            score = self.get_score(temp[-1])
            after_result = [temp[0], temp[1], temp[2], score]
            after_results.append(after_result)
        self.list_to_csv("user_result_" + self.name, after_results)

    def init(self):
        cnt = 0
        with open(self.code_style, 'r') as f:
            reader = csv.reader(f)
            for line in tqdm(reader):
                cnt += 1
                temp = [line[0], line[1], line[2], line[3]]
                self.origin.append(temp)

class user_code_thread(threading.Thread):
    def __init__(self, thread_id, name, chunk):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.chunk = chunk

    def run(self):
        start = time.time()
        print("开始线程{}:{}".format(self.name, self.time_format(start)))
        # 线程检查
        source = "../OurModelOutPut/python_source"
        userCodeStyle = UserCodeStyle(str(self.chunk), "../OurModelOutPut/Users" ,
                                      source + "/test_data_" + str(self.chunk) + "/CsvResult/detail.csv",
                                      source + "/test_data_" + str(self.chunk) + "/Python/")
        userCodeStyle.load_code_style()
        userCodeStyle.all_scores()
        finish = time.time()
        print("退出线程{}:{}".format(self.name, self.time_format(finish)))
        duration = finish - start
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

def start_thread_group(chunk_numbers):
    '''
    处理从chunk_start(含)到chunk_end(含),100个一块
    :param chunk_start:
    :param chunk_end:
    :return:
    '''
    thread_group = []
    for chunk_number in chunk_numbers:
        thread = user_code_thread(chunk_number, "Thread-" + str(chunk_number), chunk_number)
        thread_group.append(thread)
        thread.start()
    for thread in thread_group:
        thread.join()
    # 如果没有出现这句话请再次运行main.py
    print("退出主线程")

def __unit(start, end):
    '''
    合并结果仅仅在类内部使用
    :param start:
    :param end:
    :return:
    '''
    path = "../OurModelOutPut/Users"
    listdirs = os.listdir(path)
    temp = []
    for listdir in listdirs:
        if(listdir == "code_style.csv" or (not listdir.endswith(".csv"))):
            continue
        with open(path + "/" + listdir, 'r') as f:
            reader = csv.reader(f)
            for line in reader:
                temp.append(line)
    if(not os.path.exists(path + "/union")):
        os.makedirs(path + "/union")
    with open(path + "/union/user_result_" + str(start) + "_" + str(end) + ".csv",'w',newline="") as f2:
        writer = csv.writer(f2)
        for line in temp:
            writer.writerow(line)

if __name__ == '__main__':
    start_thread_group([x for x in range(1, 2)])
    print("Finish!")

