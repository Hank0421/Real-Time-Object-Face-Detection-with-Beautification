import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QFileDialog, QHBoxLayout, QCheckBox, QComboBox
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
from object_detector import ObjectDetector
from face_beautifier import FaceBeautifier

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("即時影像處理")

        self.image_label = QLabel()
        self.gray_checkbox = QCheckBox("灰階")
        self.blur_checkbox = QCheckBox("模糊")
        self.edge_checkbox = QCheckBox("邊緣偵測")
        self.beautify_checkbox = QCheckBox("美顏")

        self.mode_selector = QComboBox()
        self.mode_selector.addItems(["原始模式", "物件偵測模式"])
        self.mode_selector.currentIndexChanged.connect(self.change_mode)

        self.load_button = QPushButton("載入圖片")
        self.load_button.clicked.connect(self.load_image_from_file)

        self.camera_button = QPushButton("開啟攝影機")
        self.camera_button.clicked.connect(self.start_camera)


        self.reset_button = QPushButton("重設")
        self.reset_button.clicked.connect(self.reset_image)

        self.save_button = QPushButton("儲存圖片")
        self.save_button.clicked.connect(self.save_image)


        button_layout = QHBoxLayout()
        button_layout.addWidget(self.gray_checkbox)
        button_layout.addWidget(self.blur_checkbox)
        button_layout.addWidget(self.edge_checkbox)
        button_layout.addWidget(self.beautify_checkbox)
        button_layout.addWidget(self.mode_selector)
        button_layout.addWidget(self.load_button)
        button_layout.addWidget(self.camera_button)
        button_layout.addWidget(self.reset_button)
        button_layout.addWidget(self.save_button)

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addLayout(button_layout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.cap = cv2.VideoCapture(0)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

        self.object_detector = ObjectDetector()
        self.face_beautifier = FaceBeautifier()

        self.current_image = None
        self.original_image = None
        self.mode = 'original'

        self.gray_checkbox.stateChanged.connect(self.apply_filters_to_static)
        self.blur_checkbox.stateChanged.connect(self.apply_filters_to_static)
        self.edge_checkbox.stateChanged.connect(self.apply_filters_to_static)
        self.beautify_checkbox.stateChanged.connect(self.apply_filters_to_static)

    def change_mode(self, index):
        self.mode = 'object' if index == 1 else 'original'
        self.apply_filters_to_static()

    def load_image_from_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "選擇圖片", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if file_name:
            image = cv2.imread(file_name)
            if image is not None:
                self.current_image = image.copy()
                self.original_image = image.copy()
                self.cap = None  # 停用攝影機
                self.apply_filters_to_static()

    def reset_image(self):
        if self.original_image is not None:
            self.current_image = self.original_image.copy()
            self.display_image(self.current_image)

        # 取消所有勾選框
        self.gray_checkbox.setChecked(False)
        self.blur_checkbox.setChecked(False)
        self.edge_checkbox.setChecked(False)
        self.beautify_checkbox.setChecked(False)


    def apply_filters_to_static(self):
        if self.cap is None and self.current_image is not None:
            processed = self.process_image(self.current_image.copy())
            if self.mode == 'object':
                results = self.object_detector.detect(processed)
                results.render()
                processed = results.ims[0]
            self.display_image(processed)

    def update_frame(self):
        if self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                processed = self.process_image(frame)
                if self.mode == 'object':
                    results = self.object_detector.detect(processed)
                    results.render()
                    processed = results.ims[0]
                self.display_image(processed)

    def process_image(self, frame):
        result = frame.copy()

        if self.gray_checkbox.isChecked():
            result = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
            result = cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)

        if self.blur_checkbox.isChecked():
            result = cv2.GaussianBlur(result, (15, 15), 0)

        if self.edge_checkbox.isChecked():
            gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 50, 150)
            result = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

        if self.beautify_checkbox.isChecked():
            if isinstance(result, np.ndarray):
                result = self.face_beautifier.beautify(result)

        return result

    def display_image(self, image):
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        self.image_label.setPixmap(QPixmap.fromImage(qt_image))
    
    def start_camera(self):
        if self.cap is None or not self.cap.isOpened():
            self.cap = cv2.VideoCapture(0)
        self.load_image = None  # 清除載入圖片
        self.timer.start(30)

    def save_image(self):
        # 攝影機開啟時，擷取當前畫面
        if self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                file_path, _ = QFileDialog.getSaveFileName(self, "儲存圖片", "", "PNG Files (*.png);;JPEG Files (*.jpg *.jpeg)")
                if file_path:
                    processed = self.process_image(frame)
                    if self.mode == 'object':
                        results = self.object_detector.detect(processed)
                        results.render()
                        processed = results.ims[0]
                    cv2.imwrite(file_path, processed)
            return
        # 靜態圖片模式
        if self.current_image is not None:
            file_path, _ = QFileDialog.getSaveFileName(self, "儲存圖片", "", "PNG Files (*.png);;JPEG Files (*.jpg *.jpeg)")
            if file_path:
                processed = self.process_image(self.current_image.copy())
                if self.mode == 'object':
                    results = self.object_detector.detect(processed)
                    results.render()
                    processed = results.ims[0]
                cv2.imwrite(file_path, processed)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
