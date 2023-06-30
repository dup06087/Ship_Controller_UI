from PyQt5 import QtWidgets, uic

class MyWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        uic.loadUi('main_page.ui', self)

        # QLabel to QLineEdit
        self.sensor_value_edit = QtWidgets.QLineEdit("Type your value", self)
        self.sensor_value_edit.setGeometry(self.lbl_sensor_value.geometry())
        self.sensor_value_edit.hide()

        # QLabel to QComboBox
        self.sensor_name_combo = QtWidgets.QComboBox(self)
        self.sensor_name_combo.addItems(["Choice 1", "Choice 2", "Choice 3"])
        self.sensor_name_combo.setGeometry(self.lbl_sensor_name.geometry())
        self.sensor_name_combo.hide()

        # Connect checkbox state change signal to a custom slot
        self.chk_custom.stateChanged.connect(self.customize_ui)

        self.combo_hide.hide()
        self.show()

    def customize_ui(self, state):
        if state == QtCore.Qt.Checked:
            # Show QLineEdit and QComboBox and hide QLabel
            self.sensor_value_edit.show()
            self.lbl_sensor_value.hide()
            self.sensor_name_combo.show()
            self.lbl_sensor_name.hide()
        else:
            # Hide QLineEdit and QComboBox and show QLabel
            self.sensor_value_edit.hide()
            self.lbl_sensor_value.show()
            self.sensor_name_combo.hide()
            self.lbl_sensor_name.show()

if __name__ == "__main__":
    import sys
    from PyQt5 import QtCore
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())