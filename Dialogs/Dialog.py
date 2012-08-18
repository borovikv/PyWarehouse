'''
Created on 07.07.2012

@author: vb
'''
from PyQt4 import QtCore, QtGui

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
        
