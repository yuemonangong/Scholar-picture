'''
文献：
Face Description with Local Binary Patterns:Application to Face Recognition
(Timo Ahonen, Student Member, IEEE, Abdenour Hadid,and Matti Pietikainen, ¨ Senior Member, IEEE)
的python实现

LJX
2017.12.04
'''

# coding:utf-8
from cv2 import *
import numpy as np
import os
import random


# 人脸检测器
class faceDetector:
    def __init__(self):
        self.face_cascade = CascadeClassifier(
            "haarcascade_frontalface_default.xml")

    def faceDetect(self, _img):
        img = np.copy(_img)
        gray = cvtColor(img, COLOR_BGR2GRAY)

        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        if len(faces) == 0:
            #print('no face detected! return original image!')
            return _img

        max_x = 0
        max_y = 0
        max_w = 0
        max_h = 0
        for (x, y, w, h) in faces:
            # 框出所有人脸 取其中最大
            #cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            if w >= max_w:
                max_x = x
                max_y = y
                max_w = w
                max_h = h
        # 框出人脸区域的完整输入图像
        #self.markedImg = img
        # 其中最大的人脸图像
        self.largestFace = img[max_y:max_y + max_h, max_x:max_x + max_w]

        return self.largestFace


# 人脸特征提取
class faceFeatureExtract:
    def __init__(self):
        self.faceRegionList = []
        self.bitChangeDict = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0}

    def __faceResize(self, _face, _high=140, _width=140):
        face = resize(_face, (_width, _high), interpolation=INTER_LINEAR)
        return face

    # 将一个大正方形分割为若干个小正方形 _divideScale为每边分几个 默认7 即分解成7*7个窗口
    def faceDivide(self, _face, _divideScale=7):
        self.faceRegionList = []
        face = self.__faceResize(_face)
        faceHeight = face.shape[0]
        faceWidth = face.shape[1]
        # 方形区域大小
        regionHeight = faceHeight // _divideScale
        regionWidth = faceWidth // _divideScale
        lineFace = np.copy(face)
        for i in range(_divideScale):
            if i > 0:
                line(lineFace, (regionWidth * i, 0),
                     (regionWidth * i, faceHeight - 1), (0, 0, 0))
                line(lineFace, (0, regionHeight * i),
                     (faceWidth - 1, regionHeight * i), (0, 0, 0))
            for j in range(_divideScale):
                self.faceRegionList.append(
                    face[regionHeight * i:regionHeight * (
                        i + 1), regionWidth * j:regionWidth * (j + 1)])
        return lineFace

    # 位跳变计数
    def bitChangeCount(self, code):
        count = 0
        for i in range(1, len(code)):
            if code[i] != code[i - 1]:
                count += 1
        return count

    # mode 1(8,1)  2(8,2)
    def generateLBP(self, _src, _mode=1):
        src = _src
        if src.ndim == 3:
            src = cvtColor(src, COLOR_BGR2GRAY)
        # 高斯模糊预处理
        # src=cv2.GaussianBlur(src,(5,5),1.5)
        # 填充边界
        self.bitChangeDict = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0}
        if _mode == 1:
            src = copyMakeBorder(src, 1, 1, 1, 1, BORDER_REPLICATE)
            height = src.shape[0]
            width = src.shape[1]
            dst = np.zeros([height - 2, width - 2], dtype='uint8')
            for m in range(1, height - 1):
                for n in range(1, width - 1):
                    # 阈值为中间像素值
                    lbpThreshold = src[m, n]
                    # 从左上角开始判断
                    if src[m - 1, n - 1] >= lbpThreshold:
                        codeTopLeft = '1'
                    else:
                        codeTopLeft = '0'
                    if src[m - 1, n] >= lbpThreshold:
                        codeTopMid = '1'
                    else:
                        codeTopMid = '0'
                    if src[m - 1, n + 1] >= lbpThreshold:
                        codeTopRight = '1'
                    else:
                        codeTopRight = '0'
                    if src[m, n - 1] >= lbpThreshold:
                        codeMidLeft = '1'
                    else:
                        codeMidLeft = '0'
                    if src[m, n + 1] >= lbpThreshold:
                        codeMidRight = '1'
                    else:
                        codeMidRight = '0'
                    if src[m + 1, n - 1] >= lbpThreshold:
                        codeBottomLeft = '1'
                    else:
                        codeBottomLeft = '0'
                    if src[m + 1, n] >= lbpThreshold:
                        codeBottomMid = '1'
                    else:
                        codeBottomMid = '0'
                    if src[m + 1, n + 1] >= lbpThreshold:
                        codeBottomRight = '1'
                    else:
                        codeBottomRight = '0'
                    # 得到lbp编码
                    lbpCode = codeTopLeft + codeTopMid + codeTopRight + codeMidRight + codeBottomRight + codeBottomMid + codeBottomLeft + codeMidLeft
                    count = self.bitChangeCount(lbpCode)
                    self.bitChangeDict[count] += 1
                    lbpCode = eval('0b' + lbpCode)
                    # print(lbpCode)
                    dst[m - 1, n - 1] = lbpCode
        elif _mode == 2:
            src = copyMakeBorder(src, 2, 2, 2, 2, BORDER_REPLICATE)
            height = src.shape[0]
            width = src.shape[1]
            dst = np.zeros([height - 4, width - 4], dtype='uint8')
            for m in range(2, height - 2):
                for n in range(2, width - 2):
                    # 阈值为中间像素值
                    lbpThreshold = src[m, n]
                    # 从顶角开始判断
                    if src[m - 2, n] >= lbpThreshold:
                        codeTop = '1'
                    else:
                        codeTop = '0'
                    if src[m - 1, n + 1] >= lbpThreshold:
                        codeTopRight = '1'
                    else:
                        codeTopRight = '0'
                    if src[m, n + 2] >= lbpThreshold:
                        codeRight = '1'
                    else:
                        codeRight = '0'
                    if src[m + 1, n + 1] >= lbpThreshold:
                        codeBottomRight = '1'
                    else:
                        codeBottomRight = '0'
                    if src[m + 2, n] >= lbpThreshold:
                        codeBottom = '1'
                    else:
                        codeBottom = '0'
                    if src[m + 1, n - 1] >= lbpThreshold:
                        codeBottomLeft = '1'
                    else:
                        codeBottomLeft = '0'
                    if src[m, n - 2] >= lbpThreshold:
                        codeLeft = '1'
                    else:
                        codeLeft = '0'
                    if src[m - 1, n - 1] >= lbpThreshold:
                        codeTopLeft = '1'
                    else:
                        codeTopLeft = '0'

                    # 得到lbp编码
                    lbpCode = codeTop + codeTopRight + codeRight + codeBottomRight + codeBottom + codeBottomLeft + codeLeft + codeTopLeft
                    count = self.bitChangeCount(lbpCode)
                    self.bitChangeDict[count] += 1
                    lbpCode = eval('0b' + lbpCode)
                    # print(lbpCode)
                    dst[m - 2, n - 2] = lbpCode
        else:
            print('the parameter mode is not right!')
            return 0
        return dst

    def generateLbpDescriptor(self, _face, _divideScale=7, _mode=1):
        if _face.ndim == 3:
            face = cvtColor(_face, COLOR_BGR2GRAY)
        else:
            face = _face

        face = self.__faceResize(face)
        lbpFace = self.generateLBP(face, _mode)
        self.faceDivide(lbpFace)
        localLbpDescriptorList = []
        for i in range(_divideScale**2):
            regionLbp = self.faceRegionList[i]
            hist = calcHist([regionLbp], [0], None, [256], [0.0, 256.0])
            uniformPattensHist = np.zeros([59])
            uniformList = [
                0, 1, 2, 3, 4, 6, 7, 8, 12, 14, 15, 16, 24, 28, 30, 31, 32, 48,
                56, 60, 62, 63, 64, 96, 112, 120, 124, 126, 127, 128, 129, 131,
                135, 143, 159, 191, 192, 193, 195, 199, 207, 223, 224, 225,
                227, 231, 239, 240, 241, 243, 247, 248, 249, 251, 252, 253,
                254, 255
            ]

            for i in range(58):
                uniformPattensHist[i] = hist[uniformList[i]]
            uniformPattensHist[58] = hist.sum() - uniformPattensHist.sum()
            mode = getMod(uniformPattensHist)
            uniformPattensHist = uniformPattensHist / mode
            localLbpDescriptorList.append(uniformPattensHist)
        return localLbpDescriptorList


