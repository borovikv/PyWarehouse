'''
Created on 07.07.2012

@author: vb
'''
from PyQt4 import QtCore, QtGui
from Utils.QUtils import makeButton

class DialogBox(QtGui.QWidget):
    def __init__(self, width, height, color, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.color = color
        self.resize(width, height)
        self.setWindowFlags(QtCore.Qt.Window | 
                            QtCore.Qt.FramelessWindowHint | 
                            QtCore.Qt.CustomizeWindowHint | 
                            QtCore.Qt.Dialog)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowOpacity(0.95)
        centrX, centrY = self.getCenter(width, height)
        self.move(centrX, centrY)
    

    def getCenter(self, width, height):
        desktop = QtGui.QApplication.desktop()
        centrX, centrY = (desktop.width() - width) / 2, (desktop.height() - height) / 2
        return centrX, centrY

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        color = QtGui.QColor(self.color)
        painter.setPen(color)
        painter.setBrush(QtGui.QBrush(color))
        
        width, height = float(self.width()), float(self.height())
        dialogRectangle = QtCore.QRectF(0.0, 0.0, width, height)
        xRound, yRound = 7.5 , 15
        painter.drawRoundRect(dialogRectangle, xRound, yRound)

class LineDialog(DialogBox):

    def __init__(self, lines, buttons, parent=None):
        super(LineDialog, self).__init__(600, 300, "#aaa", parent)
        vbox = QtGui.QVBoxLayout()
        
        self.makeLines(lines)
        self.addLinesToLayout(vbox)
        
        self.makeButtons(buttons)
        hbox = QtGui.QHBoxLayout()
        self.addButtonsToLayout(hbox)
        vbox.addLayout(hbox)
        
        self.setLayout(vbox)
    
    def makeLines(self, lines):
        self.lines = []
        for _ in range(lines):
            self.lines.append(QtGui.QLineEdit())

    def addLinesToLayout(self, layout):
        for line in self.lines:
            layout.addWidget(line)

    def makeButtons(self, buttons):
        self.buttons = {}
        for name, (text, listener) in buttons.items():
            self.makeButton(name, text, listener)
    
    def makeButton(self, name, text, listener):
        return self.buttons.setdefault(name, makeButton(text, func=listener))

    def addButtonsToLayout(self, layout):
        for name in sorted(self.buttons):
            layout.addWidget(self.buttons[name])
                            
    def addCloseButton(self, vbox):
        closeBut = makeButton("close", func=self.hide)
        hbox = QtGui.QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(closeBut)
        vbox.addLayout(hbox)

        
    def getLineText(self, position):
        if position < len(self.lines):
            return self.lines[position].text()
    
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.hide()
        return DialogBox.keyPressEvent(self, event)
    
class FindReplaceDialog(LineDialog):
    def __init__(self, parent):
        buttons = {
           'find':('find', parent.findNext),
           'find_all':('find all', parent.findAll), 
           'replace': ('replace first', parent.replaceNext),
           'replace_all': ('replace all', parent.replaceAll),
        }
        LineDialog.__init__(self, 2, buttons=buttons, parent=parent)  
    
    def textToFind(self):
        return self.getLineText(0)
    
    def textToReplace(self):
        self.getLineText(1)
    
    def setTextToFind(self):   
        selectedText = self.parent().selectedText()
        findLine = self.lines[0]
        findLine.setText(selectedText)
        findLine.setSelection(0, len(selectedText))
        
    def show(self):
        self.setTextToFind()
        return LineDialog.show(self)
          
if __name__=="__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    d = LineDialog(2, {'a':('aa', lambda: 'a'), 'b': ('bb', lambda: 'b') })    
    d.show()
    sys.exit(app.exec_())
        
