from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QLineEdit, QMainWindow, QLabel
import youtube_dl.YoutubeDL as YDL
import sys, os

ydl_audio_opts = {
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True,
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

ydl_video_opts = {
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True,
            'format': 'bestvideo+bestaudio/best',
            'videoformat' : "mp4",
        }

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setGeometry(200, 200, 300, 300)
        self.setFixedSize(500, 250)
        self.setWindowOpacity(1)
        self.setWindowTitle("YouTube Downloader")
        self.setStyleSheet("color: white; background-color: rgb(32, 34, 37)")
        self.setWindowIcon(QtGui.QIcon('ytlogo.png'))
        self.initUI()
        
    def initUI(self):
        fontin = QtGui.QFont()
        font = QtGui.QFont()
        font.setPointSize(12)
        fontin.setPointSize(11)
        #Label
        self.nameLabel = QLabel(self)
        self.nameLabel.setText('Enter Link\nor Search:')
        self.nameLabel.setGeometry(QtCore.QRect(20, 38, 81, 41))
        self.nameLabel.setFont(font)
        #TextBox
        self.textbox = QLineEdit(self)
        self.textbox.setGeometry(QtCore.QRect(110, 40, 371, 41))
        self.textbox.setFont(fontin)
        ##Buttons
        #Button 1
        self.b1 = QtWidgets.QPushButton(self)
        self.b1.setText("MP4")
        self.b1.setGeometry(QtCore.QRect(160, 110, 101, 51))
        self.b1.setFont(font)
        self.b1.clicked.connect(self.b1click)
        self.b1.setStyleSheet("background-color: rgb(54, 57, 63)")
        #Button2
        self.b2 = QtWidgets.QPushButton(self)
        self.b2.setText("MP3")
        self.b2.setGeometry(QtCore.QRect(350, 110, 111, 51))
        self.b2.setFont(font)
        self.b2.setStyleSheet("background-color: rgb(54, 57, 63)")
        self.b2.clicked.connect(self.b2click)  

    def b1click(self):
        self.textcontent = self.textbox.text()
        if self.textcontent:
            self.dld(self.textcontent)
            self.b1.setText("Ok !!!!")

    def b2click(self):
        self.textcontent = self.textbox.text()
        if self.textcontent:
            self.dldaudio(self.textcontent)
            self.b2.setText("OK !!!")

    #Download Function
    def dld(self, link):
        with YDL(ydl_video_opts) as ydl:
            info = ydl.extract_info(f'ytsearch:{link}', download=False)['entries'][0]
            video_name = info.get('title', None)
            video_url = info.get("webpage_url")
            ydl.download([video_url])
            for file in os.listdir("./"):
                if file.endswith(".mp4"):
                    os.rename(file, f"{video_name}.mp4")
                elif file.endswith(".mkv"):
                    os.rename(file, f"{video_name}.mkv")

    def dldaudio(self, link):
        with YDL(ydl_audio_opts) as ydl:
            info = ydl.extract_info(f'ytsearch:{link}', download=False)['entries'][0]
            video_name = info.get('title', None)
            video_url = info.get("webpage_url")
            ydl.download([video_url])
            for file in os.listdir("./"):
                if file.endswith(".mp3"):
                    os.rename(file, f"{video_name}.mp3")

def window():
    # Window
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())

window()