# -*- coding: utf-8 -*-
# 不推荐使用常规PCA，可以尝试增量PCA(Incremental PCA)和随机PCA（Randomized PCA）
import numpy as np
from sklearn.decomposition import PCA
# 矩阵
X = np.array([[-1, -1], [-2, -1], [-3, -2], [1, 1], [2, 1], [3, 2]])
# PCA参数个数，n_components可以设置为小数，表示想要保留的方差比率
pca = PCA(n_components=2)
# 使用PCA来训练
newX = pca.fit_transform(X)
print(X)
print(newX)
# 方差解释率，显示出方差具体集中在哪一个方向上
print(pca.explained_variance_ratio_)