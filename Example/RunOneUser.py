# -*- coding: utf-8 -*-
from OurModel import _0_RetrievePython
from OurModel import _1_FindValid
from OurModel import _2_Statisic
from OurModel import _2_UserCodeStyle
from OurModel import _2_Valid
from OurModel import _3_Calculate
from matplotlib import pyplot as plt
import matplotlib
import numpy as np
import time
import threading
import os
import csv
import json

class Case_thread(threading.Thread):
    def __init__(self, name, user_id):
        threading.Thread.__init__(self)
        self.name = name
        self.source = "./" + str(user_id) + "/JSON_source/" + str(user_id) + ".json"
        self.python_source = "./" + str(user_id) + "/python_source/"
        self.valid_output = "./" + str(user_id) + "/Valid_Uploads"
        self.statistics_output = "./" + str(user_id) + "/Statistic/"
        self.result_output = "./" + str(user_id) + "/Result/"
        self.graph_output = "./" + str(user_id) + "/Graph/"
        self.user_code_output = "./" + str(user_id) + "/User_Code_Style/"
        self.result = []

        # 从源文件中切割保存用户JSON
        with open("../JSON/test_data.json", 'r', encoding="utf-8") as f:
            txt = f.read()
            users = json.loads(txt)
            if(user_id not in users.keys()):
                return
            user = json.dumps({user_id:users[user_id]}, indent=4)

        # 如果没有的话就初始化目录
        if (not os.path.exists("./" + str(user_id))):
            os.mkdir("./" + str(user_id))
        if(not os.path.exists("./" + str(user_id) + "/JSON_source/")):
            os.mkdir("./" + str(user_id) + "/JSON_source/")

        with open(self.source, 'w', encoding="utf-8") as f2:
            f2.write(user)

    def run(self):
        start = time.time()
        print("开始线程{}:{}".format(self.name, self.__time_format(start)))
        self.__all()
        end = time.time()
        print("退出线程{}:{}".format(self.name, self.__time_format(end)))
        duration = end - start

        print("线程{}共计用时{}".format(self.name,
                                  time.strftime("%M minutes %S seconds",time.localtime(duration))))

    def __all(self):
        '''
        完整处理一个块的预处理
        :param chunk_number: str
        :return:
        '''

        if(not os.path.exists(self.source)):
            print("没有找到这个用户")
            return
        self.__retrieve_python()
        self.__valid_uploads()
        self.__statistics()
        self.__user_code_style_score()
        self.__user_valid()
        self.__user_score()
        self.__rank()

    def __time_format(self, t):
        '''
        输入秒，格式化为字符串
        :param t:
        :return:
        '''
        struct_t = time.localtime(t)
        return time.strftime("%Y-%m-%d %H:%M:%S",struct_t)

    def __retrieve_python(self):
        '''
        下载Python
        :param chunk_number:
        :return:
        '''
        print("Thread Name:{} begin retrieve python.".format(self.name))
        retrieve_python = _0_RetrievePython.RetrieveClass(self.name,
                                                          self.source, self.python_source)
        retrieve_python.retrieve_uploads()
        print("Thread Name:{} finish retrieve python.".format(self.name))

    def __valid_uploads(self):
        '''
        检查所有的有效提交情况
        :return:
        '''
        print("Thread Name:{} begin check valid uploads.".format(self.name))
        find_valid = _1_FindValid.FindValidClass(self.name,
                                                 self.python_source, self.source, self.valid_output)
        find_valid.findValid()
        print("Thread Name:{} finish check valid uploads.".format(self.name))

    def __statistics(self):
        '''
        统计题目信息和用户行为数据
        :return:
        '''
        print("Thread Name:{} begin statistics.".format(self.name))
        my_statistics = _2_Statisic.StatisticsClass(self.name,
                                                    self.valid_output + "/detail.csv", self.statistics_output)
        my_statistics.my_statistics()
        print("Thread Name:{} finish statistics.".format(self.name))

    def __user_code_style_score(self):
        '''
        计算用户的有效提交的编码风格分数
        :return:
        '''
        print("Thread Name:{} begin user code style statistics.".format(self.name))
        user_code_style = _2_UserCodeStyle.UserCodeStyle(self.name , self.user_code_output, self.valid_output + "/detail.csv",
                                                         self.python_source)
        if(not os.path.exists(self.user_code_output)):
            os.mkdir(self.user_code_output)
        user_code_style.load_code_style()
        user_code_style.all_scores()
        self.__clear_py_cache()
        print("Thread Name:{} finish user code style statistics.".format(self.name))

    def __user_valid(self):
        print("Thread Name:{} begin user valid status.".format(self.name))
        valid_check = _2_Valid.ValidCheck(self.source, self.valid_output + "/detail.csv", self.valid_output)
        user_valid_result = valid_check.user_valid()
        user_valid_result.insert(0, ['user_id', 'case_id', 'all_uploads_number', 'valid_uploads_number', 'valid_rate'])
        with open(self.valid_output + "/valid.csv", 'w', newline="") as f:
            writer = csv.writer(f)
            for line in user_valid_result:
                writer.writerow(line)
        print("Thread Name:{} finish user valid status.".format(self.name))

    def __user_score(self):
        '''
        获取用户的最终的得分
        :return:
        '''
        print("Thread Name:{} begin user score digest.".format(self.name))
        calculator = _3_Calculate.Calculator(
            self.source,
            self.user_code_output + "/user_result_" + self.name + ".csv",
            self.statistics_output + "score_statistics.csv",
            "../OurModelOutPut/Cases/cases_detail.csv",
            self.valid_output + "/valid.csv",
            "../OurModelOutPut/Cases/user_weight.csv",
            self.result_output + "/user_score.csv",
            '../OurModelOutPut/Cases/difficulty_center.csv'
        )
        print("Thread Name:{} end user score digest.".format(self.name))
        self.result = calculator.all_user_score()

    def __rank(self):
        if(not os.path.exists(self.graph_output)):
            os.mkdir(self.graph_output)

        # 整体分数情况统计
        user_code_style_score = []
        reader = csv.reader(open(self.user_code_output + "/user_result_" + self.name + ".csv"
                                 , 'r', encoding="utf-8"))
        for line in reader:
            user_code_style_score.append(float(line[3]))
        user_code_style_rank = self.__rank_search(np.mean(user_code_style_score),
                                                  "../OurModelOutPut/Rank/user_code_rank.csv")
        user_code_style_score.clear()

        # line:"用户编号", "作业完成情况", "总评分", "每题综合分的字典", "每一类题的综合分的数组"
        line = self.result[0]
        all_score_rank = self.__rank_search(float(line[1]), "../OurModelOutPut/Rank/all_score_rank.csv")
        average_score_rank = self.__rank_search(float(line[2]), "../OurModelOutPut/Rank/average_score_rank.csv")

        result = {"编码风格排位": user_code_style_rank, "总分数排位": all_score_rank, "平均分排位": average_score_rank}
        total_labels = list(result.keys())

        print(self.name + " 用户编码风格排位：" + str(user_code_style_rank) + "%")
        print(self.name + " 用户总分排位：" + str(all_score_rank) + "%")
        print(self.name + " 用户均分排位：" + str(average_score_rank) + "%")

        user_id = line[0]
        # 绘制雷达图
        labels = np.array(["排序算法", "查找算法", "图结构", "树结构", "数字操作", "字符串", "线性表", "数组"])
        data = np.zeros([8,1])
        for i in range(len(labels)):
            if(labels[i] in line[4].keys()):
                data[i] = self.__rank_search(np.mean(line[4][labels[i]]),
                                             "../OurModelOutPut/Rank/Category/" + labels[i] + "_rank.csv")
                print(self.name + " 用户" + labels[i] + "排位：" + str(data[i][0]) + "%")
        # 设置字体
        matplotlib.rcParams['font.family'] = 'SimHei'
        matplotlib.rcParams['font.sans-serif'] = ['SimHei']
        # 设置维度
        nAttr = len(labels)
        # 计算角度
        angles = np.linspace(0, 2 * np.pi, nAttr, endpoint=False)
        # 保证需要闭合，数据和角度
        data = np.array(data)
        data = np.concatenate((data, [data[0]]))
        angles = np.concatenate((angles, [angles[0]]))
        # 开始制图
        plt.subplot(111, polar=True)
        # 划线
        # total_labels.sort(key=lambda x: result[x])
        plt.plot(angles, data, 'bo-', color='#6a005f', linewidth=2)
        # 从左到右，绿色 褐色 红色
        colors = [ '#00FF00', '#808000', '#FF0000']
        for i in range(len(total_labels)):
            # 画标准线
            total_label = total_labels[i]
            temp = []
            for x in range(9):
                temp.append(result[total_label])
            plt.plot(angles, np.array(temp), color=colors[i], linewidth=1.5, label=total_label)
        # 绘制阴影
        plt.fill(angles, data, facecolor='#6a005f', alpha=0.25)
        plt.thetagrids(angles * 180 / np.pi, labels)
        plt.title(str(user_id) + '号用户各类题目排位图(单位:%)', pad=15)
        # 开启图例
        plt.legend(loc='lower left', bbox_to_anchor=(0.95,0))
        plt.savefig(self.graph_output + str(user_id) + "_rank.jpg")
        plt.show()

    def __rank_search(self,my_score, target_file):
        '''
        获取排名信息
        :param my_score: 我的分数
        :param target_file: 查找分数的文件
        :return:
        '''
        reader = csv.reader(open(target_file, encoding="utf-8"))
        next(reader)
        result = "100 %"
        for line in reader:
            result = line[2]
            if(my_score >= eval(line[1])):
                break
        return float(result.split(" ")[0])

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

# 推荐使用这两位用户 60778 60725
if __name__ == '__main__':
    user_id = "60825"
    case_thread = Case_thread("User-" + user_id, user_id)
    case_thread.start()
    case_thread.join()
