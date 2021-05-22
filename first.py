from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QFormLayout, QInputDialog, QLineEdit, QMainWindow
from pytube import YouTube
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setGeometry(200, 200, 300, 300)
        self.setWindowTitle("Test Application")
        self.initUI()
        
    def initUI(self):
        self.b1 = QtWidgets.QPushButton(self)
        self.b1.setText("Click")
        self.b1.clicked.connect(self.b1click)

    def b1click(self):
        # self.download()
        self.update()
        
    # def download(self):
    #     self.yt = YouTube(self.link)
    #     self.yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download()

def window():
    # Window
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())

window()