import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QMessageBox

def dialog():
    a = QMessageBox()
    # a.setText("여기에 출력되요")
    # a.setDetailedText("상세 항목이 나와요")
    # a.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    a.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # w= QWidget()
    # w.resize(300,300)
    # w.setWindowTitle("안녕 컴퓨터")
    # label = QLabel(w)
    # label.setText("여기는 라벨이에요")
    # label.move(100,130)
    # label.show()
    # btn = QPushButton(w) #위젯 집어넣기
    # btn.setText("여기는 푸시 버튼")
    # btn.move(110,150) #버튼의 위치 이동
    # btn.clicked.connect(dialog) #btn이 눌리면 dialog 함수 호출
    # btn.show() #버튼을 보여줌
    dialog()
    # w.show() # 중요 window는 기본값이 hidden이라 show 해야함
    sys.exit(app.exec_()) # 이상태는 이벤트 루프가 돌고있다.