# -*- coding: utf-8 -*-
'''
Created on 10.01.2012

@author: vb
'''
from PyQt4 import QtCore, QtGui;

class DialogKeyFilter(QtCore.QObject):
    def __init__(self, parent=None):
        QtCore.QObject.__init__(self, parent)
        self.escPress = False
        
    def eventFilter(self, obj, e):
        
        if e.type() == QtCore.QEvent.KeyPress:
            self.escPress = False
            if e.key() == QtCore.Qt.Key_Escape:
                self.escPress = True
                
        return QtCore.QObject.eventFilter(self, obj, e)
    
class TreeDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.CustomizeWindowHint)
        self.resize(400, 50)       
        self.textField = QtGui.QLineEdit()
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.textField)
        self.setLayout(vbox)
        self.dialogKeyFilter = DialogKeyFilter(self.textField)
        self.textField.installEventFilter(self.dialogKeyFilter)
        self.textField.editingFinished.connect(self.onTextChange)       
       
    def onTextChange(self):      
        if not self.dialogKeyFilter.escPress:
            self.done(self.Accepted)
        else:
            self.reject()
    
    def getText(self):
        text = self.textField.text().toUtf8()
        #print unicode(text, 'utf-8')
        #return #unicode(self.textField.text(), 'utf-8')
        return unicode(text, 'utf-8')
    
    def showDialog(self, nodeText):
        self.textField.setText(nodeText)
        self.text = nodeText
        self.exec_()     