def bgrEqualizeHist(_img):
    (B, G, R) = split(_img)
    B = equalizeHist(B)
    G = equalizeHist(G)
    R = equalizeHist(R)
    img = merge([B, G, R])
    return img


def getMod(_vec):
    mode = 0
    for i in range(len(_vec)):
        mode += _vec[i]**2
    mode = mode**0.5
    return mode


def getCos(_vec1, _vec2):
    mod1 = getMod(_vec1)
    mod2 = getMod(_vec2)
    innerProduct = sum(_vec1 * _vec2)
    cos = innerProduct / (mod1 * mod2)
    return cos


def getCosSim(_face1, _face2):
    sim = 0
    featureExtractor = faceFeatureExtract()
    descriptor1 = featureExtractor.generateLbpDescriptor(_face1)
    descriptor2 = featureExtractor.generateLbpDescriptor(_face2)
    for i in range(len(descriptor1)):

        if (
                i >= 0 and i <= 6
        ) or i == 7 or i == 13 or i == 21 or i == 27 or i == 28 or i == 34 or i == 35 or i == 41 or i == 42 or i == 48:
            sim = sim + 0 * getCos(descriptor1[i], descriptor2[i])
        elif i == 15 or i == 16 or i == 18 or i == 19:
            sim = sim + 4 * getCos(descriptor1[i], descriptor2[i])
        elif i == 38:
            sim = sim + 2 * getCos(descriptor1[i], descriptor2[i])
        else:
            sim = sim + getCos(descriptor1[i], descriptor2[i])

    sim = sim / (25 + 2 + 16)
    return sim


