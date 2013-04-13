'''
Created on Apr 5, 2013

@author: vb
'''
from PyQt4 import QtGui, QtCore

def makeButton(name, icon, func):
    if icon:
        but = QtGui.QPushButton(icon, name)
    else:
        but = QtGui.QPushButton(name)
    but.clicked.connect(func) 
    return but 

def openFolder(parent, path):
    process2 = QtCore.QProcess(parent)
    process2.start('xdg-open "%s"'%path)
    
def tr(str_):
    return QtCore.QObject.tr(QtCore.QObject(), str_)

def getGoodUrl(link):
    urlStr = link.trimmed()
    test = QtCore.QRegExp("^[a-zA-Z]+\\:.*")
    
    # check if it looks like a qualified URL. try parsing it end see
    hasSchema = test.exactMatch(urlStr)
    if hasSchema:
        url = QtCore.QUrl(urlStr, QtCore.QUrl.TolerantMode)
        if url.isValid():
            return url
    
    # Might be a file
    if QtCore.QFile.exists(urlStr):
        return QtCore.QUrl.fromLocalFile(urlStr)
    
    # Might be a shorturl - try to detect the schema
    if not hasSchema:
        dotIndex = urlStr.indexOf('.')
        if dotIndex != 1:
            prefix = urlStr.left(dotIndex).toLower()
            schema = prefix if prefix is "ftp" else "http"
            url = QtCore.QUrl(schema + "://" + urlStr, QtCore.QUrl.TolerantMode)
            if url.isValid():
                return url
        
        return QtCore.QUrl(link, QtCore.QUrl.TolerantMode)  