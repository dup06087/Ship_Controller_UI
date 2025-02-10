import os
import sys
import time

import PyQt5
import numpy as np
import qtmodern.styles
import qtmodern.windows
import serial
from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox

import UI_main
# import upload_bin_func_and_debug_func

app = QtWidgets.QApplication(sys.argv)
qtmodern.styles.dark(app)

main_window = UI_main.UiMainWindow()
main_window = qtmodern.windows.ModernWindow(main_window)
main_window.show()

sys.exit(app.exec_())




