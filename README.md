# 细胞检测系统

## 一、运行环境

Python、Pytorch、PyQT

具体环境配置见项目代码/requirements.txt

## 二、主要代码说明

1. main.py：项目主函数，显示前端界面，调用其他函数进行处理，将输出结果与前端交互
2. detect.py：细胞检测预测代码，使用模型进行预测并输出结果给main函数
3. demo.py (demo.ui)：前端界面
4. train.py：模型训练主要代码
5. requirements.txt：环境需求文件
6. data_process_malaria.py：数据预处理代码
7. weights：训练权重文件
8. static：静态文件
9. runs/detect：预测结果默认保存路径
10. runs/train：训练结果默认保存路径
11. test_images：测试图片

## 三、训练数据说明

1. BCCD数据集：该数据集共有三类364张图像：（WBC白细胞），RBC（红细胞）和Platelets。3个类别中有4888个标签（有0个空示例）。可直接训练使用。

   数据链接：[GitHub - Shenggan/BCCD_Dataset: BCCD (Blood Cell Count and Detection) Dataset is a small-scale dataset for blood cells detection.](https://github.com/Shenggan/BCCD_Dataset)

2. 疟疾细胞数据集：数据集包含两类未感染的细胞（红细胞RBCs和白细胞leukocytes），以及四类感染的细胞（配子体gametocytes、环状体rings、滋养体trophozoites和裂殖体schizonts）。如果某些细胞不明显属于任何一种细胞类别，注释者可以将其标记为困难。数据集中未感染的红细胞相对于未感染的白细胞和感染的细胞占据了绝大多数，超过95%。数据标签与yolo训练数据不符，训练前需预先处理。

   数据链接：https://www.kaggle.com/datasets/kmader/malaria-bounding-boxes

   数据预处理可参考data_process_malaria.py

3. 细胞核分割数据集：该数据集用于分割显微镜下细胞图像的细胞核位置，包含来自不同组织的细胞图像，其中细胞核的位置已标注，以0-1掩码图像的方式给出。数据标签与yolo训练数据不符，训练前需预先处理。

   数据预处理可参考data_process_core.py

## 四、训练模型下载
weights中包含三个已经训练好的模型，预训练模型yolov5-l

链接：https://pan.baidu.com/s/1vrD4EQXX2w2MctspOcRe2g?pwd=ty35 
提取码：ty35

## 五、项目运行说明

1. 注意将main.py函数中数据库连接的相关信息进行修改
2. 直接运行main.py即可打开用户界面，按照界面提示进行操作即可

