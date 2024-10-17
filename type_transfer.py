import os
import json


def txt_to_json(txt_file, json_file):
    data = {}
    with open(txt_file, 'r', encoding='utf-8') as file:
        content = file.read().split("--------------------------------------------------\n\n")
        for item in content:
            if item.startswith('评论 '):
                key, value = item.split(":\n", 1)
                data[key] = value
    with open(json_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def convert_files_in_folder(folder):
    for filename in os.listdir(folder):
        basename, extension = os.path.splitext(filename)
        if extension.lower() == '.txt':
            txt_file = os.path.join(folder, filename)
            json_file = os.path.join(folder, basename + '.json')
            txt_to_json(txt_file, json_file)


# 将下面的 'your_folder' 替换为你需要转换的文件夹路径
convert_files_in_folder("/home/hadoop/big-data/movie_reviews")

