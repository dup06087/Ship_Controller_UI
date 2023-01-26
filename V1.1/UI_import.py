from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog

import sys
import main

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
            self.lineEdit.setText(fileName)

    def Checksum_ON_OFF(self):
        pass

    def Ok_Clicked(self):
        print(self.lineEdit.text())
        main.bin_file = self.lineEdit.text()
        print(self.lineEdit_2.text())
        main.port = "COM" + self.lineEdit_2.text()
        print(self.checkBox.checkState())
        if self.checkBox.checkState():
            main.skip_checksum = True
            print("skip checksum")
        main.check_main_func = main.main_func(main.bin_file, main.port,main.skip_checksum)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = UiMainWindow()
    main_window.show()
    sys.exit(app.exec_())