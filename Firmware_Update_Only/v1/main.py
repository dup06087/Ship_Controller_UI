# -*- coding: utf-8 -*-
"""
Created on Sun Jan  1 14:38:33 2023

@author: USER
"""

# python C:\Users\USER\Desktop\STM32\upload_bin_func.py
# python C:\Users\USER\Documents\STM32\upload_bin_func.py

import sys
import time
import os

import numpy as np
import serial
import PyQt5
from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox

# bin_file = "C:/Users/USER/Desktop/STM32/BIN.bin"
# bin_file = "C:/Users/USER/Desktop/STM32/BIN2_F413ZH.bin"

form_window = uic.loadUiType("UI_V1.ui")[0]

class main_threading(QThread):

    # countChanged = pyqtSignal(int)
    # pyqtSignal(int)
    def run(self):
        # self.countChanged.emit("변수")
        print("HI")
        time.sleep(1)
        while True:
            try:
                if main_func(main_window.bin_file, main_window.port, main_window.skip_checksum):
                    main_window.child.pushButton.setEnabled(True)
                    break
                else:
                    main_window.child.textEdit.append("restart in 3 seconds")
                    time.sleep(3)
            except:
                pass

        # check_main_func = main_window.main_func(bin_file, port, skip_checksum)


class UiMainWindow(QtWidgets.QMainWindow, form_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.bin_file = "BIN2_F413ZH.bin"
        self.port = "11"
        self.skip_checksum = False
        self.lineEdit.setText(self.bin_file)
        self.lineEdit_2.setText(self.port)
        self.setWindowFlags(self.windowFlags() | PyQt5.QtCore.Qt.WindowStaysOnTopHint)

    def File_Dialog(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "All Files (*)",
                                                  options=options)
        if fileName:
            print(fileName)
            self.lineEdit.setText(fileName)

    def Checksum_ON_OFF(self):
        pass

    def Ok_Clicked(self):
        self.bin_file = self.lineEdit.text()
        self.port = "COM" + self.lineEdit_2.text()
        if self.checkBox.checkState():
            self.skip_checksum = True

        self.child = Child_window(self)

        QApplication.processEvents()

        thread = main_threading(self)
        thread.start()


app = QtWidgets.QApplication(sys.argv)
main_window = UiMainWindow()
main_window.show()


class Child_window(QtWidgets.QDialog):
    def __init__(self, main_window):  # 부모 window 설정
        super(Child_window, self).__init__(main_window)
        option_ui = './UI_Child.ui'
        uic.loadUi(option_ui, self)

        self.setWindowFlag(PyQt5.QtCore.Qt.WindowCloseButtonHint, False)
        self.textEdit.moveCursor(QtGui.QTextCursor.End)
        # self.textEdit.movePosition(QtGui.QTextCursor.End)
        # self.textEdit.moveCursor.movePosition(QtGui.QTextCursor.End)
        self.pushButton.setEnabled(False)
        self.pushButton.clicked.connect(self.Clicked)
        self.count = 0
        self.progressBar.setMaximum(100)
        self.progressBar.setValue(self.count)

        self.setWindowModality(Qt.ApplicationModal)
        self.show()

    def Clicked(self):
        sys.exit()


def read_bin(bin_file):
    try:

        with open(bin_file, "rb") as f:
            contents = f.read()

        main_window.child.textEdit.append("Found .bin file (%s)" % bin_file)
        time.sleep(3.0)

        # for i in range(len(contents) // 16):
        #    print("0x%08x: 0x%02x%02x%02x%02x 0x%02x%02x%02x%02x 0x%02x%02x%02x%02x 0x%02x%02x%02x%02x" % (16*i, contents[16*i + 3], contents[16*i + 2], contents[16*i + 1], contents[16*i + 0], contents[16*i + 7], contents[16*i + 6], contents[16*i + 5], contents[16*i + 4], contents[16*i + 11], contents[16*i + 10], contents[16*i + 9], contents[16*i + 8], contents[16*i + 15], contents[16*i + 14], contents[16*i + 13], contents[16*i + 12]))
        # if len(contents) % 16 != 0:
        #    temp = ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "]
        #    for i in range(16):
        #        if (len(contents) // 16) * 16 + i < len(contents):
        #            temp[i] = "%02x" % contents[(len(contents) // 16) * 16 + i]
        #    print("0x%08x: 0x%02s%02s%02s%02s 0x%02s%02s%02s%02s 0x%02s%02s%02s%02s 0x%02s%02s%02s%02s" % ((len(contents) // 16) * 16, temp[3], temp[2], temp[1], temp[0], temp[7], temp[6], temp[5], temp[4], temp[11], temp[10], temp[9], temp[8], temp[15], temp[14], temp[13], temp[12]))

        # for i in range(len(contents) // 16):
        #     print("0x%08x: 0x%02x 0x%02x 0x%02x 0x%02x 0x%02x 0x%02x 0x%02x 0x%02x 0x%02x 0x%02x 0x%02x 0x%02x 0x%02x 0x%02x 0x%02x 0x%02x" % (16*i, contents[16*i + 0], contents[16*i + 1], contents[16*i + 2], contents[16*i + 3], contents[16*i + 4], contents[16*i + 5], contents[16*i + 6], contents[16*i + 7], contents[16*i + 8], contents[16*i + 9], contents[16*i + 10], contents[16*i + 11], contents[16*i + 12], contents[16*i + 13], contents[16*i + 14], contents[16*i + 15]))
        if len(contents) % 16 != 0:
            temp = ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "]
            for i in range(16):
                if (len(contents) // 16) * 16 + i < len(contents):
                    temp[i] = "%02x" % contents[(len(contents) // 16) * 16 + i]
            # print("0x%08x: 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s" % ((len(contents) // 16) * 16, temp[0], temp[1], temp[2], temp[3], temp[4], temp[5], temp[6], temp[7], temp[8], temp[9], temp[10], temp[11], temp[12], temp[13], temp[14], temp[15]))

        # crc = 0x00000000
        # for i in range(len(contents)):
        #    crc = crc + int(("0x%02x" % contents[i]), 16)
        #    crc = crc & 0xffffffff
        # print("Checksum (0x%08x - 0x%08x): 0x%08x, %d bytes" % (0x00000000, len(contents) - 1, crc, len(contents)))

        crc = np.uint32(0x00000000)
        for i in range(len(contents)):
            crc = crc + np.uint32(int(("0x%02x" % contents[i]), 16))
        main_window.child.textEdit.append(
            "Checksum (0x%08x - 0x%08x): 0x%08x, %d bytes" % (0x00000000, len(contents) - 1, crc, len(contents)))

        if len(contents) % 128 == 0:
            num_128 = len(contents) // 128
        else:
            num_128 = (len(contents) // 128) + 1

        # crc_128 = 0x00000000
        # for i in range(num_128 * 128):
        #    if i < len(contents):
        #        crc_128 = crc_128 + int(("0x%02x" % contents[i]), 16)
        #    else:
        #        crc_128 = crc_128 + int(("0x%02x" % 0xff), 16)
        #    crc_128 = crc_128 & 0xffffffff
        # print("Checksum (0x%08x - 0x%08x): 0x%08x, %d bytes" % (0x00000000, (num_128 * 128) - 1, crc_128, (num_128 * 128)))

        crc_128 = np.uint32(0x00000000)
        for i in range(num_128 * 128):
            if i < len(contents):
                crc_128 = crc_128 + np.uint32(int(("0x%02x" % contents[i]), 16))
            else:
                crc_128 = crc_128 + np.uint32(int(("0x%02x" % 0xff), 16))
        main_window.child.textEdit.append("Checksum (0x%08x - 0x%08x): 0x%08x, %d bytes" % (
        0x00000000, (num_128 * 128) - 1, crc_128, (num_128 * 128)))

        main_window.child.textEdit.append("")
        time.sleep(3.0)

        return True, contents, crc, num_128, crc_128
    except:
        main_window.child.textEdit.append("Can not find .bin file (%s)" % bin_file)

        main_window.child.textEdit.append("")
        time.sleep(3.0)

        main_window.child.textEdit.moveCursor(QtGui.QTextCursor.End)
        return False, b'', np.uint32(0x00000000), 0, np.uint32(0x00000000)


def open_serial(port):
    try:
        ser = serial.Serial(port)
        ser.baudrate = 115200

        main_window.child.textEdit.append("Opened %s" % port)

        main_window.child.textEdit.append("")
        time.sleep(3.0)

        check_ser = True
        # ser = ser
    except:
        main_window.child.textEdit.append("Can not open %s" % port)

        main_window.child.textEdit.append("")
        time.sleep(3.0)

        check_ser = False
        ser = False

    main_window.child.textEdit.moveCursor(QtGui.QTextCursor.End)
    return check_ser, ser


def check_serial(check_ser, ser):
    if check_ser == True:
        try:
            while ser.in_waiting > 0:
                data_dummy = ser.read()

            main_window.child.textEdit.append("%s is alive" % main_window.port)

            main_window.child.textEdit.append("")
            time.sleep(3.0)

            check_ser = True
        except:
            main_window.child.textEdit.append("%s is dead" % main_window.port)

            main_window.child.textEdit.append("")
            time.sleep(3.0)

            check_ser = False
    else:
        main_window.child.textEdit.append("Can not found serial port")

        main_window.child.textEdit.append("")
        time.sleep(3.0)

        # check_ser = False

    main_window.child.textEdit.moveCursor(QtGui.QTextCursor.End)
    return check_ser


def close_serial(check_ser, ser):
    if check_ser == True:
        try:
            ser.close()

            main_window.child.textEdit.append("Closed %s" % ser.port)

            main_window.child.textEdit.append("")
            time.sleep(3.0)

            check_ser = False
        except:
            main_window.child.textEdit.append("Can not close serial port")

            main_window.child.textEdit.append("")
            time.sleep(3.0)

            check_ser = False
    else:
        main_window.child.textEdit.append("Can not found serial port")

        main_window.child.textEdit.append("")
        time.sleep(3.0)

        # check_ser = False

    main_window.child.textEdit.moveCursor(QtGui.QTextCursor.End)
    return check_ser


def check_hse_frequency(check_ser, ser):
    if check_ser == True:
        try:
            data_dummy = b't0048ffffffffffffffff\r'
            for i in range(16):
                ser.write(data_dummy)
                time.sleep(0.05)

            while ser.in_waiting > 0:
                data_dummy = ser.read()

            request = b't079100\r'
            for i in range(20):
                ser.write(request)
                time.sleep(0.05)
            # main_window.child.textEdit.append("Sent: %s\\r" % request[0:-1].decode("utf-8"))
            time.sleep(0.01)

            response = b''
            prev_time = time.time()
            while True:
                if ser.in_waiting > 0:
                    data_rx = ser.read()
                    # print(data_rx)
                    response = response + data_rx
                    if data_rx == b'\r':
                        # print("Recv: %s\\r" % response[0:-1].decode("utf-8"))
                        if response == b't079179\r':
                            main_window.child.textEdit.append("Check HSE frequency Response Done (ACK)")

                            check_check_hse_frequency = True
                            check_check_hse_frequency_opt = True

                            break
                        elif response == b't07911f\r':
                            main_window.child.textEdit.append("Check HSE frequency Response Failed (NACK)")

                            check_check_hse_frequency = True
                            check_check_hse_frequency_opt = False

                            break
                        else:
                            main_window.child.textEdit.append("Check HSE frequency Response Failed (Missing data)")

                            check_check_hse_frequency = False
                            check_check_hse_frequency_opt = True

                            break
                if time.time() >= prev_time + 1.0:
                    # main_window.child.textEdit.append("Recv: %s" % response[0:].decode("utf-8"))
                    main_window.child.textEdit.append("Check HSE frequency Response Failed (Timeout)")

                    check_check_hse_frequency = False
                    check_check_hse_frequency_opt = False

                    break

            time.sleep(1.0)
            while ser.in_waiting > 0:
                data_dummy = ser.read()

            if check_check_hse_frequency == True:
                if check_check_hse_frequency_opt == True:
                    main_window.child.textEdit.append("Checked HSE frequency")
                else:
                    main_window.child.textEdit.append("Already checked HSE frequency")
            else:
                main_window.child.textEdit.append("Can not check HSE frequency")

            main_window.child.textEdit.append("")
            time.sleep(3.0)
        except:
            main_window.child.textEdit.append("Can not check HSE frequency")
            main_window.child.textEdit.append("Can not use %s" % ser.port)

            main_window.child.textEdit.append("")
            time.sleep(3.0)

            check_check_hse_frequency = False
            check_check_hse_frequency_opt = False
    else:
        main_window.child.textEdit.append("Can not check HSE frequency")
        main_window.child.textEdit.append("Can not find serial port")

        main_window.child.textEdit.append("")
        time.sleep(3.0)

        check_check_hse_frequency = False
        check_check_hse_frequency_opt = False

    main_window.child.textEdit.moveCursor(QtGui.QTextCursor.End)
    return check_check_hse_frequency, check_check_hse_frequency_opt


def get_ID(check_ser, ser):
    if check_ser == True:
        try:
            while ser.in_waiting > 0:
                data_dummy = ser.read()

            request = b't002100\r'
            ser.write(request)
            # print("Sent: %s\\r" % request[0:-1].decode("utf-8"))
            time.sleep(0.01)

            response = b''
            prev_time = time.time()
            while True:
                if ser.in_waiting > 0:
                    data_rx = ser.read()
                    # print(data_rx)
                    response = response + data_rx
                    if data_rx == b'\r':
                        # print("Recv: %s\\r" % response[0:-1].decode("utf-8"))
                        if response == b't002179\r':
                            main_window.child.textEdit.append("Get ID Request Done (ACK)")

                            check_id = True

                            break
                        elif response == b't00211f\r':
                            main_window.child.textEdit.append("Get ID Request Failed (NACK)")

                            check_id = False

                            break
                        else:
                            main_window.child.textEdit.append("Get ID Request Failed (Unknown)")

                            check_id = False

                            break
                if time.time() >= prev_time + 1.0:
                    # print("Recv: %s" % response[0:].decode("utf-8"))
                    main_window.child.textEdit.append("Get ID Request Failed (Timeout)")

                    check_id = False

                    break

            response = b''
            prev_time = time.time()
            while True:
                if ser.in_waiting > 0:
                    data_rx = ser.read()
                    # print(data_rx)
                    response = response + data_rx
                    if data_rx == b'\r':
                        # print("Recv: %s\\r" % response[0:-1].decode("utf-8"))
                        if response[0:5] == b't0022':
                            if response[5:10] == b'0421\r':
                                main_window.child.textEdit.append(
                                    "Get ID Done (ID: 0x%03s (STM32F446xx))" % response[6:9].decode("utf-8"))

                                chip_id = int(("0x%03s" % response[6:9].decode("utf-8")), 16)

                                break
                            elif response[5:10] == b'0463\r':
                                main_window.child.textEdit.append(
                                    "Get ID Done (ID: 0x%03s (STM32F413xx))" % response[6:9].decode("utf-8"))

                                chip_id = int(("0x%03s" % response[6:9].decode("utf-8")), 16)

                                break
                            else:
                                main_window.child.textEdit.append(
                                    "Get ID Done (ID: 0x%03s)" % response[6:9].decode("utf-8"))

                                chip_id = int(("0x%03s" % response[6:9].decode("utf-8")), 16)

                                break
                        else:
                            main_window.child.textEdit.append("Get ID Failed (Unknown)")

                            chip_id = 0x000

                            break
                if time.time() >= prev_time + 1.0:
                    # print("Recv: %s" % response[0:].decode("utf-8"))
                    main_window.child.textEdit.append("Get ID Failed (Timeout)")

                    chip_id = 0x000

                    break

            response = b''
            prev_time = time.time()
            while True:
                if ser.in_waiting > 0:
                    data_rx = ser.read()
                    # print(data_rx)
                    response = response + data_rx
                    if data_rx == b'\r':
                        # print("Recv: %s\\r" % response[0:-1].decode("utf-8"))
                        if response == b't002179\r':
                            main_window.child.textEdit.append("Get ID Response Done (ACK)")

                            check_id = True

                            break
                        elif response == b't00211f\r':
                            main_window.child.textEdit.append("Get ID Response Failed (NACK)")

                            check_id = False

                            break
                        else:
                            main_window.child.textEdit.append("Get ID Response Failed (Unknown)")

                            check_id = False

                            break
                if time.time() >= prev_time + 1.0:
                    # print("Recv: %s" % response[0:].decode("utf-8"))
                    main_window.child.textEdit.append("Get ID Response Failed (Timeout)")

                    check_id = False

                    break

            if check_id == True:
                if chip_id == 0x421:
                    main_window.child.textEdit.append("Got ID: 0x%03x (STM32F446xx)" % chip_id)
                elif chip_id == 0x463:
                    main_window.child.textEdit.append("Got ID: 0x%03x (STM32F413xx)" % chip_id)
                else:
                    main_window.child.textEdit.append("Got ID: 0x%03x" % chip_id)
            else:
                main_window.child.textEdit.append("Can not get Chip ID")

            main_window.child.textEdit.append("")
            time.sleep(3.0)
        except:
            main_window.child.textEdit.append("Can not get Chip ID")
            main_window.child.textEdit.append("Can not use %s" % ser.port)

            main_window.child.textEdit.append("")
            time.sleep(3.0)

            check_id = False
            chip_id = 0x000
    else:
        main_window.child.textEdit.append("Can not get Chip ID")
        main_window.child.textEdit.append("Can not find serial port")

        main_window.child.textEdit.append("")
        time.sleep(3.0)

        check_id = False
        chip_id = 0x000

    main_window.child.textEdit.moveCursor(QtGui.QTextCursor.End)
    return check_id, chip_id


def erase_memory(check_ser, ser):
    if check_ser == True:
        try:
            while ser.in_waiting > 0:
                data_dummy = ser.read()

            request = b't0431ff\r'
            ser.write(request)
            # print("Sent: %s\\r" % request[0:-1].decode("utf-8"))
            time.sleep(0.01)

            response = b''
            prev_time = time.time()
            while True:
                if ser.in_waiting > 0:
                    data_rx = ser.read()
                    # print(data_rx)
                    response = response + data_rx
                    if data_rx == b'\r':
                        # print("Recv: %s\\r" % response[0:-1].decode("utf-8"))
                        if response == b't043179\r':
                            main_window.child.textEdit.append("Erase Memory Request Done (ACK)")

                            check_erase = True

                            break
                        elif response == b't04311f\r':
                            main_window.child.textEdit.append("Erase Memory Request Failed (NACK)")

                            check_erase = False

                            break
                        else:
                            main_window.child.textEdit.append("Erase Memory Request Failed (Unknown)")

                            check_erase = False

                            break
                if time.time() >= prev_time + 1.0:
                    # main_window.child.textEdit.append("Recv: %s" % response[0:].decode("utf-8"))
                    main_window.child.textEdit.append("Erase Memory Request Failed (Timeout)")

                    check_erase = False

                    break

            response = b''
            prev_time = time.time()
            while True:
                if ser.in_waiting > 0:
                    data_rx = ser.read()
                    # print(data_rx)
                    response = response + data_rx
                    if data_rx == b'\r':
                        # print("Recv: %s\\r" % response[0:-1].decode("utf-8"))
                        if response == b't043179\r':
                            main_window.child.textEdit.append("Erase Memory Response Done (ACK)")

                            check_erase = True

                            break
                        elif response == b't04311f\r':
                            main_window.child.textEdit.append("Erase Memory Response Failed (NACK)")

                            check_erase = False

                            break
                        else:
                            main_window.child.textEdit.append("Erase Memory Response Failed (Unknown)")

                            check_erase = False

                            break
                if time.time() >= prev_time + 30.0:
                    # print("Recv: %s" % response[0:].decode("utf-8"))
                    main_window.child.textEdit.append("Erase Memory Response Failed (Timeout)")

                    check_erase = False

                    break

            if check_erase == True:
                main_window.child.textEdit.append("Erased memory")
            else:
                main_window.child.textEdit.append("Can not erase memory")

            main_window.child.textEdit.append("")
            time.sleep(3.0)
        except:
            main_window.child.textEdit.append("Can not erase memory")
            main_window.child.textEdit.append("Can not use %s" % ser.port)

            main_window.child.textEdit.append("")
            time.sleep(3.0)

            check_erase = False
    else:
        main_window.child.textEdit.append("Can not erase memory")
        main_window.child.textEdit.append("Can not find serial port")

        main_window.child.textEdit.append("")
        time.sleep(3.0)

        check_erase = False

    main_window.child.textEdit.moveCursor(QtGui.QTextCursor.End)
    return check_erase


def upload_bin(check_ser, ser, check_bin, contents, num_128):
    if check_ser == True and check_bin == True:
        try:
            while ser.in_waiting > 0:
                data_dummy = ser.read()

            for_break = False
            check_upload_bin = False
            for num in range(num_128):
                while ser.in_waiting > 0:
                    data_dummy = ser.read()

                addr = 0x08000000 + (128 * num)
                request = b't0315%08x7f\r' % addr
                ser.write(request)
                # print("Sent: %s\\r" % request[0:-1].decode("utf-8"))
                time.sleep(0.01)

                response = b''
                prev_time = time.time()
                while True:
                    if ser.in_waiting > 0:
                        data_rx = ser.read()
                        # print(data_rx)
                        response = response + data_rx
                        if data_rx == b'\r':
                            # print("Recv: %s\\r" % response[0:-1].decode("utf-8"))
                            if response == b't031179\r':
                                # main_window.child.textEdit.append("Write Memory 0x%08x - 0x%08x Request Done (ACK), %04d / %04d" % (addr, addr + 128 - 1, num + 1, num_128))

                                check_upload_bin = True

                                break
                            elif response == b't03111f\r':
                                # main_window.child.textEdit.append("Write Memory 0x%08x - 0x%08x Request Failed (NACK), %04d / %04d" % (addr, addr + 128 - 1, num + 1, num_128))

                                for_break = True
                                check_upload_bin = False

                                break
                            else:
                                # main_window.child.textEdit.append("Write Memory 0x%08x - 0x%08x Request Failed (Unknown), %04d / %04d" % (addr, addr + 128 - 1, num + 1, num_128))

                                for_break = True
                                check_upload_bin = False

                                break
                    if time.time() >= prev_time + 1.0:
                        # main_window.child.textEdit.append("Recv: %s" % response[0:].decode("utf-8"))
                        main_window.child.textEdit.append(
                            "Write Memory 0x%08x - 0x%08x Request Failed (Timeout), %04d / %04d" % (
                            addr, addr + 128 - 1, num + 1, num_128))

                        for_break = True
                        check_upload_bin = False

                        break

                if for_break == True:
                    break

                for i in range(16):
                    temp = [0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff]
                    for j in range(8):
                        if ((128 * num) + (8 * i) + j) < len(contents):
                            temp[j] = contents[(128 * num) + (8 * i) + j]

                    request = b't0048%02x%02x%02x%02x%02x%02x%02x%02x\r' % (
                    temp[0], temp[1], temp[2], temp[3], temp[4], temp[5], temp[6], temp[7])
                    ser.write(request)
                    # main_window.child.textEdit.append("Sent: %s\\r" % request[0:-1].decode("utf-8"))
                    time.sleep(0.001)

                    response = b''
                    prev_time = time.time()
                    while True:
                        if ser.in_waiting > 0:
                            data_rx = ser.read()
                            # print(data_rx)
                            response = response + data_rx
                            if data_rx == b'\r':
                                # print("Recv: %s\\r" % response[0:-1].decode("utf-8"))
                                if response == b't031179\r':
                                    # main_window.child.textEdit.append("Write Memory 0x%08x - 0x%08x (0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s) Done (ACK), %04d / %04d" % (addr + (i*8), addr + ((i+1)*8) - 1, request[5:7].decode("utf-8"), request[7:9].decode("utf-8"), request[9:11].decode("utf-8"), request[11:13].decode("utf-8"), request[13:15].decode("utf-8"), request[15:17].decode("utf-8"), request[17:19].decode("utf-8"), request[19:21].decode("utf-8"), num + 1, num_128))

                                    check_upload_bin = True

                                    break
                                elif response == b't03111f\r':
                                    # main_window.child.textEdit.append("Write Memory 0x%08x - 0x%08x Failed (NACK), %04d / %04d" % (addr + (i*8), addr + ((i+1)*8) - 1, num + 1, num_128))

                                    for_break = True
                                    check_upload_bin = False

                                    break
                                else:
                                    # main_window.child.textEdit.append("Write Memory 0x%08x - 0x%08x Failed (Unknown), %04d / %04d" % (addr + (i*8), addr + ((i+1)*8) - 1, num + 1, num_128))

                                    for_break = True
                                    check_upload_bin = False

                                    break
                        if time.time() >= prev_time + 1.0:
                            # main_window.child.textEdit.append("Recv: %s" % response[0:].decode("utf-8"))

                            for_break = True
                            check_upload_bin = False

                            # main_window.child.textEdit.append("Write Memory 0x%08x - 0x%08x Failed (Timeout), %04d / %04d" % (addr + (i*8), addr + ((i+1)*8) - 1, num + 1, num_128))
                            break

                    if for_break == True:
                        break

                if for_break == True:
                    break

                response = b''
                prev_time = time.time()
                while True:
                    if ser.in_waiting > 0:
                        data_rx = ser.read()
                        # print(data_rx)
                        response = response + data_rx
                        if data_rx == b'\r':
                            # print("Recv: %s\\r" % response[0:-1].decode("utf-8"))
                            if response == b't031179\r':
                                # print("Write Memory 0x%08x - 0x%08x Response Done (ACK), %04d / %04d" % (addr, addr + 128 - 1, num + 1, num_128))

                                check_upload_bin = True

                                break
                            elif response == b't03111f\r':
                                # print("Write Memory 0x%08x - 0x%08x Response Failed (NACK), %04d / %04d" % (addr, addr + 128 - 1, num + 1, num_128))

                                for_break = True
                                check_upload_bin = False

                                break
                            else:
                                # print("Write Memory 0x%08x - 0x%08x Response Failed (Unknown), %04d / %04d" % (addr, addr + 128 - 1, num + 1, num_128))

                                for_break = True
                                check_upload_bin = False

                                break
                    if time.time() >= prev_time + 1.0:
                        # print("Recv: %s" % response[0:].decode("utf-8"))
                        # print("Write Memory 0x%08x - 0x%08x Response Failed (Timeout), %04d / %04d" % (addr, addr + 128 - 1, num + 1, num_128))

                        for_break = True
                        check_upload_bin = False

                        break

                if for_break == True:
                    break

                time.sleep(0.01)

            if check_upload_bin == True:
                main_window.child.textEdit.append("Uploaded .bin file")
            else:
                main_window.child.textEdit.append("Can not upload .bin file")

            main_window.child.textEdit.append("")
            time.sleep(3.0)
        except:
            main_window.child.textEdit.append("Can not upload .bin file")
            main_window.child.textEdit.append("Can not use %s" % ser.port)

            main_window.child.textEdit.append("")
            time.sleep(3.0)

            check_upload_bin = False
    elif check_ser == True and check_bin == False:
        main_window.child.textEdit.append("Can not upload .bin file")
        main_window.child.textEdit.append("Can not find .bin file")

        main_window.child.textEdit.append("")
        time.sleep(3.0)

        check_upload_bin = False
    elif check_ser == False and check_bin == True:
        main_window.child.textEdit.append("Can not upload .bin file")
        main_window.child.textEdit.append("Can not find serial port")

        main_window.child.textEdit.append("")
        time.sleep(3.0)

        check_upload_bin = False
    else:
        main_window.child.textEdit.append("Can not upload .bin file")
        main_window.child.textEdit.append("Can not find both .bin file and serial port")

        main_window.child.textEdit.append("")
        time.sleep(3.0)

        check_upload_bin = False

    main_window.child.textEdit.moveCursor(QtGui.QTextCursor.End)
    return check_upload_bin


def get_checksum(check_ser, ser, num_128):
    main_window.child.textEdit.append("Checking Checksum...")
    if check_ser == True:
        try:
            while ser.in_waiting > 0:
                data_dummy = ser.read()

            for_break = False
            check_get_checksum = False
            crc_128_ack = np.uint32(0x00000000)
            for num in range(num_128):
                QApplication.processEvents()

                while ser.in_waiting > 0:
                    data_dummy = ser.read()

                addr = 0x08000000 + (128 * num)
                request = b't0115%08x7f\r' % addr
                ser.write(request)
                # print("Sent: %s\\r" % request[0:-1].decode("utf-8"))
                time.sleep(0.01)

                response = b''
                prev_time = time.time()
                while True:
                    QApplication.processEvents()

                    if ser.in_waiting > 0:
                        data_rx = ser.read()
                        # main_window.child.textEdit.append(data_rx)
                        response = response + data_rx
                        if data_rx == b'\r':
                            # main_window.child.textEdit.append("Recv: %s\\r" % response[0:-1].decode("utf-8"))
                            if response == b't011179\r':
                                # main_window.child.textEdit.append("Read Memory 0x%08x - 0x%08x Request Done (ACK), %04d / %04d" % (addr, addr + 128 - 1, num + 1, num_128))

                                check_get_checksum = True

                                break
                            elif response == b't01111f\r':
                                # main_window.child.textEdit.append("Read Memory 0x%08x - 0x%08x Request Failed (NACK), %04d / %04d" % (addr, addr + 128 - 1, num + 1, num_128))

                                for_break = True
                                check_get_checksum = False

                                break
                            else:
                                # main_window.child.textEdit.append("Read Memory 0x%08x - 0x%08x Request Failed (Unknown), %04d / %04d" % (addr, addr + 128 - 1, num + 1, num_128))

                                for_break = True
                                check_get_checksum = False

                                break
                    if time.time() >= prev_time + 1.0:
                        # main_window.child.textEdit.append("Recv: %s" % response[0:].decode("utf-8"))

                        for_break = True
                        check_get_checksum = False

                        # main_window.child.textEdit.append("Read Memory 0x%08x - 0x%08x Request Failed (Timeout), %04d / %04d" % (addr, addr + 128 - 1, num + 1, num_128))
                        break

                if for_break == True:
                    break

                i = 0
                response = b''
                prev_time = time.time()
                while True:
                    QApplication.processEvents()

                    if ser.in_waiting > 0:
                        data_rx = ser.read()
                        # main_window.child.textEdit.append(data_rx)
                        response = response + data_rx
                        if data_rx == b'\r':
                            # main_window.child.textEdit.append("Recv: %s\\r" % response[0:-1].decode("utf-8"))
                            if response[0:5] == b't0118':
                                if len(response) == 22:
                                    for j in range(8):
                                        crc_128_ack = crc_128_ack + np.uint32(
                                            int(("0x%02s" % response[5 + 2 * j:5 + 2 * j + 2].decode("utf-8")), 16))

                                    check_get_checksum = True

                                    # main_window.child.textEdit.append("Read Memory 0x%08x - 0x%08x (0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s) Done, %04d / %04d" % (addr + (i*8), addr + ((i+1)*8) - 1, response[5:7].decode("utf-8"), response[7:9].decode("utf-8"), response[9:11].decode("utf-8"), response[11:13].decode("utf-8"), response[13:15].decode("utf-8"), response[15:17].decode("utf-8"), response[17:19].decode("utf-8"), response[19:21].decode("utf-8"), num + 1, num_128))
                                else:
                                    for_break = True
                                    check_get_checksum = False

                                    # main_window.child.textEdit.append("Read Memory 0x%08x - 0x%08x Failed (Missing data), %04d / %04d" % (addr + (i*8), addr + ((i+1)*8) - 1, num + 1, num_128))
                            else:
                                for_break = True
                                check_get_checksum = False

                                # main_window.child.textEdit.append("Read Memory 0x%08x - 0x%08x Failed (Unknown), %04d / %04d" % (addr + (i*8), addr + ((i+1)*8) - 1, num + 1, num_128))

                            response = b''
                            prev_time = time.time()

                            i = i + 1
                            if i == 16:
                                break
                    if time.time() >= prev_time + 1.0:
                        # main_window.child.textEdit.append("Recv: %s" % response[0:].decode("utf-8"))

                        for_break = True
                        check_get_checksum = False

                        # main_window.child.textEdit.append("Read Memory 0x%08x - 0x%08x Failed (Timeout), %04d / %04d" % (addr, addr + 128 - 1, num + 1, num_128))
                        break

                if for_break == True:
                    break

                response = b''
                prev_time = time.time()
                while True:
                    QApplication.processEvents()

                    if ser.in_waiting > 0:
                        data_rx = ser.read()
                        # main_window.child.textEdit.append(data_rx)
                        response = response + data_rx
                        if data_rx == b'\r':
                            # main_window.child.textEdit.append("Recv: %s\\r" % response[0:-1].decode("utf-8"))
                            if response == b't011179\r':
                                # main_window.child.textEdit.append("Read Memory 0x%08x - 0x%08x Response Done (ACK), %04d / %04d" % (addr, addr + 128 - 1, num + 1, num_128))

                                check_get_checksum = True

                                break
                            elif response == b't01111f\r':
                                # main_window.child.textEdit.append("Read Memory 0x%08x - 0x%08x Response Failed (NACK), %04d / %04d" % (addr, addr + 128 - 1, num + 1, num_128))

                                for_break = True
                                check_get_checksum = False

                                break
                            else:
                                # main_window.child.textEdit.append("Read Memory 0x%08x - 0x%08x Response Failed (Unknown), %04d / %04d" % (addr, addr + 128 - 1, num + 1, num_128))

                                for_break = True
                                check_get_checksum = False

                                break
                    if time.time() >= prev_time + 1.0:
                        # main_window.child.textEdit.append("Recv: %s" % response[0:].decode("utf-8"))

                        for_break = True
                        check_get_checksum = False

                        main_window.child.textEdit.append(
                            "Read Memory 0x%08x - 0x%08x Response Failed (Timeout), %04d / %04d" % (
                            addr, addr + 128 - 1, num + 1, num_128))
                        break

                if for_break == True:
                    break

                time.sleep(0.01)

            if check_get_checksum == True:
                pass
                # main_window.child.textEdit.append("Got checksum (0x%08x - 0x%08x): 0x%08x, %d bytes" % (0x08000000, 0x08000000 + (num_128 * 128) - 1, crc_128_ack, (num_128 * 128)))
            else:
                main_window.child.textEdit.append("Can not get checksum")

            main_window.child.textEdit.append("")
            time.sleep(3.0)
        except:
            main_window.child.textEdit.append("Can not get checksum")
            main_window.child.textEdit.append("Can not use %s" % ser.port)

            main_window.child.textEdit.append("")
            time.sleep(3.0)

            check_get_checksum = False
            crc_128_ack = np.uint32(0x00000000)
    else:
        main_window.child.textEdit.append("Can not get checksum")
        main_window.child.textEdit.append("Can not find serial port")

        main_window.child.textEdit.append("")
        time.sleep(3.0)

        check_get_checksum = False
        crc_128_ack = np.uint32(0x00000000)

    main_window.child.textEdit.moveCursor(QtGui.QTextCursor.End)
    return check_get_checksum, crc_128_ack


def verify_checksum(crc_128, crc_128_ack):
    if crc_128 == crc_128_ack:
        main_window.child.textEdit.append(
            "Checksum matched (.bin file: 0x%08x, Memory: 0x%08x)" % (crc_128, crc_128_ack))

        main_window.child.textEdit.append("")
        time.sleep(3.0)

        check_verify_checksum = True
    else:
        main_window.child.textEdit.append(
            "Checksum not matched (.bin file: 0x%08x, Memory: 0x%08x)" % (crc_128, crc_128_ack))

        main_window.child.textEdit.append("")
        time.sleep(3.0)

        check_verify_checksum = False
    main_window.child.textEdit.moveCursor(QtGui.QTextCursor.End)
    return check_verify_checksum


def main_func(bin_file, port, skip_checksum):
    check_bin, contents, crc, num_128, crc_128 = read_bin(bin_file)
    if check_bin == False:
        main_window.child.textEdit.append("Failed to upload .bin file (read_bin)")

        main_window.child.textEdit.append("")

        main_window.child.textEdit.moveCursor(QtGui.QTextCursor.End)
        time.sleep(3.0)

        return False

    check_ser, ser = open_serial(port)
    if check_ser == False:
        main_window.child.textEdit.append("Failed to upload .bin file (open_serial)")

        main_window.child.textEdit.append("")

        main_window.child.textEdit.moveCursor(QtGui.QTextCursor.End)
        time.sleep(3.0)

        return False

    check_ser = check_serial(check_ser, ser)
    if check_ser == False:
        check_ser = close_serial(check_ser, ser)

        main_window.child.textEdit.append("Failed to upload .bin file (check_serial)")

        main_window.child.textEdit.append("")

        main_window.child.textEdit.moveCursor(QtGui.QTextCursor.End)
        time.sleep(3.0)

        return False

    check_check_hse_frequency, check_check_hse_frequency_opt = check_hse_frequency(check_ser, ser)
    if check_check_hse_frequency == False:
        check_ser = close_serial(check_ser, ser)

        main_window.child.textEdit.append("Failed to upload .bin file (check_hse_frequency)")

        main_window.child.textEdit.append("")

        main_window.child.textEdit.moveCursor(QtGui.QTextCursor.End)
        time.sleep(3.0)

        return False

    check_get_id, chip_id = get_ID(check_ser, ser)
    if check_get_id == False:
        check_ser = close_serial(check_ser, ser)

        main_window.child.textEdit.append("Failed to upload .bin file (check_get_id)")

        main_window.child.textEdit.append("")

        main_window.child.textEdit.moveCursor(QtGui.QTextCursor.End)

        time.sleep(3.0)

        return False

    check_erase_memory = erase_memory(check_ser, ser)
    if check_erase_memory == False:
        check_ser = close_serial(check_ser, ser)

        main_window.child.textEdit.append("Failed to upload .bin file (erase_memory)")

        main_window.child.textEdit.append("")

        main_window.child.textEdit.moveCursor(QtGui.QTextCursor.End)
        time.sleep(3.0)

        return False

    check_upload_bin = upload_bin(check_ser, ser, check_bin, contents, num_128)
    if check_upload_bin == False:
        check_ser = close_serial(check_ser, ser)

        main_window.child.textEdit.append("Failed to upload .bin file (upload_bin)")

        main_window.child.textEdit.append("")

        main_window.child.textEdit.moveCursor(QtGui.QTextCursor.End)
        time.sleep(3.0)

        return False

    if skip_checksum == False:
        check_get_checksum, crc_128_ack = get_checksum(check_ser, ser, num_128)
        if check_get_checksum == False:
            check_ser = close_serial(check_ser, ser)

            main_window.child.textEdit.append("Failed to verify checksum (get_checksum)")

            main_window.child.textEdit.append("")
            time.sleep(3.0)

            return False

        check_verify_checksum = verify_checksum(crc_128, crc_128_ack)
    else:
        main_window.child.textEdit.append("Skipped checksum verification")

        main_window.child.textEdit.append("")

        main_window.child.textEdit.moveCursor(QtGui.QTextCursor.End)

        time.sleep(3.0)

    check_ser = close_serial(check_ser, ser)

    if skip_checksum == False:
        if check_verify_checksum == True:
            main_window.child.textEdit.append("Successfully uploaded .bin file (Checksum matched)")

            main_window.child.textEdit.append("")

            main_window.child.textEdit.moveCursor(QtGui.QTextCursor.End)

            time.sleep(3.0)

            return True
        else:
            main_window.child.textEdit.append("Failed to upload .bin file (Checksum unmatched)")

            main_window.child.textEdit.append("")

            main_window.child.textEdit.moveCursor(QtGui.QTextCursor.End)

            time.sleep(3.0)

            return False
    else:
        main_window.child.textEdit.append("Successfully uploaded .bin file (Checksum verification skipped)")

        main_window.child.textEdit.append("")

        main_window.child.textEdit.moveCursor(QtGui.QTextCursor.End)

        time.sleep(3.0)

        return True


sys.exit(app.exec_())
