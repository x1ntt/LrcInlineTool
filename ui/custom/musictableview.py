
from PyQt6 import QtCore, QtGui, QtWidgets

class MusicTableView(QtWidgets.QTableView):
    def __init__(self, *args, **kwargs):
        super(MusicTableView, self).__init__(*args, **kwargs)
        self.setAcceptDrops(True)
    
    def dragEnterEvent(self, e):
        e.accept()
    
    def dragMoveEvent(self, e):
        e.accept()
    
    def dropEvent(self, e):
        self.main_window.Log_Lv.Info("放开")
        print ("放开")
        
    def SetMainWindow(self, main_window):
        self.main_window = main_window