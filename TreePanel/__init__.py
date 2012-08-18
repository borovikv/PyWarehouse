


if __name__ == "__main__":
    import sys
    import os
    from PyQt4 import QtCore, QtGui
    from TreePanel.DOMTreeWidget import DOMTreeWidget
    
    class xmlName:
        def __init__(self):
            self.attributeName = "path"
            self.tagName = "Thought"
            self.rootName = "Warehouse"
            self.splitChar = "@"
    
    p = os.path.realpath(os.getcwd())
    s = os.path.split(p)    
    app = QtGui.QApplication(sys.argv)
    xmlFile = s[0] + "/Warehouse/Warehouse.xml"
    acctions = {}
    def foo(x):
        print(x)
    acctions["addChild"] = foo
    acctions["renameNode"] = foo
    acctions["itemClick"] = foo
    window = DOMTreeWidget(xmlFile, xmlName(), acctions)
    window.resize(500, 500)
    window.move(0, 0)
    window.show()
    sys.exit(app.exec_())
