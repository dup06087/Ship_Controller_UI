from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QPalette, QBrush, QIcon
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal, QUrl
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QComboBox, QLineEdit, QPushButton, QVBoxLayout

import sys

from PyQt5 import QtWidgets, uic


class Page_Firmware_Update(QWidget):
    button_clicked_signal = pyqtSignal()

    def __init__(self, parent=None):
        super(Page_Firmware_Update, self).__init__(parent)
        uic.loadUi('firmware_ui.ui', self)

    def btn_back_clicked(self):
        self.button_clicked_signal.emit()

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