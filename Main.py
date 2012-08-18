'''
Created on 22.02.2012

@author: vb
'''


if __name__ == "__main__":
    import sys

    from MainFrame.Warehouse import Warehouse
    from PyQt4 import QtGui
    
    app = QtGui.QApplication(sys.argv)

    warehouse = Warehouse()
    
    sys.exit(app.exec_())
