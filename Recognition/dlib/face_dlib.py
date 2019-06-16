import dlib
import os
from skimage import io
import numpy as np
import re
from face_files import get_img_name
from PIL import Image
from datetime import datetime

# 模型路径
predictor_path = "shape_predictor.dat"
face_rec_model_path = "dlib_face_recognition.dat"

# 读入模型
detector = dlib.get_frontal_face_detector()
shape_predictor = dlib.shape_predictor(predictor_path)
face_rec_model = dlib.face_recognition_model_v1(face_rec_model_path)


def get_faces_descriptors(f, dets):
    img = io.imread(f)
    for index, face in enumerate(dets):
        shape = shape_predictor(img, face)  # 提取68个特征点
        face_descriptor = face_rec_model.compute_face_descriptor(img, shape)  # 计算人脸的128维向量
        face_descriptor = np.array(face_descriptor)
    return face_descriptor


def faces_detect_dlib(image_name):
    img = io.imread(image_name)
    dets = detector(img, 1)
    return dets


def faces_compare(data1, data2):
    diff = np.linalg.norm(data1-data2)
    if diff < 0.4:
        # print("It's the same person")
        return True
    else:
        # print("It's not the same person")
        return False


def save_faces_dlib(image_name, dir):
    faces = faces_detect_dlib(image_name)
    if len(faces) >= 1:
        save_dir = dir+image_name.split('\\')[1].split(".")[0]
        os.mkdir(save_dir)
        count = 0

        for k, d in enumerate(faces):
            file_name = os.path.join(save_dir, str(count)+".jpg")
            Image.open(image_name).crop((d.left(), d.top(), d.right(), d.bottom())).save(file_name)


def save_author_dlib(image_name):
    def cal_area(d):
        width = d.right() - d.left()
        heigth = d.bottom() - d.top()
        area = width * heigth
        return area

    faces = faces_detect_dlib(image_name)
    if len(faces) >= 1:
        save_dir = "photo_author_dlib\\"+image_name.split('\\')[1].split(".")[0]
        os.mkdir(save_dir)
        count = 0

        for k, d in enumerate(faces):
            dmax = d
            break
        for k, d in enumerate(faces):
            if cal_area(d) > cal_area(dmax):
                dmax = d
        d = dmax
        file_name = os.path.join(save_dir, str(count)+".jpg")
        Image.open(image_name).crop((d.left(), d.top(), d.right(), d.bottom())).save(file_name)


def faces_compare_dlib(img1, img2):
    dets1 = faces_detect_dlib(img1)
    dets2 = faces_detect_dlib(img2)
    data1 = get_faces_descriptors(img1, dets1)
    data2 = get_faces_descriptors(img2, dets2)
    return faces_compare(data1, data2)


def compare():
    img_list = get_img_name("author_photo_dlib_else")
    time1 = datetime.now()

    candidate = []  # 存放训练集人物名字
    descriptors = []  # 存放训练集人物特征列表

    for i in img_list:
        dets = faces_detect_dlib(i)
        if dets:
            search = i.split("\\")[1]
            print("判定人脸图像" + search)
            try:
                descriptors.append(get_faces_descriptors(i, dets))
                candidate.append(search)
            except:
                print("wrong!")

    # des = np.array(descriptors)
    # for i in range(len(des)):
    #     for j in range(i + 1, len(des)):
    #         print("compare " + candidate[i] + " and " + candidate[j])
    #         faces_compare(des[i], des[j])
    # d = dict(zip(candidate, descriptors))

    time2 = datetime.now()
    print("耗时：" + str(time2 - time1))


def cal_acc():
    img_list = get_img_name("photo_author")
    time1 = datetime.now()
    cnt = 0
    call = 1115
    for image_name in img_list:
        search = image_name.split("\\")[1].split(".")[0]
        print("识别图像 " + search)
        try:
            result = faces_detect_dlib(image_name)
            if result:
                cnt += 1
        except:
            print("can not detect")
    print("acc:{:.5f}".format(cnt / float(call)))
    time2 = datetime.now()
    print("耗时：" + str(time2 - time1))


if __name__ == '__main__':
    compare()


