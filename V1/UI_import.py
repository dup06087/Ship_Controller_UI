from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog

import sys


form_window = uic.loadUiType("UI_V1.ui")[0]

class UiMainWindow(QtWidgets.QMainWindow, form_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def File_Dialog(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "All Files (*)",
                                                  options=options)
        if fileName:
            print(fileName)

    def Checksum_ON_OFF(self):
        pass

    def Ok_Clicked(self):
        pass

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = UiMainWindow()
    main_window.show()
    sys.exit(app.exec_())
