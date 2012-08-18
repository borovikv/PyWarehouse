# -*- coding: utf-8 -*-
'''
Created on Jul 11, 2012

@author: vb
'''
from PyQt4 import QtGui, QtCore
#from Utils.Strings import TStrings 
from Utils.Strings import getTranslate as __
from Dialogs.Messages import Messages

class PreferencesDialog(QtGui.QDialog):
    def __init__(self, preferences, parent=None):
        #DialogBox.__init__(self, 500, 400, "#aaa", parent)
        QtGui.QDialog.__init__(self, parent)
        self.preferences = preferences
        self.messages = Messages()
        self.xmlPathEdit = QtGui.QLineEdit()
        buttonBrowse = QtGui.QPushButton(__("browse"))
        buttonBrowse.clicked.connect(self.browse)
        hboxBrowse = QtGui.QHBoxLayout()
        hboxBrowse.addWidget(self.xmlPathEdit)
        hboxBrowse.addWidget(buttonBrowse)        
        
        buttonOk = QtGui.QPushButton("OK")
        buttonCancel = QtGui.QPushButton("Cancel")
        buttonOk.clicked.connect(self.ok)
        buttonCancel.clicked.connect(self.cancel)
        
        hboxOK_Cancel = QtGui.QHBoxLayout()
        hboxOK_Cancel.insertStretch(-1)
        hboxOK_Cancel.addWidget(buttonOk)
        hboxOK_Cancel.addWidget(buttonCancel)
        hboxOK_Cancel.insertStretch(-1)
        
        
        form = QtGui.QFormLayout()
        form.addRow(__("WarehouseXML"), hboxBrowse)
        form.addRow(hboxOK_Cancel)
        vbox = QtGui.QVBoxLayout()
        vbox.insertStretch(-1)
        vbox.addLayout(form)
        vbox.insertStretch(-1)
        self.setLayout(vbox)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.resize(600, 400)
    
    def browse(self):
        filters = self.tr("XML (*.xml);;")
        filters += self.tr("All Files (*)")
        curPath = self.xmlPathEdit.text()
        xml = unicode(QtGui.QFileDialog.getOpenFileNameAndFilter(None, QtCore.QString(), filter=filters)[0], 'utf-8')
        if xml and xml == curPath:
            return
        elif xml and xml != curPath:
            self.xmlPathEdit.setText(xml)
        return xml
    
    def ok(self):
        path = self.xmlPathEdit.text()
        if not path:
            self.messages.showDialog(self.messages.chooseRoot)
        else:
            self.hide()
            self.xmlPath = path
            self.preferences.update()
    
    def cancel(self):
        if not self.xmlPath:
            self.messages.showDialog(self.messages.chooseRoot)
        else:
            self.xmlPathEdit.setText(self.xmlPath)
            self.hide()
            
    def show_prep(self):
        self.xmlPath = self.preferences.getXmlPath()
        self.xmlPathEdit.setText(self.xmlPath)
        
    
        
if __name__ == "__main__":
    import sys
    from Utils import Preferences
    app = QtGui.QApplication(sys.argv)
    d = PreferencesDialog(Preferences.Preferences(lambda:5+1))
    d.show()
    sys.exit(app.exec_())