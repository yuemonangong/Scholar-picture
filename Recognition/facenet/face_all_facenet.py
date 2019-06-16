# -*- coding:utf-8 -*-
import os


import json
import tensorflow as tf
import src.facenet
import src.align.detect_face
import numpy as np
from scipy import misc
import re
import shutil
from matrix_fun import matrix
from datetime import datetime

model_path = 'models/facenet/20170512-110547'
deal_with = "crawler"


count = 0

class face_reconition:
    def __init__(self):
        pass

    def prewhiten(self, x):
        mean = np.mean(x)
        std = np.std(x)
        std_adj = np.maximum(std, 1.0 / np.sqrt(x.size))
        y = np.multiply(np.subtract(x, mean), 1 / std_adj)
        return y

    # 没用
    def get_image_paths(self, inpath):
        file_dict = {}
        for root, dirs, files in os.walk(inpath):
            for file in files:
                if re.search(r".jpg", file):
                    if deal_with == "test" or deal_with == "crawler":
                        author = root.split("\\")[1].split("_")[1]  # 特用于scholar_picture
                    if deal_with == "author":
                        author = file.split(".")[0]
                    path = os.path.join(root, file)  # 通用，表示路径
                    if author not in file_dict.keys():
                        file_dict[author] = []
                    file_dict[author].append(path)
        return file_dict

    def faces_get_descriptor(self, image_path, modelpath):
        # 获取图片中的人脸数
        with tf.Graph().as_default():
            with tf.Session() as sess:
                src.facenet.load_model(modelpath)
                # Get input and output tensors
                images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
                embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
                phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")

                img = misc.imread(os.path.expanduser(image_path), mode='RGB')
                images = self.faces_detect(img, image_path)
                print(images.shape)
                # 判断是否检测出人脸 检测不出 就跳出此循环
                if images.shape[0] == 1000:
                    return None
                feed_dict = {images_placeholder: images, phase_train_placeholder: False}

                emb_array = sess.run(embeddings, feed_dict=feed_dict)
        print(emb_array.shape)
        return

    # 将一个文件夹下的所有图片转化为json
    def images_to_vectors(self, inpath, outjson_path, modelpath):
        results = dict()
        with tf.Graph().as_default():
            with tf.Session() as sess:
                src.facenet.load_model(modelpath)
                # Get input and output tensors
                images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
                embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
                phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")

                image_paths = self.get_image_paths(inpath)
                for author in image_paths.keys():
                    result = dict()
                    for image_path in image_paths[author]:
                        # 获取图片中的人脸数
                        img = misc.imread(os.path.expanduser(image_path), mode='RGB')
                        images = self.faces_detect(img, image_path)
                        # 判断是否检测出人脸 检测不出 就跳出此循环
                        if images.shape[0] == 1000:
                            continue
                        feed_dict = {images_placeholder: images, phase_train_placeholder: False}

                        emb_array = sess.run(embeddings, feed_dict=feed_dict)

                        filename_base = 'photo_{}_facenet'.format(deal_with)

                        for j in range(0, len(emb_array)):

                            if deal_with == "test" or deal_with == "crawler":
                                filename_folder = image_path.split("\\")[1].split("_")[1]
                            if deal_with == "author":
                                filename_folder = image_path.split("\\")[1].split(".")[0]
                            filename = os.path.basename(image_path)
                            filename_name, file_extension = os.path.splitext(filename)
                            output_filename_n = "{}/{}/{}{}.jpg".format(filename_base, filename_folder, filename_name,
                                                                        j)
                            result[output_filename_n] = emb_array[j].tolist()
                    results[author] = result

        # All done, save for later!
        print("图像保存完成！")
        json.dump(results, open(outjson_path, "w"))
        # 返回图像中所有人脸的向量
        return results

    def faces_detect(self, image_arr,image_path, image_size=160, margin=32, gpu_memory_fraction=1.0,
                               detect_multiple_faces=True):
        minsize = 20  # minimum size of face
        threshold = [0.6, 0.7, 0.7]  # three steps's threshold
        factor = 0.709  # scale factor

        print('Creating networks and loading parameters')
        with tf.Graph().as_default():
            gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=gpu_memory_fraction)
            sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options, log_device_placement=False))
            with sess.as_default():
                pnet, rnet, onet = src.align.detect_face.create_mtcnn(sess, None)

        img = image_arr
        bounding_boxes, _ = src.align.detect_face.detect_face(img, minsize, pnet, rnet, onet, threshold, factor)
        nrof_faces = bounding_boxes.shape[0]

        nrof_successfully_aligned = 0
        if nrof_faces > 0:
            det = bounding_boxes[:, 0:4]
            det_arr = []
            img_size = np.asarray(img.shape)[0:2]
            if nrof_faces > 1:
                if detect_multiple_faces:
                    for i in range(nrof_faces):
                        det_arr.append(np.squeeze(det[i]))
                else:
                    bounding_box_size = (det[:, 2] - det[:, 0]) * (det[:, 3] - det[:, 1])
                    img_center = img_size / 2
                    offsets = np.vstack(
                        [(det[:, 0] + det[:, 2]) / 2 - img_center[1], (det[:, 1] + det[:, 3]) / 2 - img_center[0]])
                    offset_dist_squared = np.sum(np.power(offsets, 2.0), 0)
                    index = np.argmax(
                        bounding_box_size - offset_dist_squared * 2.0)  # some extra weight on the centering
                    det_arr.append(det[index, :])
            else:
                det_arr.append(np.squeeze(det))

            images = np.zeros((nrof_faces, image_size, image_size, 3))
            for i, det in enumerate(det_arr):
                det = np.squeeze(det)
                bb = np.zeros(4, dtype=np.int32)
                bb[0] = np.maximum(det[0] - margin / 2, 0)
                bb[1] = np.maximum(det[1] - margin / 2, 0)
                bb[2] = np.minimum(det[2] + margin / 2, img_size[1])
                bb[3] = np.minimum(det[3] + margin / 2, img_size[0])
                cropped = img[bb[1]:bb[3], bb[0]:bb[2], :]
                # 进行图片缩放 cv2.resize(img,(w,h))
                scaled = misc.imresize(cropped, (image_size, image_size), interp='bilinear')
                nrof_successfully_aligned += 1

                # print(scaled)
                # scaled=self.prewhiten(scaled)

                # 保存检测的头像
                filename_base = 'photo_{}_facenet'.format(deal_with)
                if deal_with == "test" or deal_with == "crawler":
                    filename_folder = image_path.split("\\")[1].split("_")[1]
                if deal_with == "author":
                    filename_folder = image_path.split("\\")[1].split(".")[0]

                filename = os.path.basename(image_path)
                filename_name, file_extension = os.path.splitext(filename)
                save_dir = "{}/{}".format(filename_base, filename_folder)
                if not os.path.exists(save_dir):
                    os.mkdir(save_dir)
                output_filename_n = "{}/{}/{}{}.jpg".format(filename_base, filename_folder, filename_name, i)
                if not os.path.exists(output_filename_n):
                    misc.imsave(output_filename_n, scaled)

                scaled = src.facenet.prewhiten(scaled)
                scaled = src.facenet.crop(scaled, False, 160)
                scaled = src.facenet.flip(scaled, False)

                images[i] = scaled
        if nrof_faces > 0:
            return images
        else:
            #如果没有检测到人脸  直接返回一个1*3的0矩阵  多少维度都行  只要能和是不是一个图片辨别出来就行
            return np.zeros((1000, 3))


