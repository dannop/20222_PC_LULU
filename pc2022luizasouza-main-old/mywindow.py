from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from mycanvas import *
from mymodel import *
class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setGeometry(100,100,600,400)
        self.setWindowTitle("MyGLDrawer")
        self.canvas = MyCanvas()
        self.setCentralWidget(self.canvas)
        # create a model object and pass to canvas
        self.model = MyModel()
        self.canvas.setModel(self.model)
        # create a Toolbar
        tb = self.addToolBar("File")
        fit = QAction(QIcon("icons/fit.png"),"fit",self)
        grade = QAction(QIcon("icons/grade.png"),"grade",self)
        tb.addAction(fit)
        tb.addAction(grade)
        tb.actionTriggered[QAction].connect(self.tbpressed)

    def tbpressed(self,a):
        if a.text() == "fit":
            self.canvas.fitWorldToViewport()
        if a.text() == "grade":
            espacamento, valid = QInputDialog.getInt(self, 'Espaçamento da grade', 'Informe o espaçamento entre os pontos da grade:')
            if valid:
                self.canvas.grid(int(espacamento))