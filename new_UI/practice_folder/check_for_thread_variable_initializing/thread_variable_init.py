from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic
from PyQt5.QtCore import Qt
from upload_bin_func_and_debug_func import main_func, main_func2, exit_debug_mode_flag

import threading


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        # Load the main UI
        uic.loadUi("Theme.ui", self)

        # window size and other options
        self.setFixedSize(1600, 900)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.stacked_widget.setCurrentIndex(0)

        # Define the threads
        self.thread1 = threading.Thread(target=self.run_main_func, args=("COM6",))
        self.thread2 = threading.Thread(target=self.run_main_func2, args=("COM6",))

        # Start the default thread
        self.current_thread = self.thread2
        self.current_thread.start()

        # Connect the buttons
        self.button1.clicked.connect(self.start_func1)
        self.button2.clicked.connect(self.start_func2)

    def run_main_func(self, port):
        main_func(port)

    def run_main_func2(self, port):
        main_func2(port)

    def start_func1(self):
        self.switch_functions(self.thread1)

    def start_func2(self):
        self.switch_functions(self.thread2)

    def switch_functions(self, next_thread):
        exit_debug_mode_flag = True
        self.current_thread.join()  # Wait for the current thread to finish
        exit_debug_mode_flag = False
        self.current_thread = next_thread
        self.current_thread.start()