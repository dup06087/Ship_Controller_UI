from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QPalette, QBrush
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget
import sys

from PyQt5 import QtWidgets, uic


class Page_Firmware_Update(QWidget):
    button_clicked_signal = pyqtSignal()

    def __init__(self, parent=None):
        super(Page_Firmware_Update, self).__init__(parent)
        uic.loadUi('firmware_ui.ui', self)

    def btn_back_clicked(self):
        self.button_clicked_signal.emit()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Load the main UI
        uic.loadUi("Theme.ui", self)

        #window size and other options
        self.setFixedSize(1600, 900)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        # menu box
        self.combo_menu.addItem("Option 1")
        self.combo_menu.addItem("Option 2")
        self.combo_menu.addItem("Option 3")
        self.combo_menu.currentIndexChanged.connect(self.change_stacked_widget)
        self.combo_menu.setCurrentIndex(-1)

        # firmware update page init
        self.page_firmware_update = Page_Firmware_Update(self)
        self.stacked_widget.addWidget(self.page_firmware_update)
        self.page_firmware_update.button_clicked_signal.connect(self.page_firmware_update_btn_back_clicked)

        #
        self.hidden_pages = [self.page_firmware_update.objectName()]

    def change_stacked_widget(self, index):
        if index == -1:  # No item selected
            # Here you can handle the case where no item is selected
            pass

        elif self.combo_menu.currentText() == "Option 1":  # If the first item is selected
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
        self.prev_page_name = self.stacked_widget.currentWidget()
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

    def prev_page(self):
        self.prev_page_name = self.stacked_widget.currentWidget()
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

    def page_firmware_update_btn_back_clicked(self):
        print("Button in child widget was clicked!")
        # combo menu -1 index로 초기화
        self.combo_menu.setCurrentIndex(-1)

        self.stacked_widget.setCurrentWidget(self.prev_page_name)
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