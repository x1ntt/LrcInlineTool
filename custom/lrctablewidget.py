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
        
        self.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.rightMenuShow)

    def addSource(self):
        ns = NeteaseSource()
        self.main_window.Source_Cb.addItem(ns.source_name)
        self.source_map[ns.source_name] = ns
        
    def searchLrc(self):
        current_source = self.main_window.Source_Cb.currentText()
        source = self.source_map[current_source]
        search_request = SearchRequest(self.main_window.LrcMusicName_Le.text(), "")
        source.getResultList(search_request)
        source.SetCallbackObject(self)
    
    def resultList(self, error_str, result_list):
        if (error_str != ""):
            print (f"获取搜索结果失败 {error_str}")
        if len(result_list) == 0:
            print ("结果为空")
        self.search_result_map.clear()
        self.setColumnCount(2)
        self.setRowCount(len(result_list))
        cnt = 0
        for result in result_list:
            it = QTableWidgetItem(result.music_name)
            self.setItem(cnt, 0, it)
            it2 = QTableWidgetItem(result.art[0])
            self.setItem(cnt, 1, it2)
            cnt += 1
            
    def lrcResult(self, error_str, lrc):
        if (error_str != ""):
            print (f"获取歌词失败 {error_str}")

    def getLrc(self):
        pass

    def rightMenuShow(self, pos):
        popMenu = QMenu()
        item = popMenu.addAction(u'左侧显示歌词')
        item2 = popMenu.addAction(u'另存为歌词')
        action = popMenu.exec(QtGui.QCursor.pos())
        if action == item:
            print ("1")
        elif action == item2:
            print ("2")
        
    def SetMainWindow(self, main_window):
        self.main_window = main_window
