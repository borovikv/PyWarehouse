# -*- coding: utf-8 -*-
'''
Created on 21.02.2012

@author: vb
'''

from PyQt4 import QtCore, QtGui, QtWebKit
from PyQt4.QtWebKit import QWebPage, QWebView
import os
from os.path import join
import shutil
import locale
from EditorPanel.EditorFilter import EditorFilter
from Utils.Events import ObservableEvent
from Dialogs.InsertDialog import InsertDialog
from Utils import QUtils
from Utils.utils import copy_imgs, delete_files,\
    make_dir_if_not_exist, copy_file, copy_file, copy_folder, is_image, get_name
from PyQt4.QtCore import QString as _qstr
from Dialogs.Dialog import FindReplaceDialog
import re
import inspect
import codecs
locale.setlocale(locale.LC_ALL, '')

EDITOR_FOLDER = os.path.dirname(__file__)        
TEMPLATES = join(EDITOR_FOLDER, 'templates')
SOURCE = '_source'
SOURCE_FOLDER  = join(EDITOR_FOLDER, SOURCE)
JS_FOLDER = join(EDITOR_FOLDER, 'JScripts')

class Editor(QWebView):
    FILES_FOLDER = "Files" 
    IMG_FOLDER = "IMG"
    SELF = ""
    
    def __init__(self, notesFolder, parent = None):
        QWebView.__init__(self, parent)
        self.insertDialog = InsertDialog(self)
        self.findReplaceDialog = FindReplaceDialog(self)
        self.notesFolder = notesFolder
        self.urlForCopy = None
        self.path = None
        self.makeHeaders()
        self.copySourceFilesToNotesFolder()
        self.installEventFilter(EditorFilter(self))      
        self.createActions()
     
    def makeHeaders(self):
        self.context =  { 'scriptFolderPath': JS_FOLDER, }
        f = file(join(TEMPLATES, 'header.html'))
        header = unicode(f.read())
        f.close()
        self.extendedHeader = header%self.context
        
        f = file(join(TEMPLATES, 'default_header.html'))
        self.defaultHeader = unicode(f.read())
        f.close()
    
    def copySourceFilesToNotesFolder(self):
        dest = join(self.notesFolder, os.path.basename(SOURCE_FOLDER))
        copy_folder(SOURCE_FOLDER, dest)
    
    
    def getAction(self, name):
        return self.editor_actions.get(name)
    
    def getActions(self):
        return self.editor_actions.keys()
    
    def createActions(self):
        self.events = {
           'onArrow': self.onArrow,
           'onEnter': lambda: self.callJS('onEnter'),
           'onOutdent': lambda: self.triggerPageAction(QtWebKit.QWebPage.Outdent),
           'onIndent': lambda: self.triggerPageAction(QtWebKit.QWebPage.Indent),
           'onPaste': self.pastePreparation,
           'onKeyPress': lambda: self.callJS('onKeyPressed'),
        }
        self.editor_actions = {
            "column after": 'onInsertColAfter', 
            "column before": 'onInsertColBefore', 
            "row after": 'onInsertRowAfter', 
            "row before": 'onInsertRowBefore', 
            "delete column": 'onDeleteCol', 
            "delete row": 'onDeleteRow', 
            "bold": 'onBold', 
            "underline": 'onUnderline', 
            "italic": 'onItalic', 
            "orderer list": 'onOList', 
            "unorderer list": 'onUList', 
            "highlight": 'onHighlight', 
            "horizontal rule": 'insertHorizontalRule', 
            "remove format": 'onRemoveFormat', 
            "insert task": 'onTask', 
            "delete task": 'onDeleteTask', 
            "insert table": self.onCreateTable, 
            "show in folder": self.showInFolder,
            "find or replace": self.findReplace,
            "insert object": self.onInsert,
        }    

    def onCreateTable(self, row_col):
        row_col = self.getRowCol(row_col)
        self.jsTrigger('onCreateTable', *row_col)        

    def getRowCol(self, row_col):
        if row_col:
            row_col = [x for x in re.split(r'[^\d]+', row_col) if x.isdigit()]
            if len(row_col) == 0:
                row_col = [1, 1]
            elif len(row_col) == 1:
                row_col.append(1)
            else:
                row_col = row_col[:2]
        else:
            row_col = [1, 1]
        return row_col
    
    def showInFolder(self):
        if self.path:
            QUtils.openFolder(self, self.getPathToFolder(Editor.SELF))
    
    def findReplace(self):
        self.findReplaceDialog.show()
    
    def findNext(self):
        text = self.getText()
        self.findText(text)
    
    def findAll(self):
        text = self.getText()
        self.findText(text, QWebPage.HighlightAllOccurrences)

    def replaceNext(self):
        self.replace('first')
    
    def replaceAll(self):
        self.replace('all')

    def replace(self, what):
        text = self.getText()
        newtext = self.findReplaceDialog.textToReplace()  
        self.jsTrigger('replace', what, text, newtext)
    
    def getText(self):     
        text = self.findReplaceDialog.textToFind()  
        if not text:
            text = self.selectedText()
        return text
      
    def onInsert(self):
        self.insertDialog.exec_()
        path = self.insertDialog.path
        if not path: return
        
        if is_image(path):
            f = self.copyImage(path)
            self.execCommand("insertImage", f)
        elif os.path.isfile(path):    
            f = self.copyFile(path)
            self.insertLinkToFile(f['url'], f['name'])
        else:
            self.execCommand("createLink", path);

    def insertLinkToFile(self, url, text):
        icon = join('..', SOURCE, "File.png")
        htmlText = "&nbsp;<div class='File'><a href='%s'><img src='%s'>%s</a></div>&nbsp" % (url, icon, text)
        self.execCommand("insertHTML", htmlText)

    def copyImage(self, path):
        return copy_file(path, self.getPathToFolder(Editor.IMG_FOLDER))

    def copyFile(self, link):        
        link = _qstr(link)
        if link.isEmpty():
            return
        url = QUtils.getGoodUrl(link)
        if url.isValid():
            dst = self.getPathToFolder(Editor.FILES_FOLDER)
            make_dir_if_not_exist(dst) 
            url = copy_file(unicode(url.toString(), 'utf-8')[7:], dst)
            
            return {"url":url, "name": get_name(url)}

    def openLink(self, url):
        QtGui.QDesktopServices.openUrl(url)
        return True
    
    def onArrow(self, key):
        return self.callJS('onArrow', key)
        
    ############################################################################
    #
    # Paste IMG 
    #
    ############################################################################  
    def pastePreparation(self):
        clipboard = QtGui.QApplication.clipboard() 
        text = clipboard.text("html")
        if not text: 
            return        
        dest = self.getPathToFolder(Editor.IMG_FOLDER)
        text = copy_imgs(text, dest, os.path.dirname(self.path))
        data = QtCore.QMimeData()
        data.setHtml(text)
        clipboard.setMimeData(data)

    #---------------------------------------------------------------------------

    def openDoc(self, path):
        content = self.getHtmlStringFromFile(path)
        self.setHtml(content, QtCore.QUrl.fromLocalFile(path))
        self.page().setLinkDelegationPolicy(QWebPage.DelegateAllLinks)
        self.linkClicked[QtCore.QUrl].connect(self.openLink)
        self.setFocus()
        self.path  = path
    
    def saveDoc(self, path=None):
        path = self.getPath(path)
        if not path: return
        
        with codecs.open(path, 'w', 'utf-8') as f:
            html = self.getHtml()
            f.write(html)
    
    def rename(self, oldPath, newPath):
        self.saveDoc()
        src = os.path.dirname(oldPath)
        dst = os.path.dirname(newPath)
        shutil.move(src, dst)
        fileName = os.path.basename(oldPath)
        os.rename(join(dst, fileName), newPath)
        self.path = newPath
        
    def deleteDoc(self, path):
        shutil.rmtree(path)
        self.path = None
    
    def getHtmlStringFromFile(self, path):
        if not os.path.exists(path): 
            path = join(TEMPLATES, "sources.html")
        with codecs.open(path, 'r', 'utf-8') as f:
            template = unicode(f.read())
            template = self.insertHeader(template, self.extendedHeader)
            return template

    def insertHeader(self, html, head):
        return re.sub(r'<head>([\s\S]*)</head>', head, html)
        
    def getPath(self, path=None):
        if not path and hasattr(self, "path"): 
            path = self.path
        return path

    def getHtml(self):
        html = unicode(self.page().mainFrame().toHtml())
        return self.insertHeader(html, self.defaultHeader)

    ############################################################################
    #
    # Events
    #
    ############################################################################
    def  execute(self, cmd, *args):
        action = self.editor_actions.get(cmd) or self.events.get(cmd)
        if not action: 
            return False 
        if isinstance(action, basestring):
            self.jsTrigger(action, *args)
        else:
            return  self.callFunc(action, *args) or False
        return False
            
    def callFunc(self, action, *args):
        argSpec = inspect.getargspec(action)
        
        if len(argSpec.args)>1 or  argSpec.varargs:
            return action(*args[:len(argSpec.args)])
        else:
            return action()

    # Observe
    def update(self, event):
        if event.type == ObservableEvent.start:
            self.on_start(event)
        
        if event.type == ObservableEvent.close:
            self.on_close()
        
        if event.type is ObservableEvent.execute:
            self.execute(event.getParam('command'), event.getParam('params'))

    def on_start(self, event):
        pass

    def on_close(self):
        if hasattr(self, 'path') and self.path:
            self.saveDoc()
            self.delete_unnecessary()

    def delete_unnecessary(self):
        self.delete_unnecessary_img()
        self.delete_unnecessary_files()
    
    def delete_unnecessary_img(self):
        self.__delete_unnecessary('src', 'img', Editor.IMG_FOLDER)

    def delete_unnecessary_files(self):
        self.__delete_unnecessary('href', 'div.File>a', Editor.FILES_FOLDER)

    def __delete_unnecessary(self, attr, elem, folder):
        necesary = [get_name(e.attribute(attr)) for e in self.findAllElements(elem)]
        delete_files(self.getPathToFolder(folder), lambda f:not f in necesary)
    
    def findAllElements(self, selector):
        return self.page().currentFrame().findAllElements(selector)
    
    
    ############################################################################
    #
    # JS
    #
    ############################################################################
    
    def execCommand(self, cmd, arg = None):
        if arg:
            jsString = _qstr("document.execCommand(\"%1\", false, \"%2\")").arg(cmd).arg(arg)
        else:
            jsString = _qstr("document.execCommand(\"%1\", false, null)").arg(cmd)
        self.evaluateJavaScript(jsString)

    def evaluateJavaScript(self, js):
        frame = self.page().mainFrame()
        return frame.evaluateJavaScript(js);
    
    def callJS(self, func, *args):
        arguments = ','.join(['"%s"'%a for a in args])
        js =  '$("body").%s(%s)'%(func, arguments)
        return self.evaluateJavaScript(js).toString() == 'false'
    
    def jsTrigger(self, event, *args):
        extra_parameters = ','.join(['"%s"'%re.sub('\W+', ' ', unicode(a), flags=re.U) for a in args if a])
        if extra_parameters:
            js = "$('body').trigger('%s', [%s])"%(event, extra_parameters)
        else:
            js = "$('body').trigger('%s')"%event
        self.evaluateJavaScript(js)
        
    #--------------------------------------------------------------------------            
    def getPathToFolder(self, folderName):
        curdir = os.path.dirname(self.path)   
        return join(curdir, folderName)
