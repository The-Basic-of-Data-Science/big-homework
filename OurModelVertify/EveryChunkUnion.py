# -*- coding: utf-8 -*-
import os
import csv
import numpy as np
from tqdm import tqdm

class EveryChunkUnionClass:
    def __init__(self, source, output):
        self.source = source
        self.output = output
        # user_id,type(all|average|category) -> [ranks]
        self.result = {}

        if(not os.path.exists(output)):
            os.mkdir(output)

    def union(self):
        self.__union_one("../OurModelOutPut/Result/all.csv")
        for x in tqdm(range(1, 20)):
            self.__union_one("./VerifyOutPut/without_" + str(x) + "/Result.csv")
        with open(self.output + "ranks_result.csv", 'w', encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            for key in self.result.keys():
                temp = key.split(",")
                temp.extend(self.result[key])
                writer.writerow(temp)

    def __union_one(self, filename):
        lines = csv.reader(open(filename, 'r', encoding="utf-8"))
        next(lines)
        for line in lines:
            # line: 用户编号,作业完成情况,总评分,每题综合分的字典,每一类题的综合分的数组
            key = ','.join([line[0],'all'])
            all_rank = self.__rank_search(float(line[1]), "../OurModelOutPut/Rank/all_score_rank.csv")
            if(key not in self.result.keys()):
                self.result[key] = [all_rank]
            else:
                self.result[key].append(all_rank)

            key = ','.join([line[0], 'average'])
            average_rank = self.__rank_search(float(line[2]), "../OurModelOutPut/Rank/average_score_rank.csv")
            if (key not in self.result.keys()):
                self.result[key] = [average_rank]
            else:
                self.result[key].append(average_rank)

            categories = ["排序算法", "查找算法", "图结构", "树结构", "数字操作", "字符串", "线性表", "数组"]
            user_categories = eval(line[4])
            for category in categories:
                if(category not in user_categories.keys()):
                    continue
                key = ','.join([line[0], category])
                category_rank = self.__rank_search(np.mean(user_categories[category]),
                                                   "../OurModelOutPut/Rank/Category/" + category + "_rank.csv")
                if (key not in self.result.keys()):
                    self.result[key] = [category_rank]
                else:
                    self.result[key].append(category_rank)


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

if __name__ == '__main__':
    chunk_union = EveryChunkUnionClass("./VerifyOutPut/", "./VerifyUnion/")
    chunk_union.union()

