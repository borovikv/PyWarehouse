'''
Created on 21.02.2012

@author: vb
'''
from PyQt4 import QtGui

class Messages:
    def __init__(self):
        self.chooseNew = "file not set or not exists. choose new file"
        self.chooseRoot = "The root file is not selected"
        
    def showDialog(self, text):
        message = QtGui.QMessageBox()
        message.setText(text)
        message.exec_()
