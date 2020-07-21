# -*- coding: utf-8 -*-
import os

import numpy as np
import csv

import sklearn
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

# class AhpClass:
#     __vector_container = []
#
#     '''
#     传入判断矩阵来构造
#     '''
#     def __init__(self, matrix):
#         # matrix为判断矩阵
#         self.matrix = matrix
#         self.row = len(matrix)
#         self.column = len(matrix[0])
#
#     '''
#     计算最大特征值即其对应的特征向量
#     '''
#     def get_eigenvalue_vector(self):
#         tmp = self.matrix
#         # 获得所有特征值和特征向量
#         value, vector = np.linalg.eig(tmp)
#         # 找到最大值
#         max_eigenvalue = np.max(value)
#         position = np.argmax(value)
#         eigen_vector = vector[:, position]
#         # print("最大特征值：" + str(maxEigenvalue) + "其特征向量" + str(eigen_vector))
#         return max_eigenvalue, eigen_vector
#
#     '''
#     测试一致性
#     :param max_eigenvalue: 最大特征值; RI: 随机一致性指标
#     :return: 返回是否一致
#     '''
#     def test_consistence(self, max_eigenvalue, RI):
#         CI = (max_eigenvalue - self.row) / (self.row - 1)
#         if RI == 0:
#             return True
#         else:
#             CR = CI / RI
#             if CR < 0.1:
#                 return True
#             else:
#                 return False
#
#     '''
#     生成RI对应的表，便于直接查找
#     '''
#     def generate_RI(self):
#         n1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
#         n2 = [0, 0, 0.58, 0.90, 1.12, 1.24, 1.32, 1.41, 1.45, 1.49, 1.51]
#         d = dict(zip(n1, n2))
#         return d[self.row]
#
#     '''
#     特征向量归一化
#     :param vector:最大特征值所对应的特征向量
#     :return: 归一化后的权向量
#     '''
#     def normalize(self, vector):
#         tmpvector = []
#         sum0 = np.sum(vector)
#         for i in range(len(vector)):
#             tmpvector.append(vector[i] / sum0)
#
#         return np.array(tmpvector)
#
#     '''
#     返回计算最后权重的学生数组的组合array
#     :return: 生成一个超级大的矩阵，其列数即为学生个数，行数为评判标准的个数
#     '''
#     def generate_calmatrix(self):
#         matrix_generate = np.vstack((self.__vector_container[0], self.__vector_container[1]))
#         for i in range(2, len(self.__vector_container)):
#             matrix_generate = np.vstack((matrix_generate, self.__vector_container[i]))
#         return matrix_generate.T


class PcaClass:
    userid = []
    caseid = []
    '''
    读取csv文件
    :param
    :return: 获得需要pca处理的np.array
    '''
    def read_csv(self):
        result = []
        with open("../OurModelOutPut/Cases/action_statistics.csv", 'r', encoding='utf-8') as f:
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
                    average_change = 0
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

    def output(self):
        path = '../OurModelOutPut/Cases/test_score.csv'
        with open(path, 'w', newline="") as f:
            writer = csv.writer(f)
            result = self.get_result()
            for line in result:
                writer.writerow(line)


if __name__ == '__main__':
    pca = PcaClass()
    pca.output()

    # x = np.linspace(-1,1,50)
    # y1 = x ** 2
    # y2 = 2*x+1
    #
    # plt.figure()
    # plt.plot(x,y2)
    # plt.plot(x,y1,color='red',linewidth=1.0,linestyle='--')
    #
    # plt.xlim((-1,2))
    # plt.ylim((0,3))
    # plt.xlabel("I am X")
    # plt.ylabel("I am Y")
    #
    # new_ticks = np.linspace(-1,2,5)
    # plt.xticks(new_ticks)
    # plt.yticks([-2,-1,0,1.22,3],[r"$awful$",r"$bad\ \alpha$",r'$common$',r'$good$',r'$nice$'])
    #
    # plt.show()


