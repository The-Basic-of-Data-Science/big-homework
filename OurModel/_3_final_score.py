# -*- coding: utf-8 -*-
import numpy as np
import csv
from sklearn.decomposition import PCA

'''
计算用户得分权重
'''


class GetWeightClass:

    userid = []
    caseid = []

    def __init__(self, source, output):
        self.source = source
        self.output = output
    '''
    读取csv文件
    :param
    :return: 获得需要pca处理的np.array
    '''
    def read_csv(self):
        result = []
        with open(self.source, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            n = 1
            for item in reader:
                tmp = []
                if n == 1:
                    n = 0
                    continue
                else:
                    self.userid.append(int(item[0])) # userid
                    self.caseid.append(int(item[1])) # caseid
                    tmp.append(100 / float(item[2])) # 提交次数的负相关
                    tmp.append(float(item[5])) # 最终得分
                    arr1 = item[3].split('|') # 每次提交的得分
                    arr2 = item[4].split('|') # 分数变化
                    tmp.append(float(arr1[0])) # 第一次得分

                    tmp1 = [] # 记录所有的分数变化(>0)
                    if float(arr1[0]) > 0:
                        tmp1.append(float(arr1[0]))

                    for item in arr2:
                        if item == '':
                            break
                        if float(item) > 0:
                            tmp1.append(float(item))

                    sum = 0
                    for i in tmp1:
                        sum += i

                    if len(tmp1) == 0:
                        average_change = 0
                    else:
                        average_change = sum / len(tmp1)
                    tmp.append(average_change)

                    result.append(tmp)

        a = np.array(result)
        f.close()
        return a

    '''
    读取csv文件
    :param
    :return: 经过pca降维处理的np.array
    '''
    def pca_method(self):
        pca = PCA(n_components=1)
        a = self.read_csv()
        new_a = pca.fit_transform(a)
        b = -1 * new_a + np.max(new_a)
        b = b / (np.max(b))
        return b

    def get_result(self):
        result1 = []
        tmp = self.pca_method()
        tmp1 = []
        tmp1.append("user_id")
        tmp1.append("case_id")
        tmp1.append("result")
        result1.append(tmp1)

        for i in range(len(self.userid)):
            tmp2 = []
            tmp2.append(self.userid[i])
            tmp2.append(self.caseid[i])
            tmp2.append(float(tmp[i]))
            result1.append(tmp2)

        return result1

    def get_weight(self):
        print("Start get Weight!")
        with open(self.output, 'w', newline="") as f:
            writer = csv.writer(f)
            result = self.get_result()
            for line in result:
                writer.writerow(line)
        print("Finish get Weight!")


if __name__ == '__main__':
    pca = GetWeightClass("../OurModelOutPut/Cases/action_statistics.csv",'../OurModelOutPut/Cases/test_score.csv')
    pca.get_weight()


