import os
import sys
import time

import PyQt5
import numpy as np
import qtmodern.styles
import qtmodern.windows
import serial
from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal, QTimer
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox
import upload_bin_func_and_debug_func
import gc


form_window = uic.loadUiType("UI_V4_proto1.ui")[0]
# os.system("pyuic5 -o UI_V4_proto1.py UI_V4_proto1.ui")
#
# from UI_V4_proto1 import *

global count
count = 0

class Worker(QThread):
    finished_signal = pyqtSignal()
    progress_signal = pyqtSignal(str)

    def __init__(self, bin_file, port, skip_checksum, progress_bar):
        super().__init__()
        self.bin_file = bin_file
        self.port = port
        self.skip_checksum = skip_checksum
        self.progress_bar = progress_bar

    def print_to_label(self, text, delay_ms = 1):
        self.progress_signal.emit(text)

    def run(self):
        try:
            if upload_bin_func_and_debug_func.main_func(self.bin_file, self.port, self.skip_checksum, self.progress_bar, self.print_to_label):
                self.finished_signal.emit()
        except Exception as e:
            print("An error occurred while running upload_bin_func_and_debug_func.main_func():", e)

class UiMainWindow(QtWidgets.QMainWindow, form_window):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Firmware Update")
        self.setupUi(self)
        self.bin_file = "./vcu_f413zh_mbed.NUCLEO_F413ZH.bin"
        self.port = "9"
        self.skip_checksum = False
        self.edit_bin_file.setText(self.bin_file)
        self.edit_port_number.setText(self.port)

        self.progressBar.setMaximum(100)
        self.progressBar.setValue(count)

        self.btn_done.setEnabled(False)
        self.btn_done.clicked.connect(self.done_clicked)

        # self.btn_done.setDisabled(True)
        # self.each_sensor_format = uic.loadUiType("each_sensor.ui")
        # self.gridlayout_sensors.setColumnMinimumWidth(1,1) # 각 센서 widget 최소 크기
        ###초기화 잘해주기

        #set sensor1
        self.widget_sensor1.units = "Km/h"
        self.widget_sensor1.setGaugeTheme(3)
        self.widget_sensor1.enableBarGraph = True
        self.widget_sensor1.setMouseTracking(False)
        self.widget_sensor1.maxValue = 550
        self.widget_sensor1.minValue = 490
        self.widget_sensor1.updateValue(500)

        self.widget_sensor2.enableBarGraph = True
        self.widget_sensor2.setMouseTracking(False)

        self.setWindowFlags(self.windowFlags() | PyQt5.QtCore.Qt.WindowStaysOnTopHint)



    def clicked_file_dialog(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "All Files (*)",
                                                  options=options)
        if fileName:
            print(fileName)
            self.edit_bin_file.setText(fileName)

    def OK_Clicked(self):
        print("어디서지?1")
        self.bin_file = self.edit_bin_file.text()
        self.port = "COM" + self.edit_port_number.text()

        if self.checkBox.checkState():
            self.skip_checksum = True
        self.buttonBox.setEnabled(False)
        self.tabWidget.tabBar().setEnabled(False)
        self.pushButton.setEnabled(False)
        self.checkBox.setEnabled(False)
        self.btn_done.setEnabled(False)

        self.worker = Worker(self.bin_file, self.port, self.skip_checksum, self.progressBar)
        self.worker.finished_signal.connect(self.onFinished)
        self.worker.progress_signal.connect(self.show_log)
        self.worker.start()

    def show_log(self, message):
        self.lbl_log.setText(str(message))

    def onFinished(self):
        self.btn_done.setEnabled(True)

    def done_clicked(self):
        # 다른 필요한 작업을 수행한 후
        self.worker.finished_signal.disconnect(self.onFinished)  # 시그널 연결 해제
        self.worker.progress_signal.disconnect(self.show_log)  # 시그널 연결 해제
        self.worker.quit()  # 스레드 종료
        self.worker.wait()  # 스레드 완료까지 기다림
        self.worker.deleteLater()  # 스레드 리소스를 삭제하도록 예약
        self.worker = None  # 참조를 None으로 설정하여 메모리에서 삭제되도록 함
        gc.collect()  # 가비지 콜렉터를 호출하여 메모리를 정리

        self.buttonBox.setEnabled(True)
        self.tabWidget.tabBar().setEnabled(True)
        self.pushButton.setEnabled(True)
        self.checkBox.setEnabled(True)
        self.btn_done.setEnabled(False)
        self.progressBar.setValue(0)

