
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QFileDialog,QAbstractItemView
import os

support_ext = [".mp3", ".flac"]

class MusicListMan():
    def __init__(self, _music_list_widget):
        self.music_list_widget = _music_list_widget
        self.music_info_map = dict()
    
    def addMusic(self, url):
        ext = os.path.splitext(url)[1].lower()
        if (ext in support_ext):
            self.music_list_widget.main_window.Log_Lw.Info("添加文件: " + url)
            filename = os.path.split(url)[1]
            self.music_info_map[filename] = (filename, url, 0)
            self.music_list_widget.addItem(os.path.split(url)[1])
        else:
            self.music_list_widget.main_window.Log_Lw.Waring("只能添加mp3或者flac后缀的文件")
            
    def delMusic(self, filename):
        items = self.music_list_widget.findItems(filename, QtCore.Qt.MatchFlag.MatchExactly)
        for item in items:
            self.music_list_widget.takeItem(self.music_list_widget.row(item))


class MusicListWidget(QtWidgets.QListWidget):
    def __init__(self, *args, **kwargs):
        super(MusicListWidget, self).__init__(*args, **kwargs)
        self.setAcceptDrops(True)
        self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.music_list_man = MusicListMan(self)
    
    def dragEnterEvent(self, e):
        e.accept()
    
    def dragMoveEvent(self, e):
        e.accept()
    
    def dropEvent(self, e):
        data = e.mimeData()
        if data.hasUrls():
            for data_url in data.urls():
                url = data_url.toLocalFile()
                self.music_list_man.addMusic(url)

    def addMusic(self):
        files = QFileDialog.getOpenFileNames(self, "选择音乐文件(支持多选)", "", "音乐文件 (*.mp3 *.flac)")
        for file in files[0]:
            self.music_list_man.addMusic(file)
                
    def removeMusic(self):
        items = self.selectedItems()
        for item in items:
            self.music_list_man.delMusic(item.text())
        
    def SetMainWindow(self, main_window):
        self.main_window = main_window