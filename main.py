import sys
from ui.main_ui import Ui_MainWindow
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setAcceptDrops(True)
        
        self.OpenFile_Btn.clicked.connect(self.musicList.addMusic)
        self.Remove_Btn.clicked.connect(self.musicList.removeMusic)
        self.Save_Btn.clicked.connect(self.musicList.saveInfo)
        self.SearchLRC_Btn.clicked.connect(self.LrcList_Tw.searchLrc)
        
        self.Log_Lw.SetMainWindow(self)
        self.musicList.SetMainWindow(self)
        self.LrcList_Tw.SetMainWindow(self)
        
        self.LrcList_Tw.addSource()
        
        self.show()
        
    # 事件处理函数 ↓
    def dragEnterEvent(self, e):
        # print(e)
        e.accept()
        
    def dropEvent(self, e):
        #print(e)
        pass
    
def main():
    app = QApplication(sys.argv)
    
    main_ui = MainWindow()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()