# -*- coding: utf-8 -*-
from pylint import epylint as lint
from tqdm import tqdm
import re
import csv
import os
import threading
import time

# 全局
result = []

class UserCodeStyle:
    def __init__(self, name, source, output):
        self.name = name
        self.source = source
        self.output = output
        self.userResult = []

    def get_score(self, path):
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
        if(path == ""):
            return
        user_id = path.split("/")[-3]
        case_id = path.split("/")[-2]
        upload_id = path.split("/")[-1].split("_")[0]
        self.userResult.append([user_id, case_id, upload_id, path])

    def list_to_csv(self, filename,  data):
        '''
        将source中的数据格式化到CsvResult/filename.csv中去
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

    def load_chunks_code_style(self):
        if(not os.path.exists(self.source)):
            print("Not Find Source!")
            return
        # 清理code_style文件
        with open(self.output + "/code_style.csv",'w') as f:
            print("Clear Output!")
        chunks = os.listdir(self.source)
        for chunk in tqdm(chunks):
            self.load_csv_code_style(chunk)

    def load_csv_code_style(self, chunk):
        path = self.source + "/" + chunk + "/CsvResult/detail.csv"
        with open(path, 'r') as f:
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
                    pys = os.listdir(self.source + "/" + chunk + "/Python/" + line[0] + \
                                     "/" + line[1])
                    for py in pys:
                        if (py.startswith(line[4] + "_result")):
                            user_path = self.source + "/" + chunk + "/Python/" + line[0] + \
                                        "/" + line[1] + "/" + py
                else:
                    if(eval(line[3]) >= user_score):
                        user_score = eval(line[3])
                        pys = os.listdir(self.source + "/" + chunk + "/Python/" + line[0] + \
                                    "/" + line[1])
                        for py in pys:
                            if(py.startswith(line[4] + "_result")):
                                user_path = self.source + "/" + chunk + "/Python/" + line[0] + \
                                    "/" + line[1] + "/" + py
        self.load_code_style_score(user_path)
        self.list_to_csv("code_style", self.userResult)

    def all_scores(self, start, end):
        '''
        获取所有的结果
        :param start: 包含
        :param end: 不含
        :return:
        '''
        if(end > len(result)):
            end = len(result)
        temp_results = result[start : end]
        after_results = []
        for temp_result in tqdm(temp_results):
            score = self.get_score(temp_result[-1])
            after_result = [temp_result[0], temp_result[1], temp_result[2], score]
            after_results.append(after_result)
        self.list_to_csv("user_result_" + str(start) + "_" + str(end), after_results)

class user_code_thread(threading.Thread):
    def __init__(self, thread_id, name, begin, end):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.begin = begin
        self.end = end

    def run(self):
        start = time.time()
        print("开始线程{}:{}".format(self.name, self.time_format(start)))
        # 线程检查
        userCodeStyle = UserCodeStyle("用户编码风格分数生成", "../OurModelOutPut/python_source"
                                      , "../OurModelOutPut/Users")
        userCodeStyle.all_scores(self.begin, self.end)
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
    init()
    thread_group = []
    for chunk_number in chunk_numbers:
        thread = user_code_thread(chunk_number, "Thread-" + str(chunk_number)
                                  , 100 * chunk_number, 100*(chunk_number + 1))
        thread_group.append(thread)
        thread.start()
    for thread in thread_group:
        thread.join()
    # 如果没有出现这句话请再次运行main.py
    print("退出主线程")

def init():
    cnt = 0
    with open("../OurModelOutPut/Users/code_style.csv", 'r') as f:
        reader = csv.reader(f)
        for line in tqdm(reader):
            cnt += 1
            temp = [line[0], line[1], line[2], line[3]]
            result.append(temp)

def unit(start, end):
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

def isfind(line, data):
    for temp in data:
        if(line[0] == temp[0] and line[1] == temp[1]):
            return True
    return False

def check_code_style():
    '''
    用来检查是否有遗漏的部分
    :return:
    '''
    init()
    data = []
    not_find = []
    with open("../OurModelOutPut/Users/user_result_0_36421.csv", 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for line in reader:
            data.append(line)
    for line in tqdm(result):
        if(not isfind(line, data)):
            not_find.append(line)
    with open('../OurModelOutPut/Users/user_result_left.csv', 'w', newline="") as f2:
        writer = csv.writer(f2)
        for line in not_find:
             writer.writerow(line)

if __name__ == '__main__':
    # 一个Thread一次统计1000个
    # start_thread_group([x for x in range(0, 1)])
    # unit(0, 36421)
    check_code_style()

