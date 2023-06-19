from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QPalette, QBrush, QIcon
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal, QUrl, QTimer, QThread
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QComboBox, QLineEdit, QPushButton, QVBoxLayout
import threading
import sys
import upload_bin_func_and_debug_func as main_functions
from serial.tools import list_ports


from PyQt5 import QtWidgets, uic

class Page_Firmware_Update(QWidget):
    button_clicked_signal = pyqtSignal()
    # file, port, checksum_skip
    btn_update_clicked_signal = pyqtSignal(str, str, bool)
    btn_done_update_clicked_signal = pyqtSignal()

    def __init__(self, parent=None):
        super(Page_Firmware_Update, self).__init__(parent)
        uic.loadUi('firmware_ui.ui', self)

    def btn_back_clicked(self):
        self.button_clicked_signal.emit()

    def btn_update_clicked(self):
        _file = self.edit_bin_file.text()
        _port = self.edit_port_number.text()
        _checksum = self.chk_checksum.isChecked()
        print(_file, _port, _checksum)
        self.btn_update_clicked_signal.emit(_file, _port, _checksum)

    def btn_done_update_clicked(self):
        _port = self.edit_port_number.text()
        self.btn_done_update_clicked_signal.emit(_port)

class SquareComboBox(QComboBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def resizeEvent(self, event):
        size = min(self.width(), self.height())
        self.setFixedSize(size, size)

class SquarePushButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def resizeEvent(self, event):
        size = min(self.width(), self.height())
        self.setFixedSize(size, size)

class Worker(QThread):
    def __init__(self, func, *args):
        super().__init__()
        self.func = func
        self.args = args

    def run(self):
        self.func(*self.args)

    def stop(self):
        self.is_running = False
        self.thread().quit()
        self.thread().wait()

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Load the main UI
        uic.loadUi("Theme.ui", self)

        #window size and other options
        self.setFixedSize(1600, 900)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.stacked_widget.setCurrentIndex(0)

        # menu box
        # self.combo_menu.addItem("Firmware Update")

        # menu combobox settings
        icon1 = QIcon("img_sensors.png")
        # icon2 = QIcon("main_theme.png")
        # icon3 = QIcon("Theme.png.png")

        self.combo_menu.addItem(icon1,"Firmware Update")
        # self.combo_menu.addItem(icon2, "")
        # self.combo_menu.addItem(icon3, "")

        # self.combo_menu.addItem("Option 2")
        # self.combo_menu.addItem("Option 3")
        self.combo_menu.currentIndexChanged.connect(self.change_stacked_widget)
        self.combo_menu.setCurrentIndex(-1)


        # firmware update page init
        self.page_firmware_update = Page_Firmware_Update(self)
        self.stacked_widget.addWidget(self.page_firmware_update)
        self.page_firmware_update.button_clicked_signal.connect(self.page_firmware_update_btn_back_clicked)

        #
        self.hidden_pages = [self.page_firmware_update.objectName()]

        # 특정 위젯들 정사각형 만들기
        self.combo_menu.__class__ = SquareComboBox
        buttons = [self.btn_left, self.btn_right, self.btn_digital_1, self.btn_digital_2, self.btn_digital_3, self.btn_digital_4]  # 가정: button1, button2, button3는 my_ui.ui에 정의되어 있다.
        for button in buttons:
            button.__class__ = SquarePushButton

        # gauge widget 설정
        self.init_gauge(self.widget_gauge1)
        self.init_gauge(self.widget_gauge2)

        ### Thread
        # Define the threads

        ports = list_ports.comports()

        port = ports[0].name
        print(port)

        # bin_file, port, skip_checksum
        self.worker_firmware_update = Worker(self.run_main_func, "vcu_f413zh_mbed.NUCLEO_F413ZH.bin", port, False)
        self.worker_debugging = Worker(self.run_main_func2, port)

        # Start the default thread
        self.current_worker = self.worker_debugging
        self.current_worker.start()

        print("pass?")
        # Connect the buttons
        self.page_firmware_update.btn_update_clicked_signal.connect(self.start_func1)
        self.page_firmware_update.btn_done_update_clicked_signal.connect(self.start_func2)

        ## Thead End


        ### UI init
        QTimer.singleShot(0, self.update_ui_timer)
        QTimer.singleShot(0, self.fill_ports)


    def update_ui_timer(self):
        self.timer_update_ui = QTimer()
        self.timer_update_ui.timeout.connect(self.update_ui)
        self.timer_update_ui.start(1000)  # Fire the timer every 1000 ms (1 second)

    # update시에는 막아놓을 것, 즉 main_func2 작동시에만 변경 가능
    def port_changed(self, new_port):
        self.page_firmware_update.edit_port_number.setText(str(new_port))
        # Stop the current worker
        self.stop_worker(self.current_worker)

        #init
        self.current_worker = None
        # Create and start a new worker with the new port
        self.worker_debugging = Worker(self.run_main_func2, new_port)
        self.current_worker = self.worker_debugging
        self.current_worker.start()


    def stop_worker(self, worker):
        if worker is not None and worker.isRunning():  # If the thread is active
            # Stop the thread by setting exit_debug_mode_flag
            main_functions.exit_debug_mode_flag = True
            # True로 둔 것이 끝날 때까지 기다림
            worker.wait()
            main_functions.exit_debug_mode_flag = False

        main_functions.exit_debug_mode_flag = True

    def fill_ports(self):
        self.combo_port.blockSignals(True)

        ports = list_ports.comports()
        print(ports)
        for port in ports:
            print(str(port.name))
            self.combo_port.addItem(str(port.name))

        self.combo_port.blockSignals(False)

    def update_ui(self):
        """ 모든 변수
        global debug_bytearray_list
        global ds3231_time_u32, ds3231_date_str
        global test_module1_u8_B0, test_module1_u8_B1, test_module1_u8_B7
        global test_module2_u8_B0, test_module2_u8_B1, test_module2_u8_B7
        :return:
        """

        # time : top_left
        data_time = main_functions.ds3231_date_str
        self.lbl_time.setText(str(data_time))
        # sensors : page1
        self.data1 = main_functions.test_module1_u8_B0
        self.data2 = main_functions.test_module1_u8_B1
        self.data3 = main_functions.test_module1_u8_B7
        self.data4 = main_functions.test_module2_u8_B0
        self.data5 = main_functions.test_module2_u8_B1
        self.data6 = main_functions.test_module2_u8_B7
        self.data7 = '7'
        self.data8 = '8'

        displaying_sensor_list = [self.data1, self.data2, self.data3, self.data4, self.data5, self.data6, self.data7,
                                  self.data8]

        for i in range(1, 9):
            label = getattr(self, f'lbl_p1_sensor{i}')
            label.setText(str(displaying_sensor_list[i - 1]))

    ### main_func thread
    def run_main_func(self, file, port, check_sum):
        main_functions.main_func(file, port, check_sum)

    def run_main_func2(self, port):
        main_functions.main_func2(port)

    def start_func1(self, file, port, check_sum):
        self.worker_firmware_update = Worker(self.run_main_func, file, port, check_sum)
        self.switch_workers(self.worker_firmware_update)

    def start_func2(self, port):
        self.worker_debugging = Worker(self.run_main_func2, port)
        self.switch_workers(self.worker_debugging)
        self.timer_update_ui.start(1000)

    def switch_workers(self, next_worker):
        if self.current_worker is not None:
            self.timer_update_ui.stop()
            main_functions.exit_debug_mode_flag = True
            self.current_worker.quit()
            self.current_worker.wait()
        main_functions.exit_debug_mode_flag = False
        self.current_worker = next_worker
        self.current_worker.start()
    ## main_func thread End

    ### 여기 추후에 dict로 받아서, unit, max, min 등도 parameter로 넣기
    def init_gauge(self, gauge):
        gauge.units = "Km/h"
        gauge.enableBarGraph = True
        gauge.setMouseTracking(True)
        gauge.maxValue = 255
        gauge.minValue = 0
        gauge.updateValue(0)

        # 사용할만한 theme
        # gauge.setGaugeTheme(0)
        # gauge.setGaugeTheme(2)

    # combobox가 변경됐을 때 바로 실행 # 페이지 움직이기 전부터 페이지 옮기는 것까지
    def change_stacked_widget(self, index):
        self.prev_page_name = self.stacked_widget.currentIndex()

        if index == -1:  # No item selected
            # Here you can handle the case where no item is selected
            pass

        elif self.combo_menu.currentText() == "Firmware Update":  # If the first item is selected
            self.stacked_widget.setCurrentWidget(self.page_firmware_update)
            self.btn_right.setDisabled(True)
            self.btn_left.setDisabled(True)
            self.btn_right.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
            self.btn_left.setStyleSheet("background-color: rgba(0, 0, 0, 0);")

        elif self.combo_menu.currentText() == "Option 2":  # If the first item is selected
            pass

        elif self.combo_menu.currentText() == "Option 3":  # If the first item is selected
            pass

        else:
            pass

    def next_page(self):
        current_index = self.stacked_widget.currentIndex()
        while True:
            if current_index < self.stacked_widget.count() - 1:
                current_index += 1
            else:  # We are at the end, go to first page
                current_index = 0

            # Check if this page is in the hidden pages list
            if self.stacked_widget.widget(current_index).objectName() not in self.hidden_pages:
                break

        self.stacked_widget.setCurrentIndex(current_index)
        self.naming_title(current_index)

    def prev_page(self):
        current_index = self.stacked_widget.currentIndex()
        while True:
            if current_index > 0:
                current_index -= 1
            else:  # We are at the beginning, go to last page
                current_index = self.stacked_widget.count() - 1

            # Check if this page is in the hidden pages list
            if self.stacked_widget.widget(current_index).objectName() not in self.hidden_pages:
                break

        self.stacked_widget.setCurrentIndex(current_index)
        self.naming_title(current_index)

    # ui page명은 무조건 page_~~~으로
    def naming_title(self, current_index):
        title = str(self.stacked_widget.widget(current_index).objectName())
        title = title[5:].capitalize()
        self.lbl_title.setText(title)


    def page_firmware_update_btn_back_clicked(self):
        print("Button in child widget was clicked!")

        # 페이지 변경 및, combobox 초기화 : 순서 바뀌면 안됨
        # combo menu -1 index로 초기화
        self.stacked_widget.setCurrentIndex(self.prev_page_name)
        self.combo_menu.setCurrentIndex(-1)

        # btn control
        self.btn_right.setDisabled(False)
        self.btn_left.setDisabled(False)
        self.btn_right.setStyleSheet(
            """
            border-image: url(right.png);
            background-repeat: no-repeat;
            background-position: center;
            background-size: cover;
            """
        )
        self.btn_left.setStyleSheet(
            """
            border-image: url(left.png);
            background-repeat: no-repeat;
            background-position: center;
            background-size: cover;
            """
        )

app = QtWidgets.QApplication([])
window = MainWindow()
window.show()
app.exec_()