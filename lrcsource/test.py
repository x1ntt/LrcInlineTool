import sourcebase
import sourcenetease
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow

class T:
    def resultList(self, e, l):
        print ("==========")
        print (e)
        for u in l:
            print (u.print())

def main():
    app = QApplication(sys.argv)    
    sr = sourcebase.SearchRequest("红", "")
    ns = sourcenetease.NeteaseSource()
    t = T()
    ns.SetCallbackObject(t)
    ns.getResultList(sr)
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()