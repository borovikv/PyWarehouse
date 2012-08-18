
        
if __name__ == "__main__":
    import sys 
    from EditorPanel.Editor import Editor
    from PyQt4 import QtGui, QtCore
    
    def addButton(name, functionName, hbox):
        but = QtGui.QPushButton(name)
        but.clicked.connect(functionName)
        hbox.addWidget(but)
        return but
    
        
    app = QtGui.QApplication(sys.argv)
    editor = Editor()
    path = "/media/share/home/Temp/1.html"
    editor.setWindowFilePath(path)
    editor.openDoc(path)
    def stUrl():
        editor.setUrl(QtCore.QUrl("www.google.com"))
    
    def so():   
        editor.saveDoc();
        editor.openDoc(path)
    def opn():
        p = QtGui.QFileDialog.getOpenFileName(None, "")
        editor.openDoc(p)

    editor.newDoc()
    editor.setPath(path)
    hbox = QtGui.QHBoxLayout()
    
    
    svB = addButton("save", so, hbox)
    imgB = addButton("img", editor.insertImg, hbox)
    linkB = addButton("link", editor.createLink, hbox)
    rel = addButton("reload", editor.reload, hbox)
    op = addButton("open", opn, hbox)
    stur = addButton("url", stUrl, hbox)
    hbox.addWidget(editor.zoomSlider)
        
    
    gbox = QtGui.QGridLayout()
    gbox.addWidget(editor, 0, 0)
    gbox.addLayout(hbox, 1, 0)
   
    window = QtGui.QWidget()
    window.setWindowTitle("editor")
    window.setLayout(gbox)
    window.showMaximized()

    sys.exit(app.exec_())
