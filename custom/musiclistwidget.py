
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QFileDialog,QAbstractItemView,QMenu
import os
import eyed3

support_ext = [".mp3"]

class MusicListMan():
    def __init__(self, _music_list_widget):
        self.music_list_widget = _music_list_widget
        self.music_info_map = dict()
    
    def addMusic(self, url):
        ext = os.path.splitext(url)[1].lower()
        if (ext in support_ext):
            filename = os.path.split(url)[1]
            if (filename in self.music_info_map.keys()):
                self.music_list_widget.main_window.Log_Lw.Error("列表中已经包含文件: " + filename)
                return
            self.music_info_map[filename] = (filename, url, 0)
            self.music_list_widget.addItem(os.path.split(url)[1])
            self.music_list_widget.main_window.Log_Lw.Info("添加文件: " + url)
        else:
            self.music_list_widget.main_window.Log_Lw.Waring("只能添加mp3或者flac后缀的文件")
            
    def delMusic(self, filename):
        items = self.music_list_widget.findItems(filename, QtCore.Qt.MatchFlag.MatchExactly)
        for item in items:
            self.music_list_widget.takeItem(self.music_list_widget.row(item))
            del self.music_info_map[filename]
            
    def getFullName(self, filename):
        if (filename in self.music_info_map.keys()):
            return self.music_info_map[filename][1]
        else:
            return ""


class MusicListWidget(QtWidgets.QListWidget):
    def __init__(self, *args, **kwargs):
        super(MusicListWidget, self).__init__(*args, **kwargs)
        self.setAcceptDrops(True)
        self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        
        self.music_list_man = MusicListMan(self)
        
        self.customContextMenuRequested.connect(self.rightMenuShow)
        self.itemClicked.connect(self.clickedItem)
    
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
        support_list = ""
        for support in support_ext:
            support_list += (" *" + support)
        files = QFileDialog.getOpenFileNames(self, "选择音乐文件(支持多选)", "", "音乐文件 (" + support_list + ")")
        for file in files[0]:
            self.music_list_man.addMusic(file)
                
    def rightMenuShow(self):
        popMenu = QMenu()
        popMenu.addAction(QtGui.QAction(u'添加', self, triggered=self.addMusic))
        popMenu.addAction(QtGui.QAction(u'删除', self, triggered=self.removeMusic))
        popMenu.exec(QtGui.QCursor.pos())
    
    def removeMusic(self):
        items = self.selectedItems()
        for item in items:
            self.music_list_man.delMusic(item.text())
            
    def loadInfo(self):
        if not self.audiofile:
            raise "载入失败"
        self.main_window.Title_Le.setText(self.audiofile.tag.title if self.audiofile.tag.title else "")
        self.main_window.Artist_Te.setText(self.audiofile.tag.artist if self.audiofile.tag.artist else "")
        self.main_window.Album_Le.setText(self.audiofile.tag.album if self.audiofile.tag.album else "")
        if len(self.audiofile.tag.lyrics) == 0:
            lrc_text = ""
        else:
            lrc_text = self.audiofile.tag.lyrics[0].text
        self.main_window.Lrc_Te.setText(lrc_text)
        if not self.audiofile.info:
            raise "文件格式错误 获取不到文件信息"
        self.main_window.Time_Tl.setText(eyed3.utils.formatTime(self.audiofile.info.time_secs))
        
    def saveInfo(self):
        if not self.audiofile:
            raise "没有选择文件"
        self.audiofile.tag.title = self.main_window.Title_Le.text()
        self.audiofile.tag.artist = self.main_window.Artist_Te.text()
        self.audiofile.tag.album = self.main_window.Album_Le.text()
        self.audiofile.tag.lyrics.set(self.main_window.Lrc_Te.toPlainText())
        self.audiofile.tag.save()
        self.main_window.Log_Lw.Info("保存成功: " + self.audiofile.tag.file_info.name)
        
    def clickedItem(self, item):
        fullname = self.music_list_man.getFullName(item.text())
        if fullname != "":
            try:
                self.audiofile = eyed3.load(fullname)
                self.loadInfo()
            except Exception as e:
                self.main_window.Log_Lw.Error("载入文件失败：" + str(e))
            
        else:
            self.main_window.Log_Lw.Debug(item.text())
        
    def SetMainWindow(self, main_window):
        self.main_window = main_window