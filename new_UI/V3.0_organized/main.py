import random

from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QPalette, QBrush, QIcon, QPainter
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal, QUrl, QTimer, QThread
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QComboBox, QLineEdit, QPushButton, QVBoxLayout, \
    QFileDialog, QTextEdit, QDialogButtonBox, QMessageBox, QLabel, QInputDialog
import sys
import upload_bin_func_and_debug_func as main_functions
from serial.tools import list_ports
from PyQt5 import QtWidgets, uic

class Page_Firmware_Update(QWidget):
    button_clicked_signal = pyqtSignal()
    # file, port, checksum_skip
    btn_update_clicked_signal = pyqtSignal(str, str, bool)
    btn_done_update_clicked_signal = pyqtSignal(str)

    def __init__(self, parent=None):
        super(Page_Firmware_Update, self).__init__(parent)
        uic.loadUi('firmware_ui.ui', self)

        # button disable init
        self.btn_cancel.setEnabled(False)

        self.textedit_log.document().setMaximumBlockCount(100)
        # Connect the textEmitted signal from PrintEmitter to the append method of MyTextEdit
        sys.stdout.textEmitted.connect(self.textedit_write)

    def textedit_write(self, text):
        if not self.btn_update.isEnabled():
            self.textedit_log.append(text)

    def btn_back_clicked(self):
        self.button_clicked_signal.emit()

    def btn_update_clicked(self):
        disable_button_list = [self.btn_back, self.btn_file_select, self.btn_update, self.btn_cancel]

        for button in disable_button_list:
            button.setEnabled(False)

        _file = self.edit_bin_file.text()
        _port = self.edit_port_number.text()
        _checksum = self.chk_checksum.isChecked()
        print(_file, _port, _checksum)
        self.btn_update_clicked_signal.emit(_file, _port, _checksum)

    def btn_done_update_clicked(self):
        self.btn_done.setEnabled(False)
        able_button_list = [self.btn_back, self.btn_file_select, self.btn_update, self.btn_cancel]
        for button in able_button_list:
            button.setEnabled(True)
        _port = self.edit_port_number.text()
        self.btn_done_update_clicked_signal.emit(_port)

    def btn_cancel_update_clicked(self):
        self.btn_cancel.setEnabled(False)
        able_button_list = [self.btn_back, self.btn_file_select, self.btn_update]
        for button in able_button_list:
            button.setEnabled(True)
        _port = self.edit_port_number.text()

        QMessageBox.warning(self, "Warning", "Memory Erased Update again")

        self.btn_done_update_clicked_signal.emit(_port)

    def btn_file_select_clicked(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Select Uploading File", "", "All Files (*)",
                                                  options=options)
        if fileName:
            print(fileName)
            self.edit_bin_file.setText(fileName)

class SquareWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def resizeEvent(self, event):
        size = min(self.width(), self.height())
        self.setFixedSize(size, size)

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
    task_done = pyqtSignal()

    def __init__(self, func, *args):
        super().__init__()
        self.func = func
        self.args = args

    def run(self):
        self.func(*self.args)
        # func에서 함수가 실제로 동작 후 다음 구문 finished가 실행
        self.task_done.emit()
        print("worker done")

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

        self.combo_gauges = ["combo_small_gauge_1", "combo_small_gauge_2", "combo_gauge_1", "combo_gauge_2"]

        self.init_window()
        self.initializing_editable_labels()
        self.load_label_texts()
        self.init_port = list_ports.comports()
        self.init_port = self.init_port[0].name
        self.init_firmware_update()
        self.init_signals_and_slots()
        self.init_combo_menu()
        self.init_progressbar()
        self.init_make_rectangle_widgets()


        self.hidden_pages = [self.page_firmware_update.objectName()]


        self.init_digital_status()

        # gauge widget 설정
        self.init_gauge(self.widget_gauge1)
        self.init_gauge(self.widget_gauge2)
        self.init_gauge(self.widget_small_gauge1)
        self.init_gauge(self.widget_small_gauge2)

        # 기본 실행 thread
        self.worker_debugging = Worker(self.run_main_func2, self.init_port)
        self.current_worker = self.worker_debugging
        self.current_worker.start()

        self.init_timers()

    def init_window(self):
        self.setFixedSize(1600, 900)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.stacked_widget.setCurrentIndex(0)


        for i in range(1, 9):  # range(1, 13)는 1부터 12까지의 숫자를 생성합니다.
            combo_sensor_selector = f"combo_p1_sensor_selector_{i}"  # f-string을 사용하여 위젯 이름 생성
            combo_sensor_selector_ = getattr(self, combo_sensor_selector)  # getattr 함수로 동적으로 위젯 참조 얻기
            combo_sensor_selector_.hide()

        for combo_gauge in self.combo_gauges:  # range(1, 13)는 1부터 12까지의 숫자를 생성합니다.
            getattr(self, combo_gauge).hide()  # getattr 함수로 동적으로 위젯 참조 얻기

        self.btn_custom_setting.hide()


    def init_signals_and_slots(self):
        for i in range(1, 9):  # Adjust range accordingly
            combo_box = self.findChild(QComboBox, f'combo_p1_sensor_selector_{i}')
            combo_box.currentIndexChanged.connect(self.update_label)

        self.worker_firmware_update = Worker(self.run_main_func, "vcu_f413zh_mbed.NUCLEO_F413ZH.bin", self.init_port, False)
        self.worker_firmware_update.task_done.connect(self.update_done_signal)
        self.page_firmware_update.btn_update_clicked_signal.connect(self.start_func1)
        self.page_firmware_update.btn_done_update_clicked_signal.connect(self.start_func2)

    def init_combo_menu(self):
        # menu combobox settings
        icon1 = QIcon("img_sensors.png")
        icon2 = QIcon("img_settings.png")
        # icon3 = QIcon("Theme.png.png")

        self.menu_page_name = ["Firmware Update", "UI Settings"]
        self.combo_menu.addItem(icon1,self.menu_page_name[0])
        self.combo_menu.addItem(icon2, self.menu_page_name[1])
        # self.combo_menu.addItem(icon3, "")

        # self.combo_menu.addItem("Option 2")
        # self.combo_menu.addItem("Option 3")
        self.combo_menu.currentIndexChanged.connect(self.change_stacked_widget)
        self.combo_menu.setCurrentIndex(-1)

    def init_make_rectangle_widgets(self):
        self.combo_menu.__class__ = SquareComboBox
        self.widget_usb_state.__class__ = SquareWidget
        # self.widget_digital_2.__class__ = SquareWidget

        for i in range(1, 17):  # range(1, 13)는 1부터 12까지의 숫자를 생성합니다.
            widget_name = f"widget_digital_{i}"  # f-string을 사용하여 위젯 이름 생성
            widget = getattr(self, widget_name)  # getattr 함수로 동적으로 위젯 참조 얻기
            widget.__class__ = SquareWidget  # 클래스 변경
            btn_name = f"btn_btn_{i}"  # f-string을 사용하여 위젯 이름 생성
            btn = getattr(self, btn_name)  # getattr 함수로 동적으로 위젯 참조 얻기
            btn.__class__ = SquarePushButton  # 클래스 변경

        #theme
        buttons = [self.btn_left, self.btn_right]  # 가정: button1, button2, button3는 my_ui.ui에 정의되어 있다.
        for button in buttons:
            button.__class__ = SquarePushButton

        #page_buttons
        for i in range(1, 17):  # range(1, 13)는 1부터 12까지의 숫자를 생성합니다.
            widget_name = f"btn_btn_{i}"  # f-string을 사용하여 위젯 이름 생성
            widget = getattr(self, widget_name)  # getattr 함수로 동적으로 위젯 참조 얻기
            widget.__class__ = SquarePushButton  # 클래스 변경

    def init_digital_status(self):
        # digital states
        self.leds = [getattr(self, f'widget_digital_{i + 1}') for i in range(16)]
        self.led_states = [False] * 16  # 예시로 모두 False로 초기화

        self.pixmap_on = QPixmap('led_on.png')
        self.pixmap_off = QPixmap('led_off.png')

    def init_firmware_update(self):
        self.page_firmware_update = Page_Firmware_Update(self)
        self.stacked_widget.addWidget(self.page_firmware_update)
        self.page_firmware_update.button_clicked_signal.connect(self.page_firmware_update_btn_back_clicked)

    def init_timers(self):
        QTimer.singleShot(0, self.update_ui_timer)
        QTimer.singleShot(0, self.update_progressbar_timer)
        QTimer.singleShot(0, self.ports_refresh_timer)
        QTimer.singleShot(0, self.fill_ports)
        QTimer.singleShot(0, self.update_usb_state_timer)
        QTimer.singleShot(0, self.update_leds_timer)
        QTimer.singleShot(0, self.timer_per_5sec)

    def initializing_editable_labels(self):
        self.editable_labels = []
        # lbl_p1_sensor_name_1 ~ lbl_p1_sensor_name_8
        for i in range(1, 9):
            self.editable_labels.append(f"lbl_p1_sensor_name_{i}")

        # lbl_btn_1 ~ lbl_btn_16
        for i in range(1, 17):
            self.editable_labels.append(f"lbl_btn_{i}")

        # lbl_digital_1 ~ lbl_digital_16
        for i in range(1, 17):
            self.editable_labels.append(f"lbl_digital_{i}")

        for i in range(1, 3):
            self.editable_labels.append(f"lbl_small_gauge_{i}")

        for i in range(1, 3):
            self.editable_labels.append(f"lbl_gauge_{i}")

    def load_label_texts(self):
        try:
            with open("label_texts.txt", "r") as file:
                for line in file.readlines():
                    label_name, text = line.strip().split(":")
                    if label_name in self.editable_labels:
                        label = getattr(self, label_name)
                        label.setText(text)
        except FileNotFoundError:
            # 파일이 없는 경우의 처리: 일단은 아무것도 하지 않음
            pass

    def update_label(self, index):
        # Sender is the combo box that emitted the signal
        combo_box = self.sender()
        # Get the currently selected key
        key = combo_box.currentText()
        # Get the corresponding value from the dictionary
        value = main_functions.display_data.get(key)
        # Update the corresponding label
        label = self.findChild(QLabel, f'lbl_p1_sensor_{combo_box.objectName()[-1]}')
        label.setText(str(value))

        with open('selections.txt', 'w') as file:
            for i in range(1, 9):
                combo_box = self.findChild(QComboBox, f'combo_p1_sensor_selector_{i}')
                selected_key = combo_box.currentText()
                file.write(f'{selected_key}\n')

    def timer_per_5sec(self):
        self.timer_per_second = QTimer(self)
        self.timer_per_second.setInterval(5000)  # 1000ms = 1초
        self.timer_per_second.timeout.connect(self.update_combo_boxes)
        self.timer_per_second.start()

    def update_combo_boxes(self):
        for i in range(1, 9):  # Adjust range accordingly
            combo_box = self.findChild(QComboBox, f'combo_p1_sensor_selector_{i}')

            # Block signals
            combo_box.blockSignals(True)

            # Save current selected item
            current_item = combo_box.currentText()

            combo_box.clear()

            # Populate combo box with keys from display_data
            for key in main_functions.display_data.keys():
                combo_box.addItem(key)

            # Restore previous selection if it still exists
            index = combo_box.findText(current_item)
            if index >= 0:
                combo_box.setCurrentIndex(index)

            # Unblock signals
            combo_box.blockSignals(False)

    def btn_custom_setting_end_clicked(self):
        for i in range(1, 9):  # range(1, 13)는 1부터 12까지의 숫자를 생성합니다.
            combo_sensor_selector = f"combo_p1_sensor_selector_{i}"  # f-string을 사용하여 위젯 이름 생성
            combo_sensor_selector_ = getattr(self, combo_sensor_selector)  # getattr 함수로 동적으로 위젯 참조 얻기
            combo_sensor_selector_.hide()
        self.btn_custom_setting.hide()

        self.combo_menu.setEnabled(True)
        self.combo_menu.setCurrentIndex(-1)

        for label_name in self.editable_labels:
            label = self.findChild(QLabel, label_name)
            if label:
                label.setStyleSheet("")
                label.mousePressEvent = None

        for combo_gauge in self.combo_gauges:  # range(1, 13)는 1부터 12까지의 숫자를 생성합니다.
            getattr(self, combo_gauge).hide()  # getattr 함수로 동적으로 위젯 참조 얻기

        self.save_label_texts()

    def label_clicked(self, label):
        text, ok = QInputDialog.getText(self, "Edit Label", "Enter new text:", text=label.text())
        if ok:
            label.setText(text)

    def save_label_texts(self):
        with open("label_texts.txt", "w") as file:
            for label_name in self.editable_labels:
                label = self.findChild(QLabel, label_name)
                if label:
                    file.write(f"{label_name}:{label.text()}\n")

        # Load the saved text and update labels
        with open("label_texts.txt", "r") as file:
            for line in file:
                name, text = line.strip().split(":")
                label = self.findChild(QLabel, name)
                if label:
                    label.setText(text)

        # Make labels non-editable
        for label_name in self.editable_labels:
            label = self.findChild(QLabel, label_name)
            label.setTextInteractionFlags(Qt.NoTextInteraction)
            label.setStyleSheet("")  # Reset to default style

    def update_leds_timer(self):
        self.timer_update_leds = QTimer()
        self.timer_update_leds.timeout.connect(self.update_leds)
        self.timer_update_leds.start(3000)  # Fire the timer every 1000 ms (1 second)

    def update_leds(self):
        # 예시로 상태를 무작위로 변경
        new_states = [random.choice([True, False]) for _ in range(len(self.leds))]
        on_stylesheet = "QWidget {border-image: url(led_on.png); background-repeat: no-repeat; background-position: center; background-size: cover;}"
        off_stylesheet = "QWidget {border-image: url(led_off.png); background-repeat: no-repeat; background-position: center; background-size: cover;}"

        for led, new_state, old_state in zip(self.leds, new_states, self.led_states):
            if new_state != old_state:
                if new_state:
                    led.setStyleSheet(on_stylesheet)
                else:
                    led.setStyleSheet(off_stylesheet)

        self.led_states = new_states

    def update_usb_state_timer(self):
        self.timer_usb_state = QTimer()
        self.timer_usb_state.timeout.connect(self.update_usb_state)
        self.timer_usb_state.start(1000)  # Fire the timer every 1000 ms (1 second)
        # self.lbl_usb_state.set_status(self.usb_state)

    def update_usb_state(self):
        if main_functions.usb_state == True:
            self.widget_usb_state.setStyleSheet(
                """
                QWidget#widget_usb_state {
                border-image: url(led_on.png);
                background-repeat: no-repeat;
                background-position: center;
                background-size: cover;
                }
                """
            )
        else:
            self.widget_usb_state.setStyleSheet(
                """
                QWidget#widget_usb_state {
                border-image: url(led_off.png);
                background-repeat: no-repeat;
                background-position: center;
                background-size: cover;
                }
                """
            )

    def update_done_signal(self):
        if self.update_done_state == True:
            print("in1")
            self.page_firmware_update.btn_done.setDisabled(False)

        elif self.update_done_state == False:
            print("in2")

            self.page_firmware_update.btn_cancel.setDisabled(False)

        else:
            print("error")

    def init_progressbar(self):
        self.progressbar_gas_meter.setMinimum(0)
        self.progressbar_gas_meter.setMaximum(100)

        # 음수가 안 됨 -30 ~ 50 >> 0 ~ 80
        self.progressbar_thermometer.setMinimum(0)
        self.progressbar_thermometer.setMaximum(50)


    def update_progressbar_timer(self):
        self.timer_update_progressbar = QTimer()
        self.timer_update_progressbar.timeout.connect(self.update_progressbar)
        self.timer_update_progressbar.start(1000)  # Fire the timer every 1000 ms (1 second)

    def update_progressbar(self):
        gas_meter_value = random.randint(0,100)
        thermometer_value = random.randint(0, 50)

        if gas_meter_value < 20:
            self.progressbar_gas_meter.setStyleSheet(
                """
                    QProgressBar {
                    border: 2px solid #2196F3;
                    border-radius: 5px;
                    background-color: #E0E0E0;
                
                    font: bold 15px;  
                    color: black;
                }
                
                QProgressBar::chunk {
                    background-color: #F30000;
                    width: 10px; 
                    margin: 0.5px;
                }"""
            )
        elif gas_meter_value < 50:
            self.progressbar_gas_meter.setStyleSheet(
            """
                QProgressBar {
                border: 2px solid #2196F3;
                border-radius: 5px;
                background-color: #E0E0E0;

                font: bold 15px;  
                color: black;
            }

            QProgressBar::chunk {
                background-color: #F3F300;
                width: 10px; 
                margin: 0.5px;
            }"""
            )
        else:
            self.progressbar_gas_meter.setStyleSheet(
                """
                    QProgressBar {
                    border: 2px solid #2196F3;
                    border-radius: 5px;
                    background-color: #E0E0E0;
                
                    font: bold 15px;  
                    color: black;
                }
                
                QProgressBar::chunk {
                    background-color: #2196F3;
                    width: 10px; 
                    margin: 0.5px;
                }"""
            )

        self.progressbar_gas_meter.setValue(gas_meter_value)
        self.progressbar_thermometer.setValue(thermometer_value)

    def update_ui_timer(self):
        self.update_combo_boxes()

        try:
            with open('selections.txt', 'r') as f:
                selections = f.read().splitlines()
        except FileNotFoundError:
            selections = [None] * 8  # Default to None if the file does not exist

        # Apply previous selections
        for i in range(1, 9):
            combo_box = self.findChild(QComboBox, f'combo_p1_sensor_selector_{i}')
            # if selections[i-1] is not None and selections[i-1] in [combo_box.itemText(j) for j in range(combo_box.count())]:
            combo_box.setCurrentText(selections[i-1])

        self.timer_update_ui = QTimer()
        self.timer_update_ui.timeout.connect(self.update_ui)
        self.timer_update_ui.start(1000)  # Fire the timer every 1000 ms (1 second)

    # update시에는 막아놓을 것, 즉 main_func2 작동시에만 변경 가능
    def port_changed(self, new_port):
        self.page_firmware_update.edit_port_number.setText(str(new_port))
        # Stop the current worker
        self.stop_worker_port_changed(self.current_worker)

        #init
        self.current_worker = None
        # Create and start a new worker with the new port
        self.worker_debugging = Worker(self.run_main_func2, new_port)
        self.current_worker = self.worker_debugging
        self.current_worker.start()

    def stop_worker_port_changed(self, worker):
        if worker is not None and worker.isRunning():  # If the thread is active
            # Stop the thread by setting exit_debug_mode_flag
            main_functions.exit_debug_mode_flag = True
            # True로 둔 것이 끝날 때까지 기다림
            worker.wait()

        main_functions.exit_debug_mode_flag = False

    def ports_refresh_timer(self):
        self.timer_ports_refresh = QTimer()
        self.timer_ports_refresh.timeout.connect(self.fill_ports)
        self.timer_ports_refresh.start(5000)  # Fire the timer every 1000 ms (1 second)

    def fill_ports(self):
        self.combo_port.blockSignals(True)

        # Save current selected item
        current_item = self.combo_port.currentText()

        ports = list_ports.comports()
        self.combo_port.clear()  # Clear existing items

        for port in ports:
            self.combo_port.addItem(str(port.name))

        # Restore previous selection if it still exists
        index = self.combo_port.findText(current_item)
        if index >= 0:
            self.combo_port.setCurrentIndex(index)

        self.combo_port.blockSignals(False)

    def update_ui(self):
        data_time = main_functions.ds3231_date_str
        self.lbl_time.setText(str(data_time))

        for i in range(1, 9):
            combo_box = self.findChild(QComboBox, f'combo_p1_sensor_selector_{i}')
            label = self.findChild(QLabel, f'lbl_p1_sensor_{i}')

            selected_key = combo_box.currentText()
            selected_value = main_functions.display_data.get(selected_key, 'N/A')  # Default to 'N/A' if key is not present

            label.setText(str(selected_value))

    ### main_func thread
    # 직접 실행하는 문
    def run_main_func(self, file, port, check_sum):
        # main_functions.main_func(file, port, check_sum)
        main_func = main_functions.main_func
        self.update_done_state = main_func(file, port, check_sum)


    def run_main_func2(self, port):
        # main_functions.main_func2(port)
        main_func = main_functions.main_func2
        value_extract = main_func(port)

    # 직접 실행하는 문 끝

    # 2번째부터는 여기서 실행
    # update 시작 할 때 : init에서 시그널로 연결 됨.
    def start_func1(self, file, port, check_sum):
        # button 및 window disable
        disable_list = [self.combo_port, self.combo_menu]
        for widget in disable_list:
            widget.setEnabled(False)


        # thread 새로 만들기
        self.worker_firmware_update = Worker(self.run_main_func, file, port, check_sum)
        self.worker_firmware_update.task_done.connect(self.update_done_signal)

        self.switch_workers(self.worker_firmware_update)

    # update 끝나고 done 눌렀을 때 : init에서 시그널로 연결 됨.
    def start_func2(self, port):
        able_list = [self.combo_port, self.combo_menu]
        for widget in able_list:
            widget.setEnabled(True)

        self.worker_debugging = Worker(self.run_main_func2, port)
        self.switch_workers(self.worker_debugging)
        self.timer_update_ui.start(1000)
    # 2번째부터는 여기서 실행 끝

    def switch_workers(self, next_worker):
        if self.current_worker is not None:
            self.timer_update_ui.stop()
            main_functions.exit_debug_mode_flag = True
            self.current_worker.wait()

        self.current_worker = None
        self.current_worker = next_worker
        self.current_worker.start()
    ## main_func thread End

    ### 여기 추후에 dict로 받아서, unit, max, min 등도 parameter로 넣기
    def init_gauge(self, gauge):
        gauge.units = "Km/h"
        gauge.enableBarGraph = True
        gauge.setMouseTracking(False)
        gauge.maxValue = 255
        gauge.minValue = 0
        gauge.updateValue(0)

        # 사용할만한 theme
        # gauge.setGaugeTheme(0)
        # gauge.setGaugeTheme(2)

    # combobox가 변경됐을 때 바로 실행 # 페이지 움직이기 전부터 페이지 옮기는 것까지
    def change_stacked_widget(self, index):
        self.prev_page = self.stacked_widget.currentIndex()
        self.prev_page_name = self.stacked_widget.currentWidget()

        current_page = self.combo_menu.currentText()
        if index == -1:  # No item selected
            # Here you can handle the case where no item is selected
            pass

        elif current_page == self.menu_page_name[0]:  # If the first item is selected
            self.lbl_title.setText(str(self.menu_page_name[0]))
            self.stacked_widget.setCurrentWidget(self.page_firmware_update)
            self.btn_right.setDisabled(True)
            self.btn_left.setDisabled(True)
            self.btn_right.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
            self.btn_left.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
            self.combo_menu.setEnabled(False)

        elif current_page == self.menu_page_name[1]:  # If the first item is selected
            self.customizing_pages()

        elif current_page == "Option 3":  # If the first item is selected
            pass

        else:
            pass

    def customizing_pages(self):
        ### page_main
        for i in range(1, 9):  # range(1, 13)는 1부터 12까지의 숫자를 생성합니다.
            combo_sensor_selector = f"combo_p1_sensor_selector_{i}"  # f-string을 사용하여 위젯 이름 생성
            combo_sensor_selector_ = getattr(self, combo_sensor_selector)  # getattr 함수로 동적으로 위젯 참조 얻기
            combo_sensor_selector_.show()
        self.btn_custom_setting.show()
        self.combo_menu.setEnabled(False)

        for label_name in self.editable_labels:
            label = self.findChild(QLabel, label_name)
            if label:
                label.setStyleSheet("QLabel { border: 1px solid gray; background-color: lightyellow; }")
                label.mousePressEvent = lambda event, l=label: self.label_clicked(l)


        for combo_gauge in self.combo_gauges:
            getattr(self, combo_gauge).show()  # getattr 함수로 동적으로 위젯 참조 얻기
        ### page_btn

        ### page_digital_status

        ### sensors



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
        self.stacked_widget.setCurrentIndex(self.prev_page)
        self.combo_menu.setCurrentIndex(-1)
        self.naming_title(self.prev_page)

        self.combo_menu.setEnabled(True)
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