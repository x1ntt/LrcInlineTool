import sourcebase
import sourcenetease
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow


def main():
    app = QApplication(sys.argv)    
    sr = sourcebase.SearchRequest("声")
    ns = sourcenetease.NeteaseSource()
    ns.handleRequest(sr)
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()