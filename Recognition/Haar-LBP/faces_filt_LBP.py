# -*-coding:utf8-*-#
import os
from face_haar import faces_detect_haar
from face_LBP import faceDetector, faceFeatureExtract
from face_files import get_img_dict, get_img_name
from datetime import datetime
from PIL import Image
from cv2 import *

count = 0


def save_faces_LBP(image_name, dir):
    global count
    faces = faces_detect_haar(image_name)
    if len(faces) >= 1:
        save_dir = dir+image_name.split('\\')[1].split("_")[1]
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)

        for (x1, y1, x2, y2) in faces:
            file_name = os.path.join(save_dir, str(count) + ".jpg")
            Image.open(image_name).crop((x1, y1, x2, y2)).save(file_name)
            count += 1


def faces_save_LBP():
    global count
    time1 = datetime.now()
    f_dict = get_img_dict("photo_crawler")

    for person_name in sorted(f_dict.keys(), key=str.lower):
        count = 0
        f_list = f_dict[person_name]
        print("%s loading" % person_name)
        for img_name in f_list:
            save_faces_LBP(img_name, "photo_crawler_LBP\\")

    time2 = datetime.now()
    print("耗时：" + str(time2 - time1))


def save_author_LBP(image_name, dir):
    global count
    img = imread(image_name)
    face = faceDetector().faceDetect(img)
    if face.any:
        save_dir = dir+image_name.split('\\')[1].split(".")[0]
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)
        file_name = os.path.join(save_dir, str(count) + ".jpg")
        imwrite(file_name, face)
        count += 1


def author_save_LBP():
    global count
    time1 = datetime.now()
    f_dict = get_img_name("photo_author")

    for img_name in f_dict:
        count = 0
        print("%s loading" % img_name)
        save_author_LBP(img_name, "photo_author_haar\\")

    time2 = datetime.now()
    print("耗时：" + str(time2 - time1))


if __name__ == '__main__':
    faces_save_LBP()




