import sys
from mywindow import *

def main():
    QApplication.setAttribute(QtCore.Qt.AA_UseDesktopOpenGL)
    app = QApplication(sys.argv)
    gui = MyWindow()
    gui.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()