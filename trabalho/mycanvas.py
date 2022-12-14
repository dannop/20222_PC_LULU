import json

from PyQt5 import QtOpenGL
from PyQt5.QtWidgets import *
from OpenGL.GL import *
from PyQt5 import QtCore
from PyQt5.QtCore import *
from he.hecontroller import HeController
from he.hemodel import HeModel
from geometry.segments.line import Line
from geometry.point import Point
from compgeom.tesselation import Tesselation
from compgeom.compgeom import CompGeom


class MyCanvas(QtOpenGL.QGLWidget):
    
    def __init__(self):
        super(MyCanvas, self).__init__()
        self.m_model = None
        self.m_w = 0 # width: GL canvas horizontal size
        self.m_h = 0 # height: GL canvas vertical size
        self.m_L = -1000.0
        self.m_R = 1000.0
        self.m_B = -1000.0
        self.m_T = 1000.0
        self.list = None
        self.m_buttonPressed = False
        self.m_pt0 = QtCore.QPointF(0.0,0.0)
        self.m_pt1 = QtCore.QPointF(0.0,0.0)
        self.m_hmodel = HeModel()
        self.m_controller = HeController(self.m_hmodel)
        self.space = 0
    

    def initializeGL(self):
        #glClearColor(1.0, 1.0, 1.0, 1.0)
        glEnable(GL_DEPTH_TEST)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_LINE_SMOOTH)
        self.list = glGenLists(1)
        
    def resizeGL(self, _width, _height):
        self.m_w = _width
        self.m_h = _height
        if(self.m_model==None)or(self.m_model.isEmpty()): self.scaleWorldWindow(1.0)
        else:
            self.m_L,self.m_R,self.m_B,self.m_T = self.m_model.getBoundBox()
            self.scaleWorldWindow(1.1)
        glViewport(0, 0, self.m_w, self.m_h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(self.m_L,self.m_R,self.m_B,self.m_T,-1.0,1.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glCallList(self.list)
        glDeleteLists(self.list, 1)
        self.list = glGenLists(1)
        glNewList(self.list, GL_COMPILE)
        pt0_U = self.convertPtCoordsToUniverse(self.m_pt0)
        pt1_U = self.convertPtCoordsToUniverse(self.m_pt1)
        glColor3f(1.0, 0.0, 0.0)
        glBegin(GL_LINE_STRIP)
        glVertex2f(pt0_U.x(), pt0_U.y())
        glVertex2f(pt1_U.x(), pt1_U.y())
        glEnd()
        if not((self.m_model == None) and (self.m_model.isEmpty())):
            verts = self.m_model.getVerts()
            glColor3f(0.0, 1.0, 0.0) # green
            glBegin(GL_TRIANGLES)
            for vtx in verts:
                glVertex2f(vtx.getX(), vtx.getY())
            glEnd()
            curves = self.m_model.getCurves()
            glColor3f(0.0, 0.0, 1.0) # blue
            glBegin(GL_LINES)
            for curv in curves:
                glVertex2f(curv.getP1().getX(), curv.getP1().getY())
                glVertex2f(curv.getP2().getX(), curv.getP2().getY())
            glEnd()
        glEndList()
        if not(self.m_hmodel.isEmpty()):
            patches = self.m_hmodel.getPatches()
            for pat in patches:
                pts = pat.getPoints()
                triangs = Tesselation.tessellate(pts)
                for j in range(0, len(triangs)):
                    glColor3f(1.0,0.0,1.0)
                    glBegin(GL_TRIANGLES)
                    glVertex2d(pts[triangs[j][0]].getX(),pts[triangs[j][0]].getY())
                    glVertex2d(pts[triangs[j][1]].getX(),pts[triangs[j][1]].getY())
                    glVertex2d(pts[triangs[j][2]].getX(),pts[triangs[j][2]].getY())
                    glEnd()
                segments = self.m_hmodel.getSegments()
                for curv in segments:
                    ptc = curv.getPointsToDraw()
                    glColor3f(0.0,1.0,1.0)
                    glBegin(GL_LINES)
                    for curv in curves:
                        glVertex2f(ptc[0].getX(), ptc[0].getY())
                        glVertex2f(ptc[1].getX(), ptc[1].getY())
                    glEnd()


    def setModel(self,_model):
        self.m_model = _model

    def fitWorldToViewport(self):
        print("fitWorldToViewport")
        if self.m_model == None:
            return
        self.m_L,self.m_R,self.m_B,self.m_T=self.m_model.getBoundBox()
        self.scaleWorldWindow(1.10)
        self.update()
        self.pointGrid(self.space)

    def scaleWorldWindow(self,_scaleFac):
        vpr = self.m_h / self.m_w
        cx = (self.m_L + self.m_R) / 2.0
        cy = (self.m_B + self.m_T) / 2.0
        sizex = (self.m_R - self.m_L) * _scaleFac
        sizey = (self.m_T - self.m_B) * _scaleFac
        if sizey > (vpr*sizex):
            sizex = sizey / vpr
        else:
            sizey = sizex * vpr
        self.m_L = cx - (sizex * 0.5)
        self.m_R = cx + (sizex * 0.5)
        self.m_B = cy - (sizey * 0.5)
        self.m_T = cy + (sizey * 0.5)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(self.m_L, self.m_R, self.m_B, self.m_T, -1.0, 1.0)

    def panWorldWindow(self, _panFacX, _panFacY):
        panX = (self.m_R - self.m_L) * _panFacX
        panY = (self.m_T - self.m_B) * _panFacY
        self.m_L += panX
        self.m_R += panX
        self.m_B += panY
        self.m_T += panY
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(self.m_L, self.m_R, self.m_B, self.m_T, -1.0, 1.0)

    def convertPtCoordsToUniverse(self, _pt):
        dX = self.m_R - self.m_L
        dY = self.m_T - self.m_B
        mX = _pt.x() * dX / self.m_w
        mY = (self.m_h - _pt.y()) * dY / self.m_h
        x = self.m_L + mX
        y = self.m_B + mY
        return QtCore.QPointF(x,y)

    def mousePressEvent(self, event):
        self.m_buttonPressed = True
        self.m_pt0 = event.pos()

    def mouseMoveEvent(self, event):
        if self.m_buttonPressed:
            self.m_pt1 = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        pt0_U = self.convertPtCoordsToUniverse(self.m_pt0)
        pt1_U = self.convertPtCoordsToUniverse(self.m_pt1)
        self.m_model.setCurve(pt0_U.x(),pt0_U.y(),pt1_U.x(),pt1_U.y())
        #self.m_model.setCurve(self.m_pt0.x(),...,...,...)
        self.m_buttonPressed = False
        self.m_pt0.setX(0.0)
        self.m_pt0.setY(0.0)
        self.m_pt1.setX(0.0)
        self.m_pt1.setY(0.0)
        p0 = Point(pt0_U.x(), pt0_U.y())
        p1 = Point(pt1_U.x(), pt1_U.y())
        segment = Line(p0,p1)
        self.m_controller.insertSegment(segment, 0.01)
        self.update()
        self.repaint()
        self.pointGrid(self.space)

    def pointGrid(self, space):
        self.space = space
        if self.space > 0:
            xmax = self.m_hmodel.getBoundBox()[1]
            xmin = self.m_hmodel.getBoundBox()[0]
            x_quant = int((xmax - xmin) / self.space)
            ymax = self.m_hmodel.getBoundBox()[3]
            ymin = self.m_hmodel.getBoundBox()[2]
            y_quant = int((ymax - ymin) / self.space)
            glNewList(self.list, GL_COMPILE)
            points_list = {"points": [] }
            for i in range(x_quant):
                for j in range(y_quant):
                    posx = xmin + self.space*i
                    posy = ymin + self.space*j
                    point = Point(posx, posy)
                    if CompGeom.isPointInPolygon(self.m_hmodel.getPoints(), point):
                        glColor4f(1.0, 1.0, 1.0, 1.0)
                        glPointSize(4)
                        glBegin(GL_POINTS)
                        glVertex2f(point.getX(), point.getY())
                        glEnd()
                        points_list["points"].append([point.getX(), point.getY()])
            glEndList()

            json_object = json.dumps(points_list)
            with open("points_list.json", "w") as outfile:
                outfile.write(json_object)