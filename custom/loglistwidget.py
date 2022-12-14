
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QColor

class LogListWidget(QtWidgets.QListWidget):
    def __init__(self, *args, **kwargs):
        super(LogListWidget, self).__init__(*args, **kwargs)
    
    def Info(self, log):
        item = QtWidgets.QListWidgetItem(log)
        # item.setBackground(QtGui.QColor(144,238,144))
        self.insertItem(0, item)
        
    def Error(self, log):
        item = QtWidgets.QListWidgetItem(log)
        item.setBackground(QtGui.QColor(240,128,128))
        self.insertItem(0, item)
        
    def Waring(self, log):
        item = QtWidgets.QListWidgetItem(log)
        item.setBackground(QtGui.QColor(255,255,224))
        self.insertItem(0, item)
        
    def Debug(self, log):
        return
        item = QtWidgets.QListWidgetItem(log)
        item.setBackground(QtGui.QColor(220,220,220))
        self.insertItem(0, item)

    def SetMainWindow(self, main_window):
        self.main_window = main_window
