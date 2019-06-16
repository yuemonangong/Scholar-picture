# -*-coding:utf8-*-#
import os
import cv2
import re
from PIL import Image
from datetime import datetime
from face_files import get_img_name


def faces_detect_haar(image_name):
    img = cv2.imread(image_name)
    pathf = 'C:\\Users\\86182\\AppData\\Local\\Continuum\\anaconda3\\envs\\opencv\\Library\\etc\\' \
            'haarcascades\\haarcascade_frontalface_default.xml'
    face_cascade = cv2.CascadeClassifier(pathf)
    if img.ndim == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img

    faces = face_cascade.detectMultiScale(gray, 1.2, 5)  # 1.3和5是特征的最小、最大检测窗口，它改变检测结果也会改变
    result = []
    for (x, y, width, height) in faces:
        result.append((x, y, x + width, y + height))
    return result


# 保存人脸图
def save_faces_haar(image_name):
    faces = faces_detect_haar(image_name)
    if faces:
        # 将人脸保存在save_dir目录下。
        # Image模块：Image.open获取图像句柄，crop剪切图像(剪切的区域就是detectFaces返回的坐标)，save保存。
        save_dir = image_name.split('.')[0]+"_faces"
        os.mkdir(save_dir)
        count = 0
        for (x1, y1, x2, y2) in faces:
            file_name = os.path.join(save_dir,str(count)+".jpg")
            Image.open(image_name).crop((x1, y1, x2, y2)).save(file_name)
            count += 1


def faces_detect(image_name):
    return faces_detect_haar(image_name)


def faces_save(image_name):
    save_faces_haar(image_name)


if __name__ == '__main__':
    img_list = get_img_name("photo_author")
    time1 = datetime.now()
    cnt = 0
    call = 1115
    for image_name in img_list:
        search = image_name.split("\\")[1].split(".")[0]
        print("识别图像 " + search)
        try:
            result = faces_detect(image_name)
            if result:
                cnt += 1
        except:
            print("can not detect")
    print("acc:{:.5f}".format(cnt/float(call)))
    time2 = datetime.now()
    print("耗时：" + str(time2 - time1))
