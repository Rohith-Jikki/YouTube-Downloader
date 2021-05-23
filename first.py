from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QFormLayout, QLineEdit, QMainWindow, QLabel
from pytube import YouTube
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setGeometry(200, 200, 300, 300)
        self.setWindowTitle("YouTube Downloader")
        self.initUI()
        
    def initUI(self):
        self.nameLabel = QLabel(self)
        self.nameLabel.setText('Enter Link:')
        self.nameLabel.move(0, 0)
        self.textbox = QLineEdit(self)
        self.textbox.move(15, 30)
        self.textbox.resize(280,40)
        self.b1 = QtWidgets.QPushButton(self)
        self.b1.setText("MP4")
        self.b1.move(110, 90)
        self.b1.resize(80,40)
        self.b1.clicked.connect(self.b1click)
        self.b2 = QtWidgets.QPushButton(self)
        self.b2.setText("MP3")
        self.b2.move(110, 130)
        self.b2.resize(80,40)
        self.b2.clicked.connect(self.b2click)

    def b1click(self):
        self.textcontent = self.textbox.text()
        self.dld(self.textcontent)
        self.b1.setText("Ok !!!!")
        
    def b2click(self):
        self.b2.setText("OK !!!")

    def dld(self, link):
        yt = YouTube(link)
        yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download()

def window():
    # Window
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())

window()