# -*- coding: utf-8 -*-

import os
import re
import shutil
from face_dlib import faces_compare, get_faces_descriptors, faces_detect_dlib
from face_files import get_dlib_dict


def faces_cluster():
    f_dict = get_dlib_dict("photo_crawler_dlib")
    for person_name in sorted(f_dict.keys(), key=str.lower):
        target = "result1"
        f_list = f_dict[person_name]
        if not os.path.exists(target+"\\" + person_name):  # 用于断点重连
            print("%s loading" % person_name)
            picture = faces_cluster_list(f_list)
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
    return


def faces_cluster_list(f_list):
    cand = []  # 存放训练集人物名字
    des = []  # 存放训练集人物特征列表
    for i in f_list:
        try:
            dets = faces_detect_dlib(i)
            if dets:
                des.append(get_faces_descriptors(i, dets))
                print(i)
                cand.append(i)
        except:
            print("%s dlib cannot deal!" % i)
    if not cand:
        return None
    d = {0: 1}
    name_list = {0: [cand[0]]}
    for i in range(1, len(des)):
        flag = True
        for j in d.keys():
            if faces_compare(des[i], des[j]):
                flag = False
                d[j] += 1
                name_list[j].append(cand[i])
        if flag:
            d[i] = 1
            name_list[i] = [cand[i]]
    d_sorted = sorted(d.items(), key=lambda item: item[1], reverse=True)
    print(cand[d_sorted[0][0]].split('\\')[1] + " 照片获取！")
    return name_list[d_sorted[0][0]]


def faces_cluster_onename(f_list):
    cand = []  # 存放训练集人物名字
    des = []  # 存放训练集人物特征列表
    for i in f_list:
        try:
            dets = faces_detect_dlib(i)
            if dets:
                des.append(get_faces_descriptors(i, dets))
                print(i)
                cand.append(i)
        except:
            print("%s dlib cannot deal!" % i)
    if not cand:
        return None
    d = {0: 1}
    for i in range(1, len(des)):
        flag = True
        for j in d.keys():
            if faces_compare(des[i], des[j]):
                flag = False
                d[j] += 1
        if flag:
            d[i] = 1
    d_sorted = sorted(d.items(), key=lambda item: item[1], reverse=True)
    print(cand[d_sorted[0][0]].split('\\')[1] + " 照片获取！")
    return cand[d_sorted[0][0]]


if __name__ == '__main__':
    faces_cluster()
