import sys
import os
import psutil
from requests import get
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtGui import QIcon, QIntValidator
from PyQt5.QtCore import QSize

form_class = uic.loadUiType("./design.ui")[0]


class MainClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("EasyBukkit")
        self.setWindowIcon(QIcon("paper.png"))

        self.setFixedSize(QSize(535, 528))

        self.only_integer(self.MaxLine)
        self.only_integer(self.MiniLine)

        self.version1192.clicked.connect(self.select_version)
        self.version1171.clicked.connect(self.select_version)
        self.version1165.clicked.connect(self.select_version)
        self.version1152.clicked.connect(self.select_version)
        self.version1144.clicked.connect(self.select_version)
        self.version1132.clicked.connect(self.select_version)
        self.version1122.clicked.connect(self.select_version)

        self.Start.clicked.connect(self.start_bukkit)
        # self.End.clicked.connect(self.end_bukkit)

    def only_integer(self, select):
        select.setValidator(QIntValidator(self))
        select.setValidator(QIntValidator(1, 32767, self))

    def start_bukkit(self):
        if self.check_process_running("cmd"):
            QMessageBox.warning(self, "에러", "이미 버킷을 실행 중입니다.\n(CMD 실행 시, 오류가 발생할 수 있습니다.)")
            return
        path = self.PathLine.text()
        self.create_bukkit()
        self.download_bukkit(self.get_target_bukkit(), f"{path}\\paper.jar")
        try:
            os.chdir(path)
            os.startfile(f"{path}")
            os.startfile(f"{path}\\Run.bat")
        except FileNotFoundError as e:
            print(e)

    def check_process_running(self, process_name):
        for proc in psutil.process_iter():
            try:
                if process_name.lower() in proc.name().lower():
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False

    def download_bukkit(self, url, file_name):
        with open(file_name, "wb") as file:  # open in binary mode
            response = get(url)  # get request
            file.write(response.content)

    def get_target_bukkit(self):
        if self.version1192.isChecked():
            return "https://api.papermc.io/v2/projects/paper/versions/1.19.2/builds/138/downloads/paper-1.19.2-138.jar"
        if self.version1171.isChecked():
            return "https://api.papermc.io/v2/projects/paper/versions/1.17.1/builds/411/downloads/paper-1.17.1-411.jar"
        if self.version1165.isChecked():
            return "https://api.papermc.io/v2/projects/paper/versions/1.16.5/builds/794/downloads/paper-1.16.5-794.jar"
        if self.version1152.isChecked():
            return "https://api.papermc.io/v2/projects/paper/versions/1.15.2/builds/393/downloads/paper-1.15.2-393.jar"
        if self.version1144.isChecked():
            return "https://api.papermc.io/v2/projects/paper/versions/1.14.4/builds/245/downloads/paper-1.14.4-245.jar"
        if self.version1132.isChecked():
            return "https://api.papermc.io/v2/projects/paper/versions/1.13.2/builds/657/downloads/paper-1.13.2-657.jar"
        if self.version1122.isChecked():
            return "https://api.papermc.io/v2/projects/paper/versions/1.12.2/builds/1620/downloads/paper-1.12.2-1620.jar"

    def create_bukkit(self):
        path = self.PathLine.text()
        max_ram = self.MaxLine.text()
        mini_ram = self.MiniLine.text()
        max_byte = self.get_ram(self.MaxByte)
        mini_byte = self.get_ram(self.MiniByte)

        if path == "":
            QMessageBox.warning(self, "에러", "경로가 설정되어 있지 않습니다.")
            return

        try:
            os.makedirs(path)
        except FileExistsError as e:
            print(e)

        with open(f"{path}\\Run.bat", "w+") as start:
            start.write("@echo off")
            start.write(f"\njava -Xmx{max_ram}{max_byte} -Xms{mini_ram}{mini_byte} -jar paper.jar{self.get_nogui()}")
            start.write("\npause")

        with open(f"{path}\\eula.txt", "w+", encoding="utf-8") as eula_file:
            if self.Eula.isChecked():
                eula = "true"
            else:
                eula = "false"

            eula_file.write(f"eula={eula}")

    def get_ram(self, select):
        return select.currentText().replace("B", "")

    def get_nogui(self):
        if self.NoGui.isChecked():
            return " nogui"
        return ""

    def select_version(self):
        if self.version1192.isChecked():
            self.PathLine.setText("C:\\EasyBukkit\\1.19.2")
            return
        if self.version1171.isChecked():
            self.PathLine.setText("C:\\EasyBukkit\\1.17.1")
            return
        if self.version1165.isChecked():
            self.PathLine.setText("C:\\EasyBukkit\\1.16.5")
            return
        if self.version1152.isChecked():
            self.PathLine.setText("C:\\EasyBukkit\\1.15.2")
            return
        if self.version1144.isChecked():
            self.PathLine.setText("C:\\EasyBukkit\\1.14.4")
            return
        if self.version1132.isChecked():
            self.PathLine.setText("C:\\EasyBukkit\\1.13.2")
            return
        if self.version1122.isChecked():
            self.PathLine.setText("C:\\EasyBukkit\\1.12.2")
            return


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MainClass()
    myWindow.show()
    app.exec_()

