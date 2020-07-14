# -*- coding: utf-8 -*-
from pylint import epylint as lint
from tqdm import tqdm
import re
import csv
import os

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

    def all_scores(self):
        # TODO
        result = []
        with open(self.output + "/code_style.csv", 'r') as f:
            reader = csv.reader(f)
            for line in tqdm(reader):
                temp = [line[0], line[1]]
                temp.append(self.get_score(line[2]))
        self.list_to_csv("user_result", result)


if __name__ == '__main__':
    userCodeStyle = UserCodeStyle("用户编码风格分数生成", "../OurModelOutPut/python_source"
                                  , "../OurModelOutPut/Users")
    userCodeStyle.load_chunks_code_style()