'''
Created on 21.02.2012

@author: vb
'''
from PyQt4 import  QtGui
from PyQt4.QtCore import Qt, QEvent, QObject

class EditorFilter(QObject):
    def __init__(self, parent=None):
        QObject.__init__(self, parent)
        
        self.keyCodes = { Qt.Key_Left: "ARROWLEFT", 
                          Qt.Key_Right: "ARROWRIGHT", 
                          Qt.Key_Up: "ARROWUP", 
                          Qt.Key_Down: "ARROWDOWN", 
                          Qt.Key_Enter: "ENTER", 
                          Qt.Key_Delete: "DELETE", 
                          Qt.Key_Insert: "INSERT"}
        
        self.actions = {
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
        if self.isCtrlActionEvent(event):
            return self.execute(obj, event)
        
        if self.isPasteEvent(event):
            obj.pastePreparation()
        
        elif self.isCopyEvent(event):
            obj.setUrlForCopy()
        
        elif self.isArrowEvent(event):
            key = self.keyCodes[event.key()]
            obj.onArrow(key)
        return QObject.eventFilter(self, obj, event)

    
    def isCtrlActionEvent(self, event):
        return self.ctrlPressed(event) and event.key() in self.actions

    def isCopyEvent(self, event):
        return event.matches(QtGui.QKeySequence.Copy) or event.matches(QtGui.QKeySequence.Cut)


    def isPasteEvent(self, event):
        return event.matches(QtGui.QKeySequence.Paste)
    
    def isArrowEvent(self, event):
        key = self.keyCodes.get(event.key()) 
        return key and key in ("ARROWUP", "ARROWDOWN")

    def execute(self, obj, event):
        action = self.actions[event.key()]
        obj.execute(action)
        if event.key() not in self.keyCodes:
            return True
        return QObject.eventFilter(self, obj, event)


    def ctrlPressed(self, event):
        return event.modifiers() & Qt.ControlModifier





