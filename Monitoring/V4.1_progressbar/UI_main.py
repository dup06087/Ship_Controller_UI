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
        # self.msleep(delay_ms)

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

        self.sensor_widget_list = [uic.loadUi("each_sensor.ui") for _ in range(25)]

        self.current_row = 0
        self.current_column = 0
        self.max_column_count = 4
        self.current_idx =  self.current_row * (self.max_column_count + 1) + self.current_column

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

    def closeEvent(self, event):
        try:
            if self.threading.isRunning():
                close = self.alert()
                if close == QMessageBox.Yes:
                    event.accept()
                else:
                    event.ignore()
        except:
            pass

    def alert(self):
        return QMessageBox.question(self,"Warning", "Are you sure want to quit?? \nYou might have a severe damage", QMessageBox.Yes,QMessageBox.No)

    def OK_Clicked(self):
        print("어디서지?1")
        self.bin_file = self.edit_bin_file.text()
        self.port = "COM" + self.edit_port_number.text()
        if self.checkBox.checkState():
            self.skip_checksum = True

        self.buttonBox.setEnabled(False)
        #
        print(self.bin_file, self.port, self.skip_checksum)
        print(type(self.bin_file), type(self.port), type(self.skip_checksum))

        self.worker = Worker(self.bin_file, self.port, self.skip_checksum, self.progressBar)
        self.worker.finished_signal.connect(self.onFinished)
        self.worker.progress_signal.connect(self.show_log)
        self.worker.start()

    def show_log(self, message):
        self.lbl_log.setText(str(message))

    def onFinished(self):

        print("end!!")
        # QMessageBox.information(self, 'Finished', 'Task is finished.')

    def done_clicked(self):
        os.execl(sys.executable, sys.executable, *sys.argv)
        # main_window.buttonBox.setEnabled(True)