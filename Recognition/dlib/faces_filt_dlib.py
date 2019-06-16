# -*-coding:utf8-*-#
import os
from face_dlib import faces_detect_dlib, save_faces_dlib
from face_files import get_img_dict
from datetime import datetime
from PIL import Image

count = 0


def save_faces_dlib(image_name, dir):
    global count
    faces = faces_detect_dlib(image_name)
    if len(faces) >= 1:
        save_dir = dir+image_name.split('\\')[1].split("_")[1]
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)

        for k, d in enumerate(faces):
            file_name = os.path.join(save_dir, str(count)+".jpg")
            Image.open(image_name).crop((d.left(), d.top(), d.right(), d.bottom())).save(file_name)
            count += 1


def faces_save_dlib():
    global count
    time1 = datetime.now()
    f_dict = get_img_dict("photo_crawler")

    for person_name in sorted(f_dict.keys(), key=str.lower):
        count = 0
        f_list = f_dict[person_name]
        print("%s loading" % person_name)
        for img_name in f_list:
            save_faces_dlib(img_name, "photo_crawler_dlib\\")

    time2 = datetime.now()
    print("耗时：" + str(time2 - time1))


if __name__ == '__main__':
    faces_save_dlib()




