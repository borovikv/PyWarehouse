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
                        }
        
    def eventFilter(self, obj, e):
        if e.type() == QEvent.KeyPress  and e.modifiers()& Qt.ControlModifier and e.key() in self.actions:
            action = self.actions.get(e.key())
            obj.execute(action)
            if e.key() not in self.keyCodes:
                return True
            return QObject.eventFilter(self, obj, e)
        
        if e.type() == QEvent.KeyPress:
            if e.matches(QtGui.QKeySequence.Paste):
                obj.pastePreparation()
            elif e.matches(QtGui.QKeySequence.Copy) or e.matches(QtGui.QKeySequence.Cut):
                obj.setUrlForCopy()
               
        return QObject.eventFilter(self, obj, e)
