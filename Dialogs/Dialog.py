'''
Created on 07.07.2012

@author: vb
'''
from PyQt4 import QtCore, QtGui
from Utils.Strings import getTranslate
from Utils.QUtils import makeButton

class DialogBox(QtGui.QWidget):
    def __init__(self, width, height, color, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.color = color
        self.resize(width, height)
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowOpacity(0.95)
        desktop = QtGui.QApplication.desktop()
        centrX, centrY = (desktop.width() - width) / 2, (desktop.height() - height) / 2
        self.move(centrX, centrY)
    
    def paintEvent(self, event):
        width, height = self.width(), self.height()
        xRound, yRound = 7.5 , 15
        painter = QtGui.QPainter(self)
        qColor = QtGui.QColor(self.color)
        painter.setPen(qColor)
        painter.setBrush(QtGui.QBrush(qColor))
        painter.drawRoundRect(QtCore.QRectF(0.0, 0.0, float(width), float(height)), xRound, yRound)

class DualLineDialog(DialogBox):
    def __init__(self, parent = None):
        super(DualLineDialog, self).__init__(600, 300, "#aaa", parent)
        vbox = QtGui.QVBoxLayout()
        self.first_line = QtGui.QLineEdit()
        self.second_line = QtGui.QLineEdit()
        close_button =makeButton("close", None, self.hide)
        find_button =makeButton("find", None, self.hide)
        find_all_button =makeButton("find all", None, self.hide)
        replace_button =makeButton("replace", None, self.hide)
        replace_all_button =makeButton("replace all", None, self.hide)
        hbox = QtGui.QHBoxLayout
        vbox.addWidget(self.first_line)
        vbox.addWidget(self.second_line)
        
        vbox.addWidget(close_button)
        self.setLayout(vbox)
        
    def getFirstLineText(self):
        return self.first_line.text()
    def getSecondLineText(self):
        return self.second_line.text()
    
if __name__=="__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    d = DialogBox(600, 300, "#aaa")
    vbox = QtGui.QVBoxLayout()
    textField = QtGui.QLineEdit()
    vbox.addWidget(textField)
    d.setLayout(vbox)
    
    d.show()
    sys.exit(app.exec_())
        
