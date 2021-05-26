from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QLineEdit, QMainWindow, QLabel
import youtube_dl.YoutubeDL as YDL
import sys, os, time, shutil
from style import *
from tkinter import filedialog
from tkinter import *
from threading import Thread

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
        self.setFixedSize(650, 270)
        self.setWindowOpacity(1)
        self.setWindowTitle("YouTube Downloader")
        self.setWindowIcon(QtGui.QIcon('ytlogo.png'))
        self.setStyleSheet(appStyle)
        self.initUI()
        
    def initUI(self):
        fontin = QtGui.QFont()
        font = QtGui.QFont()
        font.setPointSize(12)
        fontin.setPointSize(11)

        # Label
        self.nameLabel = QLabel(self, text='Enter Link or Search:')
        self.nameLabel.setGeometry(QtCore.QRect(10, 50, 181, 41))
        self.nameLabel.setFont(font)
        self.nameLabel.setStyleSheet("color:white;")

        # TextBox
        self.textbox = QLineEdit(self)
        self.textbox.setGeometry(QtCore.QRect(200, 50, 450, 41))
        self.textbox.setFont(fontin)
        self.textbox.setStyleSheet(tstyle)

        # Buttons

        # Button 1
        self.b1 = QtWidgets.QPushButton(self, text="MP4")
        self.b1.setGeometry(QtCore.QRect(220, 110, 100, 50))
        self.b1.setFont(font)
        self.b1.clicked.connect(lambda: self.button_click(self.b1, 'video'))
        self.b1.setStyleSheet(btn)

        # Button 2
        self.b2 = QtWidgets.QPushButton(self, text="MP3")
        self.b2.setGeometry(QtCore.QRect(450, 110, 100, 50))
        self.b2.setFont(font)
        self.b2.setStyleSheet(btn)
        self.b2.clicked.connect(lambda: self.button_click(self.b2, 'audio'))  

    def button_click(self, button, type):
        videoname = self.textbox.text()
        button.setStyleSheet(btnc)
        if videoname:
            # Start a download thread
            Thread(target=self.download, args=(videoname, type)).start()
            button.setText("OK")

    # Search
    def search(self, link):
        with YDL(ydl_video_opts) as ydl:
            info = ydl.extract_info(f'ytsearch:{link}', download=False)['entries'][0]
            self.video_url = info.get("webpage_url")
            self.video_title = info.get('title', None)
            self.video_thumb = info.get("thumbnail")
            self.video_duration = time.strftime('%M:%S', time.gmtime(info.get("duration")))

    # Download Function   
    def download(self, link, type="video"):
        opts = ydl_video_opts if type == "video" else ydl_audio_opts
        with YDL(opts) as ydl:
            info = ydl.extract_info(f'ytsearch:{link}', download=False)['entries'][0]
            video_url = info.get("webpage_url")
            ydl.download([video_url])
            for file in os.listdir("./"):
                if (type == "video" and file.endswith((".mp4", ".mkv"))) or (type == "audio" and file.endswith(".mp3")):
                    file_path = os.path.abspath(f"./{file}")
                    MainWindow.move_file(self, file_path)

    # Move Downloaded file
    def move_file(self, file_path):
        root = Tk()
        root.withdraw()
        destination = filedialog.askdirectory()
        root.destroy()
        shutil.move(file_path, destination)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
