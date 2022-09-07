import sys
import os
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtGui import QIcon, QIntValidator

form_class = uic.loadUiType("./design.ui")[0]


class MainClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon("paper.png"))

        self.only_integer(self.MaxLine)
        self.only_integer(self.MiniLine)

        self.version119.clicked.connect(self.select_version)
        self.version1171.clicked.connect(self.select_version)
        self.version1122.clicked.connect(self.select_version)
        self.version1710.clicked.connect(self.select_version)
        self.version164.clicked.connect(self.select_version)
        self.version152.clicked.connect(self.select_version)

        self.Start.clicked.connect(self.start_bukkit)
        # self.End.clicked.connect(self.end_bukkit)

    def only_integer(self, select):
        select.setValidator(QIntValidator(self))
        select.setValidator(QIntValidator(1, 32767, self))

    def start_bukkit(self):
        self.create_bukkit()

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

        with open(f"{path}\\Start.bat", "w+") as start:
            start.write("@echo off")
            start.write(f"\njava -Xmx{max_ram}{max_byte} -Xms{mini_ram}{mini_byte} -jar paper.jar{self.get_nogui()}")

    def get_ram(self, select):
        return select.currentText().replace("B", "")

    def get_nogui(self):
        if self.NoGui.isChecked():
            return " nogui"
        return ""

    def select_version(self):
        if self.version119.isChecked():
            self.PathLine.setText("C:\\EasyBukkit\\1.19")
            return
        if self.version1171.isChecked():
            self.PathLine.setText("C:\\EasyBukkit\\1.17.1")
            return
        if self.version1122.isChecked():
            self.PathLine.setText("C:\\EasyBukkit\\1.12.2")
            return
        if self.version1710.isChecked():
            self.PathLine.setText("C:\\EasyBukkit\\1.7.10")
            return
        if self.version164.isChecked():
            self.PathLine.setText("C:\\EasyBukkit\\1.6.4")
            return
        if self.version152.isChecked():
            self.PathLine.setText("C:\\EasyBukkit\\1.5.2")
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
