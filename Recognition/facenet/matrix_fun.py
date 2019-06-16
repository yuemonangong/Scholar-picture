# -*- coding:utf-8 -*-
import numpy as np


class matrix:
    def __init__(self):
        pass

    # 两个矩阵的欧式距离
    def EuclideanDistances(self, A, B):
        A = np.array(A)
        B = np.array(B)
        distance = np.linalg.norm(A - B)
        # BT = B.transpose()
        # # vecProd = A * BT
        # vecProd = np.dot(A, BT)
        # # print(vecProd)
        # SqA = A ** 2
        # # print(SqA)
        # sumSqA = np.matrix(np.sum(SqA, axis=1))
        # sumSqAEx = np.tile(sumSqA.transpose(), (1, vecProd.shape[1]))
        # # print(sumSqAEx)
        #
        # SqB = B ** 2
        # sumSqB = np.sum(SqB, axis=1)
        # sumSqBEx = np.tile(sumSqB, (vecProd.shape[0], 1))
        # SqED = sumSqBEx + sumSqAEx - 2 * vecProd
        # SqED[SqED < 0] = 0.0
        # ED = np.sqrt(SqED)
        return distance

