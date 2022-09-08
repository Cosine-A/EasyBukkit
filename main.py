import sys
import os
import psutil
from requests import get
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtGui import QIcon, QIntValidator
from PyQt5.QtCore import QSize

form_class = uic.loadUiType("main.ui")[0]


class EasyBukkitMain(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("EasyBukkit")
        self.setWindowIcon(QIcon("paper.png"))

        self.setFixedSize(QSize(500, 400))

        self.only_integer(self.MaxLine)
        self.only_integer(self.MinLine)

        self.versions.currentTextChanged.connect(self.select_version)

        self.AllowFlight.stateChanged.connect(self.change_state)

        self.Start.clicked.connect(self.start_bukkit)
        # self.End.clicked.connect(self.end_bukkit)

        # 프로퍼티 설정
        self.TabBox.tabBarClicked.connect(self.setting_tab)

    def change_state(self):
        try:
            path = self.PathLine.text()
            read_server = open(f"{path}\\server.properties", "r")
            lines = read_server.readlines()
            read_server.close()

            with open(f"{path}\\server.properties", "w") as write_server:
                for line in lines:
                    if line.startswith("allow-flight"):
                        check = str(self.bool_to_str(self.AllowFlight.isChecked()))
                        line = line.replace("true", check).replace("false", check)
                        write_server.write(line)
                        print(line)
                    else:
                        write_server.write(line)

        except BaseException as e:
            print(e)

    def bool_to_str(self, state):
        if state:
            return "true"
        else:
            return "false"

    def setting_tab(self):
        path = self.PathLine.text()
        self.serverBox.setChecked(True)
        if os.path.exists(f"{path}\\server.properties"):
            self.serverBox.setEnabled(True)
        else:
            self.serverBox.setEnabled(False)

    def only_integer(self, select):
        select.setValidator(QIntValidator(self))
        select.setValidator(QIntValidator(1, 32767, self))

    def start_bukkit(self):
        path = self.PathLine.text()

        if self.versions.currentText() == "버전을 선택해주세요":
            QMessageBox.warning(self, "에러", "버전을 선택해주세요.")
            return

        if path == "":
            QMessageBox.warning(self, "에러", "경로가 설정되어 있지 않습니다.")
            return

        if self.check_process_running("cmd"):
            QMessageBox.warning(self, "에러", "이미 버킷을 실행 중입니다.\n(CMD 실행 시, 오류가 발생할 수 있습니다.)")
            return

        self.create_bukkit()
        self.download_bukkit(self.get_target_bukkit(), f"{path}\\paper.jar")
        self.run_bukkit(path)

    def run_bukkit(self, path):
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

    def create_bukkit(self):
        path = self.PathLine.text()
        max_ram = self.MaxLine.text()
        min_ram = self.MinLine.text()
        max_byte = self.get_ram(self.MaxByte)
        min_byte = self.get_ram(self.MinByte)
        nogui = self.get_nogui()
        eula = self.get_eula()

        self.create_folder(path)
        self.create_starter(path, max_ram, max_byte, min_ram, min_byte, nogui)
        self.create_eula(path, eula)

    def create_folder(self, path):
        try:
            os.makedirs(path)
        except FileExistsError as e:
            print(e)

    def create_starter(self, path, max_ram, max_byte, min_ram, min_byte, nogui):
        with open(f"{path}\\Run.bat", "w+") as start:
            start.write("@echo off")
            start.write(f"\njava -Xmx{max_ram}{max_byte} -Xms{min_ram}{min_byte} -jar paper.jar{nogui}")
            start.write("\npause")

    def create_eula(self, path, eula):
        with open(f"{path}\\eula.txt", "w+", encoding="utf-8") as eula_file:
            eula_file.write(f"eula={eula}")

    def get_ram(self, select):
        return select.currentText().replace("B", "")

    def get_eula(self):
        if self.CheckEula.isChecked():
            return "true"
        else:
            return "false"

    def get_nogui(self):
        if self.NoGui.isChecked():
            return " nogui"
        return ""

    def get_target_bukkit(self):
        if self.versions.currentText() == "1.19.2":
            return "https://api.papermc.io/v2/projects/paper/versions/1.19.2/builds/138/downloads/paper-1.19.2-138.jar"
        if self.versions.currentText() == "1.17.1":
            return "https://api.papermc.io/v2/projects/paper/versions/1.17.1/builds/411/downloads/paper-1.17.1-411.jar"
        if self.versions.currentText() == "1.16.5":
            return "https://api.papermc.io/v2/projects/paper/versions/1.16.5/builds/794/downloads/paper-1.16.5-794.jar"
        if self.versions.currentText() == "1.15.2":
            return "https://api.papermc.io/v2/projects/paper/versions/1.15.2/builds/393/downloads/paper-1.15.2-393.jar"
        if self.versions.currentText() == "1.14.4":
            return "https://api.papermc.io/v2/projects/paper/versions/1.14.4/builds/245/downloads/paper-1.14.4-245.jar"
        if self.versions.currentText() == "1.13.2":
            return "https://api.papermc.io/v2/projects/paper/versions/1.13.2/builds/657/downloads/paper-1.13.2-657.jar"
        if self.versions.currentText() == "1.12.2":
            return "https://api.papermc.io/v2/projects/paper/versions/1.12.2/builds/1620/downloads/paper-1.12.2-1620.jar"

    def select_version(self):
        if self.versions.currentText() == "버전을 선택해주세요":
            self.PathLine.setText("")
            return
        if self.versions.currentText() == "1.19.2":
            self.PathLine.setText("C:\\EasyBukkit\\1.19.2")
            return
        if self.versions.currentText() == "1.17.1":
            self.PathLine.setText("C:\\EasyBukkit\\1.17.1")
            return
        if self.versions.currentText() == "1.16.5":
            self.PathLine.setText("C:\\EasyBukkit\\1.16.5")
            return
        if self.versions.currentText() == "1.15.2":
            self.PathLine.setText("C:\\EasyBukkit\\1.15.2")
            return
        if self.versions.currentText() == "1.14.4":
            self.PathLine.setText("C:\\EasyBukkit\\1.14.4")
            return
        if self.versions.currentText() == "1.13.2":
            self.PathLine.setText("C:\\EasyBukkit\\1.13.2")
            return
        if self.versions.currentText() == "1.12.2":
            self.PathLine.setText("C:\\EasyBukkit\\1.12.2")
            return


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = EasyBukkitMain()
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
