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

class LineDialog(DialogBox):

    def __init__(self, lines, buttons, parent=None):
        super(LineDialog, self).__init__(600, 300, "#aaa", parent)
        vbox = QtGui.QVBoxLayout()
        
        self.makeLines(lines)
        self.addLinesToLayout(vbox)
        
        self.makeButtons(buttons)
        hbox = QtGui.QHBoxLayout()
        self.addButtonsToLayout(hbox, ('close',))
        vbox.addLayout(hbox)
                
        self.addCloseButton(vbox)
        
        self.setLayout(vbox)
    
    def makeLines(self, lines):
        self.lines = []
        for _ in range(lines):
            self.lines.append(QtGui.QLineEdit(str(_)))

    def addLinesToLayout(self, layout):
        for line in self.lines:
            layout.addWidget(line)

    def makeButtons(self, buttons):
        self.buttons = {}
        self.makeButton("close", "close", self.hide)
        for name, (text, listener) in buttons.items():
            self.makeButton(name, text, listener)
    
    def makeButton(self, name, text, listener):
        return self.buttons.setdefault(name, makeButton(text, func=listener))

    def addButtonsToLayout(self, layout, exclude):
        for name in sorted(self.buttons):
            if exclude and name in exclude:
                continue
            layout.addWidget(self.buttons[name])
                            
    def addCloseButton(self, vbox):
        hbox = QtGui.QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(self.buttons.get('close'))
        vbox.addLayout(hbox)

        
    def getLineText(self, position):
        if position < len(self.lines):
            return self.lines[position].text()
    
class FindReplaceDialog(LineDialog):
    def __init__(self, parent):
        buttons = {
           'find':('find', parent.findNext),
           'find_all':('find all', parent.findAll), 
           'replace': ('replace', parent.replaceNext),
           'replace_all': ('replace all', parent.replaceAll),
        }
        LineDialog.__init__(self, 2, buttons=buttons, parent=parent)  
          
if __name__=="__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    d = LineDialog(2, {'a':('aa', lambda: 'a'), 'b': ('bb', lambda: 'b') })    
    d.show()
    sys.exit(app.exec_())
        
