# -*- coding: utf-8 -*-
import numpy as np


class AhpClass:
    __vector_container = []

    '''
    传入判断矩阵来构造
    '''
    def __init__(self, matrix):
        # matrix为判断矩阵
        self.matrix = matrix
        self.row = len(matrix)
        self.column = len(matrix[0])

    '''
    计算最大特征值即其对应的特征向量
    '''
    def get_eigenvalue_vector(self):
        tmp = self.matrix
        # 获得所有特征值和特征向量
        value, vector = np.linalg.eig(tmp)
        # 找到最大值
        max_eigenvalue = np.max(value)
        position = np.argmax(value)
        eigen_vector = vector[:, position]
        # print("最大特征值：" + str(maxEigenvalue) + "其特征向量" + str(eigen_vector))
        return max_eigenvalue, eigen_vector

    '''
    测试一致性
    :param max_eigenvalue: 最大特征值; RI: 随机一致性指标
    :return: 返回是否一致
    '''
    def test_consistence(self, max_eigenvalue, RI):
        CI = (max_eigenvalue - self.row) / (self.row - 1)
        if RI == 0:
            return True
        else:
            CR = CI / RI
            if CR < 0.1:
                return True
            else:
                return False

    '''
    生成RI对应的表，便于直接查找
    '''
    def generate_RI(self):
        n1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        n2 = [0, 0, 0.58, 0.90, 1.12, 1.24, 1.32, 1.41, 1.45, 1.49, 1.51]
        d = dict(zip(n1, n2))
        return d[self.row]

    '''
    特征向量归一化
    :param vector:最大特征值所对应的特征向量
    :return: 归一化后的权向量
    '''
    def normalize(self, vector):
        tmpvector = []
        sum0 = np.sum(vector)
        for i in range(len(vector)):
            tmpvector.append(vector[i] / sum0)

        return np.array(tmpvector)

    '''
    返回计算最后权重的学生数组的组合array
    :return: 生成一个超级大的矩阵，其列数即为学生个数，行数为评判标准的个数
    '''
    def generate_calmatrix(self):
        matrix_generate = np.vstack((self.__vector_container[0], self.__vector_container[1]))
        for i in range(2, len(self.__vector_container)):
            matrix_generate = np.vstack((matrixgen, self.__vector_container[i]))
        return matrix_generate.T


if __name__ == '__main__':
    ContrastMatrix = np.array(
        [1, 0.5, 4, 3, 3, 2, 1, 7, 5, 5, 1 / 4, 1 / 7, 1, 1 / 2, 1 / 3, 1 / 3, 1 / 5, 2, 1, 1, 1 / 3, 1 / 5, 3, 1,
         1]).reshape((5, 5))  # 对比矩阵
    ahp = AhpClass(ContrastMatrix)

    resultmatrix = np.array([])
    if(ahp.test_consistence(ahp.get_eigenvalue_vector()[0], ahp.generate_RI())):
        print("一致性检验成功")
        resultmatrix = ahp.normalize(ahp.get_eigenvalue_vector()[1])
        print(resultmatrix)
    else:
        print("重新构造判断矩阵")

    tmparr = []
    tmparr.append(np.array([0.595, 0.277, 0.129]))
    tmparr.append(np.array([0.082, 0.236, 0.682]))
    tmparr.append(np.array([0.429, 0.429, 0.142]))
    tmparr.append(np.array([0.633, 0.193, 0.175]))
    tmparr.append(np.array([0.166, 0.116, 0.668]))

    matrixgen = np.vstack((tmparr[0], tmparr[1]))
    for i in range(2, len(tmparr)):
        matrixgen = np.vstack((matrixgen, tmparr[i]))

    res = matrixgen.T
    print(res)

    print(res.dot(resultmatrix))






# def ux(x):
#     '''
#     隶属函数
#     :param x:自变量
#     :return: 因变量
#     '''
#     return -1
#
# def isConsistency(matrix = ContrastMatrix):
#     '''
#     层次单排序 和 一致性检验
#     :param matrix: 对比矩阵
#     :return: 布尔变量
#     '''
#
# def getWeigths(matrix = ContrastMatrix):
#     '''
#     计算权向量
#     进行一致性检验
#     :param matrix:对比矩阵
#     :return:权向量
#     '''

# 之后的步骤暂时没有用到
# FAHP还有点小疑问，之后想一下