def getChiSquareDistance(_face1, _face2):
    sim = 0
    featureExtractor = faceFeatureExtract()
    descriptor1 = featureExtractor.generateLbpDescriptor(_face1)
    descriptor2 = featureExtractor.generateLbpDescriptor(_face2)
    for j in range(len(descriptor1)):
        if (
                j >= 0 and j <= 6
        ) or j == 7 or j == 13 or j == 21 or j == 27 or j == 28 or j == 34 or j == 35 or j == 41 or j == 42 or j == 48:
            w = 0
        elif j == 15 or j == 16 or j == 18 or j == 19:
            w = 4
        elif j == 38:
            w = 2
        else:
            w = 1
        for i in range(len(descriptor1[j])):
            denominator = descriptor1[j][i] + descriptor2[j][i]
            if denominator == 0:
                denominator = 1
            sim = sim + w * (
                descriptor1[j][i] - descriptor2[j][i])**2 / denominator

    return sim


def LBP_compare(descriptor1, descriptor2, _threshold):
    sim = 0
    for j in range(len(descriptor1)):
        if (
                j >= 0 and j <= 6
        ) or j == 7 or j == 13 or j == 21 or j == 27 or j == 28 or j == 34 or j == 35 or j == 41 or j == 42 or j == 48:
            w = 0
        elif j == 15 or j == 16 or j == 18 or j == 19:
            w = 4
        elif j == 38:
            w = 2
        else:
            w = 1
        for i in range(len(descriptor1[j])):
            denominator = descriptor1[j][i] + descriptor2[j][i]
            if denominator == 0:
                denominator = 1
            sim = sim + w * (
                descriptor1[j][i] - descriptor2[j][i])**2 / denominator
    if sim <= _threshold:
        return 1
    else:
        return 0


def verify(_face1, _face2, _threshold=60):
    if getChiSquareDistance(_face1, _face2) <= _threshold:
        return 1
    else:
        return 0


def faces_compare_LBP(img1, img2):
    detector = faceDetector()
    face1 = detector.faceDetect(img1)
    face2 = detector.faceDetect(img2)
    if verify(face1, face2, 70):
        return True
    else:
        return False


if __name__ == '__main__':

    feature = faceFeatureExtract()
    detector = faceDetector()
    img1 = imread('photo_author_haar\\004C820F\\0.jpg')
    img2 = imread('photo_crawler\\No.1_7F425224_08EF476D\\baidu\\0_0.jpg')
    face1 = detector.faceDetect(img1)
    face2 = detector.faceDetect(img2)
    sim = getChiSquareDistance(face1, face2)
    print(sim)
    verify(face1, face2)
    # lineFace = feature.faceDivide(face)

    # lbp=feature.generateLbpDescriptor(face)

