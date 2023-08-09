import pandas as pd
import json
import os


def convert_to_yolov5_format(data, image_width, image_height):
    yolov5_labels = []

    label_mapping = {
        'gametocyte': 0,
        'trophozoite': 1,
        'leukocyte': 2,
        'difficult': 3,
        'red blood cell': 4,
        'schizont': 5,
        'ring': 6
    }

    for obj in data["objects"]:
        xmin = obj["bounding_box"]["minimum"]["c"]
        ymin = obj["bounding_box"]["minimum"]["r"]
        xmax = obj["bounding_box"]["maximum"]["c"]
        ymax = obj["bounding_box"]["maximum"]["r"]
        category = obj["category"]
        l = label_mapping.get(category)

        # 计算归一化坐标
        x_center = (xmin + xmax) / 2 / image_width
        y_center = (ymin + ymax) / 2 / image_height
        width = (xmax - xmin) / image_width
        height = (ymax - ymin) / image_height

        # 将坐标信息添加到YOLOv5标签列表中
        label = f"{l} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}"
        yolov5_labels.append(label)

    return yolov5_labels


def process_json_file(json_file, output_dir):
    # 读取JSON数据
    with open(json_file, "r") as file:
        data = json.load(file)


    for item in data:
        # 图像宽度和高度
        image_width = item["image"]["shape"]["c"]
        image_height = item["image"]["shape"]["r"]

        # 转换为YOLOv5格式
        yolov5_labels = convert_to_yolov5_format(item, image_width, image_height)

        # 获取输出文件名
        filename = os.path.splitext(os.path.basename(item["image"]["pathname"]))[0]
        output_path = os.path.join(output_dir, filename + ".txt")

        # 将YOLOv5标签保存到文本文件
        with open(output_path, "w") as file:
            file.write("\n".join(yolov5_labels))


# 设置输入JSON文件和输出目录路径
json_file = "json/training.json"
output_directory = "train_label"

# 处理JSON文件
process_json_file(json_file, output_directory)


