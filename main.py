import csv
import sys
from datetime import datetime

import pandas as pd
import pymysql
import glob
import os
import random
from PIL import Image

from PyQt5.QtCore import QTimer, QDate, Qt
from PyQt5.QtCore import  QDateTime
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtCore, QtGui
from matplotlib import pyplot as plt

from demo import Ui_MainWindow
from detect import *

class Ui_LoginDialog(object):
    def setupUi(self, LoginDialog):
        LoginDialog.setObjectName("LoginDialog")
        LoginDialog.resize(300, 200)
        self.layout = QtWidgets.QVBoxLayout(LoginDialog)
        self.layout.setObjectName("layout")
        self.label = QtWidgets.QLabel(LoginDialog)
        self.label.setObjectName("label")
        self.layout.addWidget(self.label)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.hostLabel = QtWidgets.QLabel(LoginDialog)
        self.hostLabel.setObjectName("hostLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.hostLabel)
        self.hostLineEdit = QtWidgets.QLineEdit(LoginDialog)
        self.hostLineEdit.setObjectName("hostLineEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.hostLineEdit)
        self.userLabel = QtWidgets.QLabel(LoginDialog)
        self.userLabel.setObjectName("userLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.userLabel)
        self.userLineEdit = QtWidgets.QLineEdit(LoginDialog)
        self.userLineEdit.setObjectName("userLineEdit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.userLineEdit)
        self.passwordLabel = QtWidgets.QLabel(LoginDialog)
        self.passwordLabel.setObjectName("passwordLabel")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.passwordLabel)
        self.passwordLineEdit = QtWidgets.QLineEdit(LoginDialog)
        self.passwordLineEdit.setObjectName("passwordLineEdit")
        self.passwordLineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.passwordLineEdit)
        self.dbLabel = QtWidgets.QLabel(LoginDialog)
        self.dbLabel.setObjectName("dbLabel")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.dbLabel)
        self.dbLineEdit = QtWidgets.QLineEdit(LoginDialog)
        self.dbLineEdit.setObjectName("dbLineEdit")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.dbLineEdit)
        self.layout.addLayout(self.formLayout)
        self.connectButton = QtWidgets.QPushButton(LoginDialog)
        self.connectButton.setObjectName("connectButton")
        self.layout.addWidget(self.connectButton)

        self.retranslateUi(LoginDialog)
        QtCore.QMetaObject.connectSlotsByName(LoginDialog)

    def retranslateUi(self, LoginDialog):
        _translate = QtCore.QCoreApplication.translate
        LoginDialog.setWindowTitle(_translate("LoginDialog", "数据库登录"))
        self.label.setText(_translate("LoginDialog", "请输入数据库连接信息："))
        self.hostLabel.setText(_translate("LoginDialog", "主机名："))
        self.userLabel.setText(_translate("LoginDialog", "用户名："))
        self.passwordLabel.setText(_translate("LoginDialog", "密码："))
        self.dbLabel.setText(_translate("LoginDialog", "数据库："))
        self.connectButton.setText(_translate("LoginDialog", "连接"))

