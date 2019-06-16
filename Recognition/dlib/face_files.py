"""获取文件名，并且他们按类保存"""
import os
import re


def get_img_name(file_dir):
    file_list = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if re.search(r".jpg", file):
                path = os.path.join(root, file)
                file_list.append(path)
    return file_list


def get_img_dict(file_dir):
    file_dict = {}
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if re.search(r".jpg", file):
                author = root.split("\\")[1].split("_")[1]  # 特用于scholar_picture
                path = os.path.join(root, file)  # 通用，表示路径
                if author not in file_dict.keys():
                    file_dict[author] = []
                file_dict[author].append(path)
    return file_dict


def get_dlib_dict(file_dir):
    file_dict = {}
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if re.search(r".jpg", file):
                author = root.split("\\")[1]  # 特用于识别切割后保存的文件夹
                path = os.path.join(root, file)  # 通用，表示路径
                if author not in file_dict.keys():
                    file_dict[author] = []
                file_dict[author].append(path)
    return file_dict


def get_LBP_dict(file_dir):
    file_dict = {}
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if re.search(r".jpg", file):
                author = root.split("\\")[1]  # 特用于识别切割后保存的文件夹
                path = os.path.join(root, file)  # 通用，表示路径
                path = path.split("\\").join("\\")
                if author not in file_dict.keys():
                    file_dict[author] = []
                file_dict[author].append(path)
    return file_dict


if __name__ == '__main__':
    l = get_img_name("photo_author")
    print(len(l))
