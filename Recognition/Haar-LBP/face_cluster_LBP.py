# -*- coding: utf-8 -*-

import os
from face_LBP import faceDetector, verify, faceFeatureExtract, faces_compare_LBP, LBP_compare
import shutil
from cv2 import *
from face_files import get_img_dict, get_dlib_dict
from datetime import datetime
import numpy as np


def faces_cluster_LBP():
    time1 = datetime.now()
    f_dict = get_dlib_dict("photo_crawler_LBP")
    for person_name in sorted(f_dict.keys(), key=str.lower):
        target = "result_LBP"
        f_list = f_dict[person_name]
        if not os.path.exists(target+"\\" + person_name):  # 用于断点重连
            print("%s loading" % person_name)
            detect = faceDetector()
            feature = faceFeatureExtract()
            picture = faces_cluster_list(f_list, detect, feature)
            if picture:
                os.mkdir(target+"\\"+person_name)
                count = 0
                for p in picture:
                    shutil.copyfile(p, target+"\\"+person_name+"\\"+str(count)+"."+p.split(".")[-1])
                    count += 1
                # print(picture)
                # 以下用于单图保存
                # shutil.copy(picture, target)
                # if os.path.exists(target+"\\"+picture.split("\\")[-1]):
                #     if not os.path.exists(target+"\\" + picture.split("\\")[1]+".jpg"):
                #         os.rename(target+"\\"+picture.split("\\")[-1], target+"\\"+picture.split("\\")[1]+".jpg")
                #     else:
                #         os.remove(target+"\\"+picture.split("\\")[-1])
    time2 = datetime.now()
    print("耗时：" + str(time2 - time1))
    return


def faces_cluster_list(f_list, detect, feature):
    cand = []  # 存放训练集人物名字
    des = []  # 存放训练集人物特征列表
    for i in f_list:
        try:
            face = detect.faceDetect(imread(i))
            if face.any:
                descriptor = feature.generateLbpDescriptor(face)
                descriptor = np.array(descriptor)
                des.append(descriptor)
                print(i)
                cand.append(i)
        except:
            print("%s LBP cannot deal!" % i)
    if not cand:
        return None
    d = {0: 1}
    name_list = {0: [cand[0]]}
    for i in range(1, len(des)):
        flag = True
        for j in d.keys():
            try:
                if LBP_compare(des[i], des[j], 70):
                    flag = False
                    d[j] += 1
                    name_list[j].append(cand[i])
            except:
                print("%s + %s wrong" % (cand[i], cand[j]))
        if flag:
            d[i] = 1
            name_list[i] = [cand[i]]
    d_sorted = sorted(d.items(), key=lambda item: item[1], reverse=True)
    print(cand[d_sorted[0][0]].split('\\')[1] + " 照片获取！")
    return name_list[d_sorted[0][0]]


if __name__ == '__main__':
    faces_cluster_LBP()
