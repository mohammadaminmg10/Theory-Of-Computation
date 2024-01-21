import sys

from views.main_window import Ui_MainWindow
from PySide2.QtWidgets import *

class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MyMainWindow, self).__init__()
        self.setupUi(self)

if __name__ == "__main__":
    app = QApplication([])
    main_window = MyMainWindow()
    main_window.show()
    sys.exit(app.exec_())