
from PyQt6 import QtCore, QtGui, QtWidgets

class LogListView(QtWidgets.QListView):
    def __init__(self, *args, **kwargs):
        super(LogListView, self).__init__(*args, **kwargs)
    
    def Info(self, log):
        print ("LoG: " + log)

    def SetMainWindow(self, main_window):
        self.main_window = main_window