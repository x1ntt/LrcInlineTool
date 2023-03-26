from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog,QAbstractItemView,QMenu,QTableWidget,QTableWidgetItem,QMenu,QAction
import os
import re

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
        self.main_window.Log_Lw.Info(f"通过 {source.source_name}, 获取{self.main_window.LrcMusicName_Le.text()}歌词")
    
    def resultList(self, error_str, result_list):
        if (error_str != ""):
            self.main_window.Log_Lw.Waring(f"获取结果列表失败 {error_str}")
        if len(result_list) == 0:
            self.main_window.Log_Lw.Waring(f"获取歌词结果为空 {error_str}")
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
        self.main_window.Log_Lw.Info(f"获取到{str(len(result_list))}条结果")
        
    def lrcResult(self, error_str, lrcs, music_id, reason):
        if (error_str != ""):
            self.main_window.Log_Lw.Waring (f"获取歌词失败 {error_str}")
        self.main_window.Log_Lw.Debug(f"获取歌词成功 {music_id}")
        self.lrc_result_map[music_id] = lrcs
        self.current_music_id = music_id
        if reason == 1:
            self.main_window.lang_comboBox.clear()
            for k in lrcs.keys():
                self.main_window.lang_comboBox.addItem(k)
            if len(lrcs.keys()):
                self.main_window.lang_comboBox.setCurrentIndex(0)

        elif reason == 2:
            lrc_name = os.path.splitext(self.music_file_name)[0]
            file_name, selected_filter = QFileDialog.getSaveFileName(self, "保存为：", lrc_name, "歌词文件 (*.lrc)")
            if len(file_name) != 0:
                try:
                    with open(file_name, "w") as f:
                        f.write(lrcs["lyric"])
                except Exception as e:
                    self.main_window.Log_Lw.Error(f"保存歌词错误 {file_name}")
                    return
                self.main_window.Log_Lw.Info(f"写入歌词到 {file_name}")

    def getLrc(self, reason):
        current_source = self.main_window.Source_Cb.currentText()
        source = self.source_map[current_source]
        source.SetCallbackObject(self)
        if self.currentRow() == -1:
            return 
        mid = self.search_result_map[self.currentRow()].music_id
        if mid in self.lrc_result_map.keys():
            cur_lrc = self.lrc_result_map[mid]
            self.lrcResult("", cur_lrc, mid, reason)
        else:
            source.getLrc(str(mid), reason)
        
    def rightMenuShow(self, pos):
        popMenu = QMenu()
        item = popMenu.addAction(u'左侧显示歌词')
        item2 = popMenu.addAction(u'另存为lrc歌词')
        action = popMenu.exec(QtGui.QCursor.pos())
        if action == item:
            self.getLrc(1)
        elif action == item2:
            self.getLrc(2)
        
    def SetMainWindow(self, main_window):
        self.main_window = main_window
    
    def updateLrc(self, pos):
        cur_lrc_type = self.main_window.lang_comboBox.currentText()
        if len(cur_lrc_type) == 0:
            return
        cur_lrc = self.lrc_result_map[self.current_music_id][cur_lrc_type]
        self.main_window.Lrc_Te.setText(cur_lrc)
    
    def mergeLrc(self):
        '''
            将会合并原文和翻译，仅依据lrc文件里面的时间
        '''
        try:
            lrcs = self.lrc_result_map[self.current_music_id]
        except Exception:
            return

        if "lyric" not in lrcs.keys():
            return
        if "tlyric" not in lrcs.keys():
            return
        lyric = lrcs["lyric"]
        tlyric = lrcs["tlyric"]
        lyric_list = lyric.split('\n')
        tlyric_list = tlyric.split('\n')

        target = []
        for str in lyric_list:
            target.append(str)
            res = re.findall("^\[.*\]", str)
            if len(res):
                for s in tlyric_list:
                    if res[0] in s:
                        target.append(s)
                        break
        target_str = "\n".join(target)
        self.main_window.Lrc_Te.setText(target_str)