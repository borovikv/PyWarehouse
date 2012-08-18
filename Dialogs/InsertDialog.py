'''
Created on Jul 15, 2012

@author: vb
'''
from PyQt4 import QtGui, QtCore
from Utils.Strings import getTranslate as __
from Dialogs.Dialog import DialogBox

class InsertDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.path = None
        self.pathLine = QtGui.QLineEdit()
        buttonBrowse = QtGui.QPushButton(__("browse"))
        buttonBrowse.clicked.connect(self.browse)
        hboxBrowse = QtGui.QHBoxLayout()
        hboxBrowse.addWidget(self.pathLine)
        hboxBrowse.addWidget(buttonBrowse)        
        
        buttonOk = QtGui.QPushButton("OK")
        buttonOk.clicked.connect(self.ok)
        
        hboxOK_Cancel = QtGui.QHBoxLayout()
        hboxOK_Cancel.insertStretch(-1)
        hboxOK_Cancel.addWidget(buttonOk)
        hboxOK_Cancel.insertStretch(-1)
        
        
        form = QtGui.QFormLayout()
        form.addRow(hboxBrowse)
        form.addRow(hboxOK_Cancel)
        vbox = QtGui.QVBoxLayout()
        vbox.insertStretch(-1)
        vbox.addLayout(form)
        vbox.insertStretch(-1)
        self.setLayout(vbox)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.resize(600,400)
    
    def browse(self):
        f = unicode(QtGui.QFileDialog.getOpenFileNameAndFilter(None, QtCore.QString())[0], "utf-8")
        if f:
            self.pathLine.setText(f)
    
    def ok(self):
        self.path = unicode(self.pathLine.text(), 'utf-8')
        self.hide()
        
    def show(self, *args, **kwargs):
        self.path = ""
        return DialogBox.show(self, *args, **kwargs)

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    d = InsertDialog()
    d.show()
    sys.exit(app.exec_())