'''
Created on 21.02.2012

@author: vb
'''
from PyQt4 import  QtGui, QtWebKit
from PyQt4.QtCore import Qt, QEvent, QObject

class EditorFilter(QObject):
    def __init__(self, parent=None):
        QObject.__init__(self, parent)
        
        self.arrowKeys = { 
                          Qt.Key_Up: "ARROWUP", 
                          Qt.Key_Down: "ARROWDOWN", 
                          }
        
        self.shortCuts = {
                        Qt.Key_Left:"column after",
                        Qt.Key_Right:"column before",
                        Qt.Key_Up:"row after",
                        Qt.Key_Down:"row before",
                        Qt.Key_Delete:"delete column",
                        Qt.Key_Backspace:"delete row",
                        Qt.Key_2:"insert tag",
                        Qt.Key_3:"insert task",
                        Qt.Key_8:"unorderer list",
                        Qt.Key_9:"orderer list",
                        Qt.Key_B:"bold",
                        Qt.Key_I:"italic",
                        Qt.Key_U:"underline",
                        Qt.Key_Q:"insert object",
                        Qt.Key_T:"insert table",
                        Qt.Key_H:"highlight",
                        Qt.Key_R:"remove format",
                        Qt.Key_Underscore:"horizontal rule",
                        Qt.Key_F: "find or replace",
                        }
        
    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress:
            return self.keyPressed(obj, event)
        return QObject.eventFilter(self, obj, event)

    def keyPressed(self, obj, event):
        if self.isShortCutEvent(event):
            return self.execute(obj, event)
        
        if self.isPasteEvent(event):
            return self.execute(obj, 'onPaste')
        elif self.isCopyEvent(event):
            return self.execute(obj, 'onCopy')
        elif self.isArrowEvent(event):
            return self.execute(obj, 'onArrow', self.arrowKeys[event.key()])
        elif event.key() == Qt.Key_Backtab:
            return self.execute(obj, 'onOutdent')
        elif event.key()  == Qt.Key_Tab:
            return self.execute(obj, 'onIndent')
        elif event.key() in ( Qt.Key_Enter, Qt.Key_Return, ):
            print 'ent'
            return self.execute(obj, 'onEnter')
        elif not ( event.key() in ( Qt.Key_Left, Qt.Key_Right, ) ): 
            return self.execute(obj, 'onKeyPress')
        
        return QObject.eventFilter(self, obj, event)

    
    def isShortCutEvent(self, event):
        return self.ctrlPressed(event) and event.key() in self.shortCuts

    def isCopyEvent(self, event):
        return event.matches(QtGui.QKeySequence.Copy) or event.matches(QtGui.QKeySequence.Cut)

    def isPasteEvent(self, event):
        return event.matches(QtGui.QKeySequence.Paste)
    
    def isArrowEvent(self, event):
        return event.key() in self.arrowKeys

    def ctrlPressed(self, event):
        return event.modifiers() & Qt.ControlModifier
    
    def shiftPressed(self, event):
        return event.modifiers() & Qt.ShiftModifier

    def execute(self, obj, event, *args):
        if isinstance(event, basestring):
            return obj.execute(event, *args)
        else:
            action = self.shortCuts[event.key()]
            return obj.execute(action)





