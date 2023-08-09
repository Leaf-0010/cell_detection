import glob
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from detect import *


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.fname = ""  # 成员变量用于存储图像路径

        self.setWindowTitle("目标检测")
        self.setGeometry(100, 100, 1600, 1200)
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.upload_button = QPushButton("上传图像", self.central_widget)
        self.upload_button.clicked.connect(self.upload_image)

        self.detect_button = QPushButton("目标检测", self.central_widget)
        self.detect_button.clicked.connect(self.detect_objects)

        self.image_label = QLabel(self.central_widget)
        self.image_label.setFixedSize(800, 600)
        self.image_label.setAlignment(Qt.AlignCenter)

        self.result_label = QLabel(self.central_widget)
        self.result_label.setFixedSize(800, 600)
        self.result_label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout(self.central_widget)
        layout.addWidget(self.upload_button)
        layout.addWidget(self.detect_button)
        layout.addWidget(self.image_label)
        layout.addWidget(self.result_label)

    def upload_image(self):
        file_dialog = QFileDialog(self)
        image_path, _ = file_dialog.getOpenFileName(self, "选择图像")
        print(image_path)
        if image_path:
            self.fname = image_path  # 将图像路径存储到成员变量
            # 在界面中显示上传的图像
            self.show_image(image_path)

    def show_image(self, image_path):
        pixmap = QPixmap(image_path)
        self.image_label.setPixmap(pixmap.scaledToWidth(800))

    def detect_objects(self):
        # 执行目标检测，这里只是一个示例
        # 您需要替换为您的目标检测逻辑
        result_image_path = self.run_object_detection()

        # 在界面中显示处理后的图像
        self.show_result_image(result_image_path)

    def run_object_detection(self):
        # 在这里执行目标检测的逻辑
        opt = parse_opt()
        opt.source = self.fname
        opt.weights = 'weights/bestcc.pt'
        check_requirements(exclude=('tensorboard', 'thop'))
        save_dir = run(**vars(opt))
        print(save_dir)
        # 返回处理后的图像路径
        save_dir = os.path.normpath(save_dir)

        file_paths = glob.glob(save_dir + r"\*.jpg") + glob.glob(save_dir + r"\*.png")

        for file_path in file_paths:
            result_image_path = file_path

        print(result_image_path)

        return result_image_path

    def show_result_image(self, result_image_path):
        pixmap = QPixmap(result_image_path)
        self.result_label.setPixmap(pixmap.scaledToWidth(800))


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
