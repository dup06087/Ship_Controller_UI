import os
import sys
import threading
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

class Worker_update(QThread):
    finished_signal_update = pyqtSignal()
    progress_signal_update = pyqtSignal(str)

    def __init__(self, bin_file, port, skip_checksum, progress_bar):
        super().__init__()
        self.bin_file = bin_file
        self.port = port
        self.skip_checksum = skip_checksum
        self.progress_bar = progress_bar
        print("됐나??")

    def print_to_label(self, text, delay_ms = 1):
        self.progress_signal_update.emit(text)

    def run(self):

        print("run well?")
        try:
            print('dd')
            try:
                upload_bin_func_and_debug_func.main_func(self.bin_file, self.port, self.skip_checksum,
                                                         self.progress_bar, self.print_to_label)
            except:
                print("nope")
        except Exception as e:
            print("An error occurred while running upload_bin_func_and_debug_func.main_func():", e)

class Worker_sensor(threading.Thread):
    def __init__(self, port, progress_bar):
        super().__init__()
        self.port = port
        self.progress_bar = progress_bar
        self.running = True
        self.communication = upload_bin_func_and_debug_func
    def print_to_label(self, text, delay_ms=1):
        print(text)
        # self.progress_signal_update.emit(text)
        # pass

    def run(self):
        while self.running:
            try:
                self.communication.main_func2(self.port, self.print_to_label)
                # upload_bin_func_and_debug_func.main_func2(self.port, self.print_to_label)
            except Exception as e:
                print("An error occurred while running upload_bin_func_and_debug_func.main_func():", e)

    def stop(self):
        self.running = False


class WorkerThread(QThread):
    update_signal = pyqtSignal()

    def __init__(self):
        super().__init__()

    def run(self):
        while True:
            self.update_signal.emit()
            self.sleep(1)  # 1초마다 시그널을 발생시킵니다.

class UiMainWindow(QtWidgets.QMainWindow, form_window):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Firmware Update")
        self.setupUi(self)
        self.bin_file = "./vcu_f413zh_mbed.NUCLEO_F413ZH.bin"
        self.port = "COM9"
        self.skip_checksum = False
        self.edit_bin_file.setText(self.bin_file)
        self.edit_port_number.setText(self.port[-1])

        self.progressBar.setMaximum(100)
        self.progressBar.setValue(count)

        self.btn_done.setEnabled(False)
        self.btn_done.clicked.connect(self.done_clicked)

        self.sensor_values = {}

        #set sensor1
        self.gauge_sensor1.units = "Km/h"
        self.gauge_sensor1.setGaugeTheme(3)
        self.gauge_sensor1.enableBarGraph = True
        self.gauge_sensor1.setMouseTracking(False)
        self.gauge_sensor1.maxValue = 255
        self.gauge_sensor1.minValue = 0
        self.gauge_sensor1.updateValue(0)

        self.gauge_sensor2.enableBarGraph = True
        self.gauge_sensor2.setMouseTracking(False)
        self.gauge_sensor2.maxValue = 255
        self.gauge_sensor2.minValue = 0
        self.gauge_sensor2.updateValue(0)

        self.gauge_sensor3.maxValue = 255
        self.gauge_sensor3.minValue = 0
        self.gauge_sensor3.updateValue(0)

        self.setWindowFlags(self.windowFlags() | PyQt5.QtCore.Qt.WindowStaysOnTopHint)

        '''여기가 센서'''
        self.worker_sensor = Worker_sensor(self.port, self.progressBar)
        self.worker_sensor.start()

        self.worker_thread = WorkerThread()
        self.worker_thread.update_signal.connect(self.update_value)
        self.worker_thread.update_signal.connect(self.update_ui)
        self.worker_thread.start()
        '''센서 끝'''

    def update_value(self):
        print("1초마다 실행되는 코드")
        time = self.worker_sensor.communication.ds3231_time_u32
        date = self.worker_sensor.communication.ds3231_date_str
        sensor1_b0 = self.worker_sensor.communication.test_module1_u8_B0
        sensor1_b1 = self.worker_sensor.communication.test_module1_u8_B1
        sensor1_b7 = self.worker_sensor.communication.test_module1_u8_B7
        sensor2_b0 = self.worker_sensor.communication.test_module2_u8_B0
        sensor2_b1 = self.worker_sensor.communication.test_module2_u8_B1
        sensor2_b7 = self.worker_sensor.communication.test_module2_u8_B7

        new_sensor_values = {"time": time, "date" : date, "sensor1" : sensor1_b0, "sensor2" : sensor1_b1, "sensor3" : sensor1_b7, "sensor4" : sensor2_b0, "sensor5" : sensor2_b1, "sensor6" : sensor2_b7}
        # self.sensor_values = new_sensor_values

        if self.sensor_values != new_sensor_values:
            self.sensor_values = new_sensor_values
            self.update_combobox()


    def update_ui(self):
        self.gauge_sensor1.updateValue(float(self.worker_sensor.communication.test_module1_u8_B0))
        self.gauge_sensor2.updateValue(float(self.worker_sensor.communication.test_module1_u8_B1))
        self.gauge_sensor3.updateValue(float(self.worker_sensor.communication.test_module2_u8_B0))

        combo_box_list = self.findChildren(QtWidgets.QComboBox)

        for combo_box in combo_box_list:
            current_text = combo_box.currentText()

            label_object_name = combo_box.objectName().replace("combo", "lbl")
            label = self.findChild(QtWidgets.QLabel, label_object_name)
            if label is not None:
                label_value = self.sensor_values.get(current_text)
                if label_value is not None:
                    label.setText(str(label_value))

    def update_combobox(self):
        combo_box_list = self.findChildren(QtWidgets.QComboBox)
        # 가져온 QComboBox 객체 리스트를 출력한다.
        for combo_box in combo_box_list:
            current_text = combo_box.currentText()
            combo_box.blockSignals(True)
            combo_box.clear()
            combo_box.addItems(map(str, self.sensor_values.keys()))

            index = combo_box.findText(current_text)
            combo_box.setCurrentIndex(index)
            combo_box.blockSignals(False)  # 시그널 활성화



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


        self.worker_update = Worker_update(self.bin_file, self.port, self.skip_checksum, self.progressBar)
        print("멈춤")
        # self.worker_update.finished_signal_update.connect(self.onFinished)
        # self.worker_update.progress_signal_update.connect(self.show_log)
        self.worker_update.start()

        print("여기는??")

    def show_log(self, message):
        self.lbl_log.setText(str(message))

    def onFinished(self):
        self.btn_done.setEnabled(True)

    def done_clicked(self):
        # 다른 필요한 작업을 수행한 후
        self.worker1.finished_signal.disconnect(self.onFinished)  # 시그널 연결 해제
        self.worker1.progress_signal.disconnect(self.show_log)  # 시그널 연결 해제
        self.worker1.quit()  # 스레드 종료
        self.worker1.wait()  # 스레드 완료까지 기다림
        self.worker1.deleteLater()  # 스레드 리소스를 삭제하도록 예약
        self.worker1 = None  # 참조를 None으로 설정하여 메모리에서 삭제되도록 함
        gc.collect()  # 가비지 콜렉터를 호출하여 메모리를 정리

        self.buttonBox.setEnabled(True)
        self.tabWidget.tabBar().setEnabled(True)
        self.pushButton.setEnabled(True)
        self.checkBox.setEnabled(True)
        self.btn_done.setEnabled(False)
        self.progressBar.setValue(0)