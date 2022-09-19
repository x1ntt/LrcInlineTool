
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog,QAbstractItemView,QMenu,QAction
import os
import eyed3

from process.handle_mp3 import Handle_mp3
from process.handle_flac import Handle_flac


support_ext = [".mp3", ".flac"]

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
        
        self.music_info_obj = None
    
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
        files = QFileDialog.getOpenFileNames(self, "选择音乐文件(支持多选)", "D:\\CloudMusic", "音乐文件 (" + support_list + ")")
        for file in files[0]:
            self.music_list_man.addMusic(file)
                
    def rightMenuShow(self):
        popMenu = QMenu()
        popMenu.addAction(QAction(u'添加', self, triggered=self.addMusic))
        popMenu.addAction(QAction(u'删除', self, triggered=self.removeMusic))
        popMenu.exec(QtGui.QCursor.pos())
    
    def removeMusic(self):
        items = self.selectedItems()
        for item in items:
            self.music_list_man.delMusic(item.text())
            
    def loadInfo(self, fullname):
        tmp = fullname.split(".")
        if len(tmp) < 2:
            raise "文件名不正确 缺少后缀名"
        ext_name = tmp[-1]
        
        if ext_name == "mp3":
            self.music_info_obj = Handle_mp3(fullname)
        elif ext_name == "flac":
            self.music_info_obj = Handle_flac(fullname)
        else:
            raise f"无法处理的后缀名{ext_name}"
        
        if self.music_info_obj == None:
            raise "获取歌曲信息"
        
        info_dict = self.music_info_obj.getInfo()
        
        self.main_window.Title_Le.setText(info_dict['music_name'] if 'music_name' in info_dict else "")
        self.main_window.LrcMusicName_Le.setText(info_dict['music_name'] if'music_name' in info_dict else "")
        self.main_window.Artist_Te.setText(info_dict['artist_name'] if 'artist_name' in info_dict else "")
        self.main_window.LrcArt_Le.setText(info_dict['artist_name'] if 'artist_name' in info_dict else "")
        self.main_window.Album_Le.setText(info_dict['alnum_name'] if 'alnum_name' in info_dict else "")
        
        if ("lyrics" not in info_dict):
            lrc_text = ""
        else:
            lrc_text = info_dict['lyrics']
        self.main_window.Lrc_Te.setText(lrc_text)
        
        # if not self.audiofile.info:
        #    raise "文件格式错误 获取不到文件信息"
        # self.main_window.Time_Tl.setText(eyed3.utils.formatTime(self.audiofile.info.time_secs))
        
    def saveInfo(self):
        if self.music_info_obj == None:
            raise "没有选择文件"
        
        info_dict = dict()
        
        info_dict['music_name'] = self.main_window.Title_Le.text()
        info_dict['artist_name'] = self.main_window.Artist_Te.text()
        info_dict['alnum_name'] = self.main_window.Album_Le.text()
        info_dict['lyrics'] = self.main_window.Lrc_Te.toPlainText()
        
        self.music_info_obj.setInfo(info_dict)
        self.music_info_obj.save()
        self.main_window.Log_Lw.Info("保存成功: " + self.getCurMusicName())
        
    def clickedItem(self, item):
        fullname = self.music_list_man.getFullName(item.text())
        if fullname != "":
            # try:
            self.loadInfo(fullname)
            # except Exception as e:
                # self.main_window.Log_Lw.Error("载入文件失败：" + str(e))
            
        else:
            self.main_window.Log_Lw.Debug(item.text())
        
    # 获取当前选择的音乐文件名
    def getCurMusicName(self):
        item = self.currentItem()
        if item == None:
            return
        return item.text()
        
    # 获取带路径的全名
    def getCurMusicFullName(self):
        item = self.currentItem()
        if item == None:
            return
        fullname = self.music_list_man.getFullName(item.text())
        if fullname != "":
            return fullname
        return ""
        
    def SetMainWindow(self, main_window):
        self.main_window = main_window