# import sys
# from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QGroupBox, QRadioButton, QCheckBox, QPushButton, \
#     QMenu, QGridLayout, QVBoxLayout, QLineEdit, QLabel
# from PyQt5.QtGui import QIcon, QIntValidator
#
#
# class EasyBukkit(QWidget):
#
#     def __init__(self):
#         super().__init__()
#         self.create_ui()
#
#     # GUI 생성
#     def create_ui(self):
#         grid = QGridLayout()
#         grid.addWidget(self.create_version_box(), 0, 0)
#         grid.addWidget(self.create_setting_box(), 0, 1)
#         self.setLayout(grid)
#
#         self.setWindowTitle("EasyBukkit")
#         self.setWindowIcon(QIcon("paper.png"))
#         self.resize(1000, 600)
#         self.center()
#         self.show()
#
#     def create_version_box(self):
#         groupbox = QGroupBox("버전")
#
#         version1 = QRadioButton("1.19")
#         version2 = QRadioButton("1.17.1")
#         version3 = QRadioButton("1.12.2")
#         version4 = QRadioButton("1.7.10")
#         version5 = QRadioButton("1.6.4")
#         version6 = QRadioButton("1.5.2")
#         version1.setChecked(True)
#
#         vbox = QVBoxLayout()
#         vbox.addWidget(version1)
#         vbox.addWidget(version2)
#         vbox.addWidget(version3)
#         vbox.addWidget(version4)
#         vbox.addWidget(version5)
#         vbox.addWidget(version6)
#         vbox.addStretch(1)
#         groupbox.setLayout(vbox)
#
#         return groupbox
#
#     def create_setting_box(self):
#         groupbox = QGroupBox("설정")
#         groupbox.setFlat(True)
#
#         max_ram = QLineEdit()
#         max_ram.setValidator(QIntValidator(1, 100, self))
#
#         mini_ram = QLineEdit()
#         mini_ram.setValidator(QIntValidator(1, 100, self))
#
#         checkbox2 = QCheckBox("Checkbox2")
#         checkbox2.setChecked(True)
#
#         checkbox3 = QCheckBox("Tri-state Button")
#
#         vbox = QVBoxLayout()
#         vbox.addWidget(QLabel('Ram:'), 0)
#         vbox.addWidget(QLabel('Ram:'), 1)
#         vbox.addWidget(max_ram)
#         vbox.addWidget(mini_ram)
#         vbox.addWidget(checkbox2)
#         vbox.addWidget(checkbox3)
#         vbox.addStretch(1)
#         groupbox.setLayout(vbox)
#
#         return groupbox
#
#     # 중앙 설정 메서드
#     def center(self):
#         qr = self.frameGeometry()
#         cp = QDesktopWidget().availableGeometry().center()
#         qr.moveCenter(cp)
#         self.move(qr.topLeft())
#
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = EasyBukkit()
#     sys.exit(app.exec_())
