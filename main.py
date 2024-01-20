import sys

from views.main_window import Ui_MainWindow
from PySide2.QtWidgets import *

class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MyMainWindow, self).__init__()
        self.setupUi(self)

if __name__ == "__main__":
    app = QApplication([])  # Create the application object
    main_window = MyMainWindow()  # Create an instance of your MainWindow class
    main_window.show()  # Show the main window
    sys.exit(app.exec_())  # Start the application event loop