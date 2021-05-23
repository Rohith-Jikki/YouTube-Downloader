from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QLineEdit, QMainWindow, QLabel
import youtube_dl.YoutubeDL as YDL
import sys, os, subprocess

ydl_audio_opts = {
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True,
            'format': 'bestaudio/best',
            'outtmpl': '%(title)s.%(ext)s',
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
            'outtmpl': '%(title)s.%(ext)s',
        }

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setGeometry(200, 200, 300, 300)
        self.setFixedSize(620, 250)
        self.setWindowOpacity(1)
        self.setWindowTitle("YouTube Downloader")
        self.setStyleSheet("color: black; background-color: rgb(35, 35, 35)")
        self.setWindowIcon(QtGui.QIcon('ytlogo.png'))
        self.initUI()
        
    def initUI(self):
        fontin = QtGui.QFont()
        font = QtGui.QFont()
        font.setPointSize(12)
        fontin.setPointSize(11)
        #Label
        self.nameLabel = QLabel(self)
        self.nameLabel.setText('Enter Link or Search:')
        self.nameLabel.setGeometry(QtCore.QRect(10, 50, 181, 41))
        self.nameLabel.setFont(font)
        self.nameLabel.setStyleSheet("color:white;")
        #TextBox
        self.textbox = QLineEdit(self)
        self.textbox.setGeometry(QtCore.QRect(200, 50, 401, 41))
        self.textbox.setFont(fontin)
        self.textbox.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-radius:5px;\n"
"border : solid #a0a0a0;\n"
"border-width : 2px\n"
"")
        ##Buttons
        #Button 1
        self.b1 = QtWidgets.QPushButton(self)
        self.b1.setText("MP4")
        self.b1.setGeometry(QtCore.QRect(220, 110, 100, 50))
        self.b1.setFont(font)
        self.b1.clicked.connect(self.b1click)
        self.b1.setStyleSheet("border-radius: 5px;\n"
"border: solid #393939;\n"
"border-width: 4px;\n"
"background-color: #414141;\n"
"color: white;\n"
"")
        #Button2
        self.b2 = QtWidgets.QPushButton(self)
        self.b2.setText("MP3")
        self.b2.setGeometry(QtCore.QRect(450, 110, 100, 50))
        self.b2.setFont(font)
        self.b2.setStyleSheet("border-radius: 5px;\n"
"border: solid #393939;\n"
"border-width: 4px;\n"
"background-color: #414141;\n"
"color: white;\n"
"")
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
            video_url = info.get("webpage_url")
            ydl.download([video_url])
            for file in os.listdir("./"):
                if file.endswith(".mp4") or file.endswith(".mkv"):
                    file_path = os.path.abspath(f"./{file}")
                    subprocess.call(f"explorer /select,{file_path}")

    def dldaudio(self, link):
        with YDL(ydl_audio_opts) as ydl:
            info = ydl.extract_info(f'ytsearch:{link}', download=False)['entries'][0]
            video_url = info.get("webpage_url")
            ydl.download([video_url])
            for file in os.listdir("./"):
                if file.endswith(".mp3"):
                    file_path = os.path.abspath(f"./{file}")
                    subprocess.call(f"explorer /select,{file_path}")

def window():
    # Window
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())

window()
