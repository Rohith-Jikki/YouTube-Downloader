from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QLineEdit, QMainWindow, QLabel
import youtube_dl.YoutubeDL as YDL
import sys, os, time, shutil
from style import *
from tkinter import filedialog
from tkinter import *
from threading import Thread
import urllib

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
        self.setGeometry(200, 200, 651, 395)
        self.setFixedSize(651, 395)
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
        self.nameLabel.setGeometry(QtCore.QRect(240, 18, 172, 46))
        self.nameLabel.setFont(font)
        self.nameLabel.setStyleSheet("color:white;")

        # TextBox
        self.textbox = QLineEdit(self)
        self.textbox.setGeometry(QtCore.QRect(33, 73, 495, 50))
        self.textbox.setFont(fontin)
        self.textbox.setStyleSheet(tstyle)

        #TextEdit
        self.textEdit = QtWidgets.QTextBrowser(self)
        self.textEdit.setGeometry(QtCore.QRect(244, 142, 392, 125))
        self.textEdit.setStyleSheet(serachStyle)

        #Thumbnail
        self.thumbnail = QLabel(self, text = 'Test')
        self.thumbnail.setGeometry(33, 142,379, 125 )
        self.pixmap = QtGui.QPixmap()
        self.thumbnail.setPixmap(self.pixmap)

        #ComboBox
        self.comboBox = QtWidgets.QComboBox(self)
        self.comboBox.setGeometry(QtCore.QRect(33, 286, 190, 32))
        self.comboBox.setStyleSheet(tstyle)
        self.options = ["video", "audio"]
        self.comboBox.addItems(self.options)
        # Buttons

        # Button 1
        self.b1 = QtWidgets.QPushButton(self, text="Search")
        self.b1.setGeometry(QtCore.QRect(536, 73, 100, 50))
        self.b1.setFont(font)
        # self.b1.clicked.connect(lambda: self.button_click(self.b1, 'video'))
        self.b1.clicked.connect(lambda: self.button_click(self.b1, 'search'))
        self.b1.setStyleSheet(btn)

        # Button 2
        self.b2 = QtWidgets.QPushButton(self, text="Download")
        self.b2.setGeometry(QtCore.QRect(276, 326, 100, 50))
        self.b2.setFont(font)
        self.b2.setStyleSheet(btn)
        self.b2.clicked.connect(lambda: self.button_click(self.b2, 'download'))  

    def button_click(self, button, type):
        self.videoname = self.textbox.text()
        button.setStyleSheet(btnc)
        if type == 'search':
            self.search()
        else:
            # Start a download thread
            type = self.options[self.comboBox.currentIndex()]
            Thread(target=self.download, args=(self.videoname, type)).start()
            button.setText("OK")

    # Search
    def search(self):
        link = self.videoname
        with YDL(ydl_video_opts) as ydl:
            info = ydl.extract_info(f'ytsearch:{link}', download=False)['entries'][0]
            self.video_url = info.get("webpage_url")
            self.video_title = info.get('title', None)
            self.video_uploader = info.get('channel', None)
            self.video_thumb = info.get("thumbnail")
            self.video_duration = time.strftime('%M:%S', time.gmtime(info.get("duration")))
            self.video_views = MainWindow.human_format(info.get('view_count'))
        self.textEdit.setHtml(f"<style>a{{color: white; text-decoration: none;}}</style><a href =\"{self.video_url}\"><h3>{self.video_title}</h3></a> <p><b>Duration: </b>{self.video_duration}</p>")
        self.textEdit.setOpenExternalLinks(True)
        data = urllib.request.urlopen(self.video_thumb).read()
        self.pixmap.loadFromData(data)
        self.pixmap_rescaled = self.pixmap.scaled(211, 125, QtCore.Qt.KeepAspectRatio)
        self.thumbnail.setPixmap(self.pixmap_rescaled)
        

    # Download Function   
    def download(self, link, type="video"):
        opts = ydl_video_opts if type == "video" else ydl_audio_opts
        with YDL(opts) as ydl:
            info = ydl.extract_info(f'ytsearch:{link}', download=False)['entries'][0]
            video_url = info.get("webpage_url")
            ydl.download([video_url])
            for file in os.listdir("./"):
                if (type == "video" and file.endswith((".mp4", ".mkv", ".webm"))) or (type == "audio" and file.endswith(".mp3")):
                    file_path = os.path.abspath(f"./{file}")
                    MainWindow.move_file(self, file_path)

    # Move Downloaded file
    def move_file(self, file_path):
        root = Tk()
        root.withdraw()
        destination = filedialog.askdirectory()
        if destination:    
            root.destroy()
            shutil.move(file_path, destination)

    # Human Format
    def human_format(num):
        num = float('{:.3g}'.format(num))
        magnitude = 0
        while abs(num) >= 1000:
            magnitude += 1
            num /= 1000.0
        return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