class CamShow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.fname = ''
        self.setupUi(self)

        #展示时间
        self.timer = QtCore.QTimer()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateDateTime)
        self.timer.start(1000)
        self.updateDateTime()

        #上传、检测、保存、录入
        #tab-bc
        self.uploadbtn.clicked.connect(self.loadImage)
        self.detectbtn.clicked.connect(self.detect_blood)
        self.savebtn.clicked.connect(self.save_image)
        self.enterbtn.clicked.connect(self.enterInfo)
        self.IdInput.returnPressed.connect(self.info_query)

        #tab-malaria
        self.uploadbtn2.clicked.connect(self.loadImage2)
        self.detectbtn2.clicked.connect(self.detect_malaria)
        self.savebtn2.clicked.connect(self.save_image2)
        self.enterbtn2.clicked.connect(self.enterInfo2)
        self.IdInput_3.returnPressed.connect(self.info_query2)

        #tab-cc
        self.batchbtn.clicked.connect(self.loadImages)
        self.progressbtn.clicked.connect(self.detect_nuclei)
        self.generatebtn.clicked.connect(self.show_graph)
        self.savebtn3.clicked.connect(self.save_image3)
        # self.IdInput_3.returnPressed.connect(self.info_query2)

        self.searchbtn.clicked.connect(self.data_query)

        self.db_connection = None

        # self.actionDatabase.triggered.connect(self.showLoginDialog)
        self.connectToDB()
        # self.showLoginDialog()

    #连接数据库
    def connectToDB(self):

        self.db_connection = pymysql.connect(
            host="localhost",
            user="root",
            password="******",
            database="mytest"
        )

        print("连接成功")


    #加载图片
    def loadImage(self):
        fname, _ = QFileDialog.getOpenFileName(self, '请选择图片', '.', '图像文件(*.jpg *.jpeg *.png)')
        print('文件名:', fname)
        if fname:
            jpg = QtGui.QPixmap(fname).scaled(self.originImgLabel.width(), self.originImgLabel.height())
            self.originImgLabel.setPixmap(jpg)
        self.fname=fname

    def loadImage2(self):
        fname, _ = QFileDialog.getOpenFileName(self, '请选择图片', '.', '图像文件(*.jpg *.jpeg *.png)')
        print('文件名:', fname)
        if fname:
            jpg = QtGui.QPixmap(fname).scaled(self.originImgLabel_2.width(), self.originImgLabel_2.height())
            self.originImgLabel_2.setPixmap(jpg)
        self.fname=fname

    def loadImages(self):
        folder_path = QFileDialog.getExistingDirectory(self, '请选择文件夹', '.')
        print('文件夹路径:', folder_path)

        if folder_path:
            self.fname = folder_path
            QMessageBox.information(None, "上传成功", "当前文件夹路径为：" + folder_path)

    #更新时间
    def updateDateTime(self):
        currentDateTime = datetime.now()
        date = currentDateTime.strftime("%Y-%m-%d")
        weekday = currentDateTime.strftime("%A")
        time = currentDateTime.strftime("%H:%M:%S")
        self.timeLabel.setText(f"{date}  {time}")

    #进行血细胞检测
    def run_blood_detection(self):
        # 在这里执行目标检测的逻辑
        class_count_list.clear()
        opt = parse_opt()
        opt.source = self.fname
        weights_bc = './weights/best.pt'
        opt.weights = weights_bc
        check_requirements(exclude=('tensorboard', 'thop'))
        save_dir = run(**vars(opt))
        save_dir = os.path.normpath(save_dir)

        file_paths = glob.glob(save_dir + r"\*.jpg") + glob.glob(save_dir + r"\*.png")

        for file_path in file_paths:
            result_image_path = file_path

        print(result_image_path)
        rbc, wbc, plt = self.get_class_count_bc()
        rbc = str(rbc)
        self.resultTable.item(0, 0).setText(rbc)
        wbc = str(wbc)
        self.resultTable.item(0, 1).setText(wbc)
        plt = str(plt)
        self.resultTable.item(0, 2).setText(plt)

        return result_image_path


    # 进行血细胞检测
    def run_malaria_detection(self):
        # 在这里执行目标检测的逻辑
        class_count_list.clear()
        opt = parse_opt()
        opt.source = self.fname
        weights_malaria = './weights/best_malaria.pt'
        opt.weights = weights_malaria
        check_requirements(exclude=('tensorboard', 'thop'))
        save_dir = run(**vars(opt))
        save_dir = os.path.normpath(save_dir)

        file_paths = glob.glob(save_dir + r"\*.jpg") + glob.glob(save_dir + r"\*.png")

        for file_path in file_paths:
            result_image_path = file_path

        print(result_image_path)
        is_malaria, data = self.get_class_count_malaria()
        result = f'  是否存在感染细胞：{is_malaria} \n  详细信息：{data}'
        self.label_14.setText(result)
        return result_image_path



    # 进行细胞核检测
    def run_nuclei_detection(self):
        # 在这里执行目标检测的逻辑
        opt = parse_opt()
        opt.source = self.fname
        weights_nuclei = './weights/bestcc.pt'
        opt.weights = weights_nuclei
        check_requirements(exclude=('tensorboard', 'thop'))
        save_dir = run(**vars(opt))
        save_dir = os.path.normpath(save_dir)
        # 源文件夹路径
        source_folder = save_dir

        print(class_count_list)
        # 保存为CSV文件
        target_csv_path = os.path.join(source_folder, "class_count.csv")
        with open(target_csv_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['count'])  # 写入列标题
            for item in class_count_list:
                count = int(list(item.values())[0])
                writer.writerow([count])  # 写入每个字典的值
        print("csv done")

        # 获取源文件夹中所有图片文件的路径
        image_files = [os.path.join(source_folder, file) for file in os.listdir(source_folder)
                       if os.path.isfile(os.path.join(source_folder, file))
                       and file.lower().endswith((".jpg", ".jpeg", ".png", ".gif"))]

        # 从图片列表中随机选取六张图片
        selected_images = random.sample(image_files, 6)

        # 计算每张图片的宽度和高度
        image_width, image_height = Image.open(selected_images[0]).size

        # 设置拼接后的图片的宽度和高度
        target_width = 850
        target_height = 550

        # 计算每张图片的缩放比例
        scale_ratio = min(target_width / (image_width * 3), target_height / (image_height * 2))

        # 计算调整后的每张图片的宽度和高度
        adjusted_width = int(image_width * scale_ratio)
        adjusted_height = int(image_height * scale_ratio)

        # 创建一个空白的目标图片
        target_image = Image.new('RGB', (target_width, target_height))

        # 拼接图片
        for i, image_path in enumerate(selected_images):
            image = Image.open(image_path)
            # 调整图片大小
            image = image.resize((adjusted_width, adjusted_height), Image.ANTIALIAS)
            x = (i % 3) * adjusted_width
            y = (i // 3) * adjusted_height
            target_image.paste(image, (x, y))

        # 保存拼接后的图片到当前文件夹（源文件夹）下的sample.png
        target_image_path = os.path.join(source_folder, "sample.png")
        target_image.save(target_image_path)
        print(target_image_path)
        return target_image_path


    def get_class_count_bc(self):
        class_count = class_count_list[0]
        print(class_count)
        rbc = class_count['RBC']
        rbc = int(rbc)
        wbc = class_count['WBC']
        wbc = int(wbc)
        plt = class_count['Platelets']
        plt = int(plt)
        # class_count_list.clear()
        return rbc, wbc, plt

    def get_class_count_malaria(self):
        is_malaria = '否'
        if class_count_list:
            class_count = class_count_list[0]
            data = {key: int(value) for key, value in class_count.items()}
            print(data)

            keys_to_check = ['gametocyte', 'trophozoite', 'schizont', 'ring']
            for key in keys_to_check:
                if key in class_count:
                    is_malaria = '是'

            # class_count_list.clear()
            return is_malaria, data
        else:
            return is_malaria, None



    #血细胞检测调用
    def detect_blood(self):
        # 执行目标检测，这里只是一个示例
        # 您需要替换为您的目标检测逻辑
        if not self.fname:
            QMessageBox.warning(None, "未检测到图像", "请您上传图像！")
            return

        result_image_path = self.run_blood_detection()
        # 在界面中显示处理后的图像
        if result_image_path:
            self.show_result_image(result_image_path)    #展示结果图片

    # 疟疾细胞检测调用
    def detect_malaria(self):
        # 执行目标检测，这里只是一个示例
        # 您需要替换为您的目标检测逻辑
        if not self.fname:
            QMessageBox.warning(None, "未检测到图像", "请您上传图像！")
            return

        result_image_path = self.run_malaria_detection()

        # 在界面中显示处理后的图像
        if result_image_path:
            self.show_result_image2(result_image_path)    # 展示结果图片

    # 细胞核检测调用
    def detect_nuclei(self):
        # 执行目标检测，这里只是一个示例
        # 您需要替换为您的目标检测逻辑
        if not self.fname:
            QMessageBox.warning(None, "未检测到图像", "请您上传图像！")
            return

        result_image_path = self.run_nuclei_detection()

        # 在界面中显示处理后的图像
        if result_image_path:
            self.show_result_image3(result_image_path)    # 展示结果图片

    def show_result_image(self, result_image_path):
        if result_image_path:
            jpg = QtGui.QPixmap(result_image_path).scaled(self.resultImgLabel.width(), self.resultImgLabel.height())
            self.resultImgLabel.setPixmap(jpg)

    def show_result_image2(self, result_image_path):
        if result_image_path:
            jpg = QtGui.QPixmap(result_image_path).scaled(self.resultImgLabel_2.width(), self.resultImgLabel_2.height())
            self.resultImgLabel_2.setPixmap(jpg)

    def show_result_image3(self, result_image_path):
        if result_image_path:
            jpg = QtGui.QPixmap(result_image_path).scaled(self.label_6.width(), self.label_6.height())
            self.label_6.setPixmap(jpg)

    def show_graph(self):
        result_image_path = self.draw_graph()
        if result_image_path:
            jpg = QtGui.QPixmap(result_image_path).scaled(self.label_6.width(), self.label_6.height())
            self.label_6.setPixmap(jpg)
        else:
            QMessageBox.warning(None,"数据错误！","请在处理文件夹后再生成图标！")


    def draw_graph(self):
        # 目标文件夹路径
        folder_path = 'runs\\detect'

        # 获取目标文件夹下所有文件夹的路径
        folder_paths = glob.glob(os.path.join(folder_path, '*'))

        # 按照文件夹的创建时间进行排序
        folder_paths.sort(key=os.path.getctime, reverse=True)

        # 获取最新创建的文件夹路径
        directory = folder_paths[0]
        print(directory)
        csv_path = os.path.join(directory, "class_count.csv")
        exist = os.path.exists(csv_path)
        if exist:
            # 读取CSV文件数据
            data = pd.read_csv(csv_path)

            # 绘制折线图
            plt.figure(figsize=(5, 5))  # 设置图像大小
            data['count'].plot(kind='line', marker='o')
            plt.xlabel('Index')
            plt.ylabel('Count')
            plt.title('Count Trend')
            # plt.tight_layout()

            # 保存折线图
            line_path = os.path.join(directory, "line_chart.png")
            plt.savefig(line_path)

            # 自定义划分区间
            # 区间范围和标签
            bins = [0, 30, 60, 90, 120, 150, float('inf')]
            labels = ['1-30', '31-60', '61-90', '91-120', '121-150', '>150']

            # 分类计数
            data['category'] = pd.cut(data['count'], bins=bins, labels=labels, right=False)
            count_by_category = data['category'].value_counts().sort_index()

            # 绘制饼图
            plt.figure(figsize=(5, 5))
            plt.pie(count_by_category, labels=count_by_category.index, autopct='%1.1f%%', startangle=90, counterclock=False)
            plt.axis('equal')
            plt.title('Count Distribution by Category')
            # plt.tight_layout()

            # 保存饼图
            pie_path = os.path.join(directory, "pie_chart.png")
            plt.savefig(pie_path)

            # 倒序计数
            count_by_category = count_by_category[::-1]

            # 绘制柱状图
            plt.figure(figsize=(5, 5))
            plt.barh(count_by_category.index, count_by_category.values)
            plt.xlabel('Count')
            plt.ylabel('Category')
            plt.title('Count Distribution by Category')
            plt.tight_layout()

            # 保存柱状图
            bar_path = os.path.join(directory, "bar_chart.png")
            plt.savefig(bar_path)

            # image_paths = [bar_path, pie_path, line_path]
            image_paths = [pie_path, line_path]
            output_path = os.path.join(directory, "result.png")

            images = [Image.open(path) for path in image_paths]

            # 获取图片的最大宽度和高度
            max_width = max(image.width for image in images)
            total_height = max(image.height for image in images)

            # 创建新的空白图像作为拼接结果
            result = Image.new('RGB', (max_width * len(images), total_height))

            # 将每张图片依次拼接到结果图像上
            x_offset = 0
            for image in images:
                result.paste(image, (x_offset, 0))
                x_offset += image.width

            # 保存拼接后的图像
            result.save(output_path)
            return output_path
        else:
            return None



    #保存图片
    def save_image(self):
        if self.resultImgLabel.pixmap():
            file_dialog = QFileDialog(self)
            save_path, _ = file_dialog.getSaveFileName(self, "保存图像", "", "JPEG Image (*.jpg);;PNG Image (*.png)")

            if save_path:
                pixmap = self.resultImgLabel.pixmap()
                pixmap.save(save_path)

                print("图像保存成功:", save_path)

    def save_image2(self):
        if self.resultImgLabel_2.pixmap():
            file_dialog = QFileDialog(self)
            save_path, _ = file_dialog.getSaveFileName(self, "保存图像", "", "JPEG Image (*.jpg);;PNG Image (*.png)")

            if save_path:
                pixmap = self.resultImgLabel_2.pixmap()
                pixmap.save(save_path)

                print("图像保存成功:", save_path)

    def save_image3(self):
        if self.label_6.pixmap():
            file_dialog = QFileDialog(self)
            save_path, _ = file_dialog.getSaveFileName(self, "保存图像", "", "JPEG Image (*.jpg);;PNG Image (*.png)")

            if save_path:
                pixmap = self.label_6.pixmap()
                pixmap.save(save_path)

                print("图像保存成功:", save_path)

    #录入信息
    def enterInfo(self):
        if self.db_connection:
            name = self.nameInput.text()
            gender = self.genderInput.text()
            age = self.ageInput.text()
            if age:
                age = int(age)
            nid = self.IdInput.text()
            if nid:
                nid = int(nid)

            rbc = self.resultTable.item(0, 0).text()
            if rbc:
                rbc = int(rbc)
            wbc = self.resultTable.item(0, 1).text()
            if wbc:
                wbc = int(wbc)
            plt = self.resultTable.item(0, 2).text()
            if plt:
                plt = int(plt)

            # 获取当前日期
            current_date = QDate.currentDate().toString(Qt.ISODate)
            current_date = QDateTime.currentDateTime().toString(Qt.ISODate)

            if name and gender and age and rbc and wbc and plt and nid:
                try:
                    self.enter_patient_info(nid,name,gender,age)
                    cursor = self.db_connection.cursor()
                    cursor.execute(
                        "INSERT INTO bc_info (date, RBC, WBC, PLT, nid) VALUES ( %s, %s, %s, %s, %s)",
                        (current_date, rbc, wbc, plt, nid))
                    self.db_connection.commit()
                    QMessageBox.information(None, "录入成功", "信息录入成功！")
                    cursor.close()
                except pymysql.Error as e:
                    QMessageBox.warning(None, "录入失败", f"信息录入失败：{str(e)}")
            else:
                QMessageBox.warning(None, "录入失败", "请填写完整信息！")
        else:
            QMessageBox.warning(None, "未连接数据库", "您还未连接数据库！")


    def enterInfo2(self):
        if self.db_connection:
            name = self.nameInput_3.text()
            gender = self.genderInput_3.text()
            age = self.ageInput_3.text()
            if age:
                age = int(age)
            nid = self.IdInput_3.text()
            if nid:
                nid = int(nid)

            is_malaria, result = self.get_class_count_malaria()
            print(result)
            if result:
                gametocyte = result.get('gametocyte', 0)
                trophozoite = result.get('trophozoite', 0)
                leukocyte = result.get('leukocyte', 0)
                difficult = result.get('difficult', 0)
                rbc = result.get('red blood cell', 0)
                schizont = result.get('schizont', 0)
                ring = result.get('ring', 0)

            # 获取当前日期
            # current_date = QDate.currentDate().toString(Qt.ISODate)
            current_date = QDateTime.currentDateTime().toString(Qt.ISODate)
            if result and name and gender and age and nid:
                try:
                    self.enter_patient_info(nid, name, gender, age)
                    cursor = self.db_connection.cursor()
                    cursor.execute(
                        "INSERT INTO malaria_info (nid, date, gametocyte, trophozoite, leukocyte, difficult, rbc, schizont, ring, is_malaria) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                        (nid, current_date, gametocyte, trophozoite, leukocyte, difficult, rbc, schizont, ring, is_malaria))
                    self.db_connection.commit()
                    QMessageBox.information(None, "录入成功", "信息录入成功！")
                    cursor.close()
                except pymysql.Error as e:
                    QMessageBox.warning(None, "录入失败", f"信息录入失败：{str(e)}")
            else:
                QMessageBox.warning(None, "录入失败", "请填写完整信息！")
        else:
            QMessageBox.warning(None, "未连接数据库", "您还未连接数据库！")

    def enter_patient_info(self,nid,name,gender,age):
        if nid and name and gender and age:
            try:
                cursor = self.db_connection.cursor()
                cursor.execute(
                    "REPLACE INTO patients_info (nid, name, gender, age) VALUES (%s, %s, %s, %s)",
                    (nid,name,gender,age))
                self.db_connection.commit()
                cursor.close()
            except pymysql.Error as e:
                QMessageBox.warning(None, "录入失败", f"信息录入失败：{str(e)}")



    def info_query(self):
        if self.db_connection:
            nid = self.IdInput.text()
            nid_effect = self.check_id(nid)
            if nid_effect:
                cursor = self.db_connection.cursor()
                cursor.execute(f"SELECT name, gender, age FROM patients_info WHERE nid = '{nid}'")
                result = cursor.fetchone()
                print(result)
                self.nameInput.setText(result[0])
                self.genderInput.setText(result[1])
                self.ageInput.setText(str(result[2]))
                cursor.close()
            else:
                QMessageBox.warning(None, "错误ID", "请核对您的就诊卡号信息！")

    def info_query2(self):
        if self.db_connection:
            nid = self.IdInput_3.text()
            print(nid)
            nid_effect = self.check_id(nid)
            print(nid_effect)

            if nid_effect:
                cursor = self.db_connection.cursor()
                cursor.execute(f"SELECT name, gender, age FROM patients_info WHERE nid = '{nid}'")
                result = cursor.fetchone()
                print(result)
                self.nameInput_3.setText(result[0])
                self.genderInput_3.setText(result[1])
                self.ageInput_3.setText(str(result[2]))
                cursor.close()
            else:
                QMessageBox.warning(None, "错误ID", "请核对您的就诊卡号信息！")

    def check_id(self, nid):
        if self.db_connection:
            cursor = self.db_connection.cursor()

            # 执行查询语句，检查字段是否存在
            query = f"SELECT COUNT(*) FROM patients_info WHERE nid = '{nid}'"
            cursor.execute(query)
            result = cursor.fetchone()[0]

            print(result)

            # 关闭数据库连接
            cursor.close()
            return result > 0

    def data_query(self):
        if self.db_connection:
            nid = self.IdInput_2.text()
            table_name = self.comboBox.currentText()

            # 根据nid字段查询
            if nid:
                # 创建查询语句
                if table_name == '血细胞检测':
                    query = f"SELECT * FROM bc_info WHERE nid = '{nid}'"
                    self.nid_bc(nid, query)
                elif table_name == '疟疾细胞检测':
                    query = f"SELECT * FROM malaria_info WHERE nid = '{nid}'"
                    self.nid_malaria(nid, query)

            # 无ID输入，表中全部数据
            else:
                # 查询 bc_info
                if table_name == '血细胞检测':
                    query = f"SELECT * FROM bc_info"
                    self.nid_bc(nid=0, query=query)
                # 查询 malaria_info
                elif table_name == '疟疾细胞检测':
                    query = f"SELECT * FROM malaria_info"
                    self.nid_malaria(nid=0, query=query)

    def nid_bc(self, nid, query):

        cursor = self.db_connection.cursor()
        # 执行查询
        cursor.execute(query)
        result = cursor.fetchall()

        # 获取列名信息
        column_names = [column[0] for column in cursor.description]

        fliter = ['id', 'difficult']

        for val in fliter:
            if val in column_names:
                # 获取字段的索引位置
                id_index = column_names.index(val)

                # 移除字段
                column_names.pop(id_index)

                # 移除字段对应的列数据
                result = [row[:id_index] + row[id_index + 1:] for row in result]

        if nid != 0:
            # 查询 patients_info 表的 name, gender, age 字段
            query_patients_info = f"SELECT name, gender, age FROM patients_info WHERE nid = '{nid}'"
            cursor.execute(query_patients_info)
            patients_info_result = cursor.fetchone()
            print(patients_info_result)

            # 合并查询结果
            if patients_info_result:
                # 在原查询结果的每一条数据前添加 patients_info_result
                result = [patients_info_result + row for row in result]
                print(result)
                # 更新列名信息
                column_names = ['name', 'gender', 'age'] + column_names

        while self.verticalLayout_3.count():
            item = self.verticalLayout_3.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
            else:
                self.verticalLayout_3.removeItem(item)

        # 创建表格模型
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(column_names)  # 设置表头

        # 添加数据到模型
        for row in result:
            items = [QStandardItem(str(item)) for item in row]
            model.appendRow(items)

        # 创建表格视图
        table_view = QTableView()
        table_view.setModel(model)
        table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 自适应列宽

        # 将表格视图添加到布局
        self.verticalLayout_3.addWidget(table_view)

        cursor.close()

        return

    def nid_malaria(self, nid, query):

        cursor = self.db_connection.cursor()
        # 执行查询
        cursor.execute(query)
        result = cursor.fetchall()

        # 获取列名信息
        column_names = [column[0] for column in cursor.description]

        fliter = ['id', 'difficult']

        for val in fliter:
            if val in column_names:
                # 获取字段的索引位置
                id_index = column_names.index(val)

                # 移除字段
                column_names.pop(id_index)

                # 移除字段对应的列数据
                result = [row[:id_index] + row[id_index + 1:] for row in result]

        if nid != 0:
            # 查询 patients_info 表的 name, gender, age 字段
            query_patients_info = f"SELECT name, gender, age FROM patients_info WHERE nid = '{nid}'"
            cursor.execute(query_patients_info)
            patients_info_result = cursor.fetchone()
            print(patients_info_result)

            # 合并查询结果
            if patients_info_result:
                # 在原查询结果的每一条数据前添加 patients_info_result
                result = [patients_info_result + row for row in result]
                print(result)

            process_result = []

            # 处理数据并插入到表格中
            for i, row in enumerate(result):
                infected_cell = row[5] + row[6] + row[9] + row[10]
                risk = '是' if infected_cell > 50 else '否'

                # 删除原始数据第六列以后的数据
                result = row[:5] + (infected_cell, risk)
                process_result.append(result)

            column_names = ['name', 'gender', 'age', 'nid', 'date', 'infected_cell', 'risk']

        else:
            process_result = []
            # 处理数据并插入到表格中
            for i, row in enumerate(result):
                infected_cell = row[2] + row[3] + row[6] + row[7]
                risk = '是' if infected_cell > 50 else '否'

                # 删除原始数据第六列以后的数据
                result = row[:2] + (infected_cell, risk)
                process_result.append(result)

            column_names = ['nid', 'date', 'infected_cell', 'risk']

        print("--------------")
        print(process_result)

        while self.verticalLayout_3.count():
            item = self.verticalLayout_3.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
            else:
                self.verticalLayout_3.removeItem(item)

        # 创建表格模型
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(column_names)  # 设置表头

        # 添加数据到模型
        for row in process_result:
            items = [QStandardItem(str(item)) for item in row]
            model.appendRow(items)

        # 创建表格视图
        table_view = QTableView()
        table_view.setModel(model)
        table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 自适应列宽

        # 将表格视图添加到布局
        self.verticalLayout_3.addWidget(table_view)

        cursor.close()

        return

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = CamShow()
    ui.show()
    sys.exit(app.exec_())
