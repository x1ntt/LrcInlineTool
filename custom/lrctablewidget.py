from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog,QAbstractItemView,QMenu,QTableWidget,QTableWidgetItem,QMenu,QAction
import os

from lrcsource.sourcenetease import NeteaseSource
from lrcsource.sourcebase import SearchRequest

class LrcTableWidget(QTableWidget):
    def __init__(self, *args, **kwargs):
        super(LrcTableWidget, self).__init__(*args, **kwargs);
        self.source_map = dict()
        self.search_result_map = dict()
        self.lrc_result_map = dict()
        
        self.music_file_name = ""
        
        self.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.rightMenuShow)

    def addSource(self):
        ns = NeteaseSource()
        self.main_window.Source_Cb.addItem(ns.source_name)
        self.source_map[ns.source_name] = ns
        
    def searchLrc(self):
        self.music_file_name = self.main_window.musicList.getCurMusicFullName()
        if len(self.main_window.LrcMusicName_Le.text()) == 0:
            return 
        current_source = self.main_window.Source_Cb.currentText()
        source = self.source_map[current_source]
        search_request = SearchRequest(self.main_window.LrcMusicName_Le.text(), "")
        source.SetCallbackObject(self)
        source.getResultList(search_request)
    
    def resultList(self, error_str, result_list):
        if (error_str != ""):
            print (f"获取搜索结果失败 {error_str}")
        if len(result_list) == 0:
            print ("结果为空")
        self.search_result_map.clear()
        self.lrc_result_map.clear()
        self.setColumnCount(2)
        self.setRowCount(len(result_list))
        cnt = 0
        for result in result_list:
            it = QTableWidgetItem(result.music_name)
            self.setItem(cnt, 0, it)
            it2 = QTableWidgetItem("/".join(result.art))
            self.setItem(cnt, 1, it2)
            self.search_result_map[cnt] = result
            cnt += 1
            
    def lrcResult(self, error_str, lrc, music_id, reason):
        if (error_str != ""):
            print (f"获取歌词失败 {error_str}")
        self.lrc_result_map[music_id] = lrc
        if reason == 1:
            self.main_window.Lrc_Te.setText(lrc)
        elif reason == 2:
            lrc_name = os.path.splitext(self.music_file_name)[0]
            file_name, selected_filter = QFileDialog.getSaveFileName(self, "保存为：", lrc_name, "歌词文件 (*.lrc)")
            print ((file_name, selected_filter))
            if len(file_name) != 0:
                with open(file_name, "w") as f:
                    f.write(lrc)

    def getLrc(self, reason):
        current_source = self.main_window.Source_Cb.currentText()
        source = self.source_map[current_source]
        source.SetCallbackObject(self)
        if self.currentRow() == -1:
            return 
        mid = self.search_result_map[self.currentRow()].music_id
        if mid in self.lrc_result_map.keys():
            cur_lrc = self.lrc_result_map[music_id]
            lrcResult("", cur_lrc, mid, reason)
        else:
            source.getLrc(str(mid), reason)
        
    def rightMenuShow(self, pos):
        popMenu = QMenu()
        item = popMenu.addAction(u'左侧显示歌词')
        item2 = popMenu.addAction(u'另存为歌词')
        action = popMenu.exec(QtGui.QCursor.pos())
        if action == item:
            self.getLrc(1)
        elif action == item2:
            self.getLrc(2)
        
    def SetMainWindow(self, main_window):
        self.main_window = main_window