def faces_cluster(out_path):
    with open(out_path, "r") as f:
        f_dict = json.load(f)
    results = dict()
    for person_name in sorted(f_dict.keys(), key=str.lower):
        target = "photo_{}_result".format(deal_with)
        f_list = f_dict[person_name]
        if not os.path.exists(target + "\\" + person_name):  # 用于断点重连
            print("%s loading" % person_name)
            picture = faces_cluster_dict(f_list)
            result = dict()
            if picture:
                os.mkdir(target + "\\" + person_name)
                count = 0
                for p in picture:
                    copy_file_path = target + "\\" + person_name + "\\" + str(count) + "." + p.split(".")[-1]
                    shutil.copyfile(p, copy_file_path)
                    result[copy_file_path] = f_dict[person_name][p]
                    count += 1
            results[person_name] = result
    result_json = "result_{}.json".format(deal_with)
    json.dump(results, open(result_json, "w"))
    return


def faces_cluster_dict(f_dict):
    global count

    def verify(des1, des2):
        judge = matrix()
        distance = judge.EuclideanDistances(des1, des2)
        if distance < 0.8:
            return True
        else:
            return False
    cand = []  # 存放训练集人物名字
    des = []  # 存放训练集人物特征列表

    for file_path in f_dict.keys():
        if os.path.exists(file_path):
            des.append(f_dict[file_path])
            cand.append(file_path)
        else:
            count += 1

    if not cand:
        return None
    d = {0: 1}
    name_list = {0: [cand[0]]}
    for i in range(1, len(des)):
        flag = True
        for j in d.keys():
            if verify(des[i], des[j]):
                flag = False
                d[j] += 1
                name_list[j].append(cand[i])
        if flag:
            d[i] = 1
            name_list[i] = [cand[i]]
    d_sorted = sorted(d.items(), key=lambda item: item[1], reverse=True)
    print(cand[d_sorted[0][0]] + " 照片获取！")
    return name_list[d_sorted[0][0]]


# def count_json():
#     with open("crawler.json", "r") as f:
#         f_dict = json.load(f)
#     cnt = 0
#     for author in f_dict.keys():
#         flag = False
#         for paths in f_dict[author].keys():
#             if not os.path.exists(paths):
#                 flag = True
#                 print("not exist {}".format(paths))
#         if flag:
#             cnt += 1
#     print("共计", cnt)
#     return


if __name__ == "__main__":
    time1 = datetime.now()
    face_rec = face_reconition()
    images_path = 'photo_{}'.format(deal_with)
    modelpath = 'models/facenet/20170512-110547'
    out_path = '{}.json'.format(deal_with)
    face_rec.images_to_vectors(images_path, out_path, model_path)
    faces_cluster(out_path)
    # print("保存丢失数据数:{}".format(count))
    time2 = datetime.now()
    print("total time is "+str(time2 - time1))
#     count_json()


