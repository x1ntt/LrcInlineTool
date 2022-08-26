
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QColor

class LogListWidget(QtWidgets.QListWidget):
    def __init__(self, *args, **kwargs):
        super(LogListWidget, self).__init__(*args, **kwargs)
    
    def Info(self, log):
        item = QtWidgets.QListWidgetItem(log)
        item.setBackground(QtGui.QColor(144,238,144))
        self.addItem(item)
        
    def Error(self, log):
        item = QtWidgets.QListWidgetItem(log)
        item.setBackground(QtGui.QColor(240,128,128))
        self.addItem(item)
        
    def Waring(self, log):
        item = QtWidgets.QListWidgetItem(log)
        item.setBackground(QtGui.QColor(255,255,224))
        self.addItem(item)
        
    def Debug(self, log):
        item = QtWidgets.QListWidgetItem(log)
        item.setBackground(QtGui.QColor(220,220,220))
        self.addItem(item)

    def SetMainWindow(self, main_window):
        self.main_window = main_window