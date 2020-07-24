# -*- coding: utf-8 -*-
import csv
import os
import numpy as np
'''
统计用户排位情况
'''
class Rank:
    def __init__(self, code_style_source, score_source, output):
        self.code_style_source = code_style_source
        self.score_source = score_source
        self.output = output
        if(not os.path.exists(output)):
            os.mkdir(output)

    def rank_code_style(self):
        '''
        统计编码风格分数排位
        :return:
        '''
        reader = csv.reader(open(self.code_style_source))
        user_code_styles = {}
        for line in reader:
            if(line[0] not in user_code_styles.keys()):
                user_code_styles[line[0]] = [line[3]]
            else:
                user_code_styles[line[0]].append(line[3])

        user_ranks = {}
        for user in user_code_styles.keys():
            user_ranks[user] = np.mean(list(map(float,user_code_styles[user])))

        user_code_styles.clear()

        self.__rank_output(user_ranks, "user_code_rank.csv", ["user_id", "average_score", "rank(percent)"])

    def rank_score(self):
        '''
        统计总评分排序、平均分排序和各部分排序
        :return:
        '''
        all_score = {}
        average_score = {}
        # category:{user_id:score}
        categories = {"排序算法": {}, "查找算法": {}, "图结构": {}, "树结构": {}, "数字操作": {},
                      "字符串": {}, "线性表": {}, "数组": {}}
        reader = csv.reader(open(self.score_source, encoding="utf-8"))
        next(reader)
        for line in reader:
            all_score[line[0]] = eval(line[1])
            average_score[line[0]] = eval(line[2])
            user_categories = eval(line[4])
            for category in user_categories.keys():
                categories[category][line[0]] = np.mean(user_categories[category])

        self.__rank_output(all_score, "all_score_rank.csv", ["user_id", "all_score", "rank(percent)"])
        self.__rank_output(average_score, "average_score_rank.csv", ["user_id", "average_score", "rank(percent)"])
        category_output = self.output +"/category"
        if(not os.path.exists(category_output)):
                os.mkdir(category_output)
        for category in categories:
            self.__rank_output(categories[category], "/category/" + category + "_rank.csv",
                               ["user_id", "average_score", "rank(percent)"])

    def __rank_output(self, my_dict, filename, title):
        '''
        输出排位
        :param my_dict: 字典 userid:分数
        :param filename: 输出文件名
        :param title: 输出文件的抬头
        :return:
        '''
        my_dict_keys = list(my_dict.keys())
        my_dict_keys.sort(key=lambda x: my_dict[x], reverse=True)
        with open(self.output + "/" + filename, 'w', newline="") as f:
            writer = csv.writer(f)
            writer.writerow(title)
            for i in range(len(my_dict_keys)):
                my_dict_key = my_dict_keys[i]
                writer.writerow([my_dict_key, my_dict[my_dict_key], self.__format_percent(i, len(my_dict_keys))])

    def __format_percent(self, now, total):
        my_rank = 100 - now/total*100.0
        return "%.2f" %(my_rank) + " %"

if __name__ == '__main__':
    rank = Rank("../OurModelOutPut/Users/user_result_0_36421.csv",
                "../OurModelOutPut/Result/all.csv",
                "../OurModelOutPut/Rank")
    rank.rank_score()