# -*- coding: utf-8 -*-
'''
Created on 21.02.2012

@author: vb
'''

from PyQt4 import QtCore, QtGui
from PyQt4.QtWebKit import QWebPage, QWebView
import os
from os.path import join
import shutil
import locale
from EditorPanel.EditorFilter import EditorFilter
from Utils.Resources import Resources
from Utils.Events import ObservableEvent
from Dialogs.InsertDialog import InsertDialog
from Utils import QUtils
from Utils.utils import render_template, copy_img_html, delete_files,\
    make_dir_if_not_exist, copy_local_file, copy_file, copy_folder, is_image, get_name
from PyQt4.QtCore import QString as _qstr
from Dialogs.Dialog import LineDialog, FindReplaceDialog
locale.setlocale(locale.LC_ALL, '')
        

# Редактировать
# File operation
# Functionality
# Paste IMG 
# Utils
# Observe
class Editor(QWebView):
    FILES_FOLDER = "Files" 
    IMG_FOLDER = "IMG"
    SOURCE_FOLDER = "_source"
    SELF = ""
    
    def __init__(self, workFolder, parent = None):
        QWebView.__init__(self, parent)
        self.insertDialog = InsertDialog(self)
        self.findReplaceDialog = FindReplaceDialog(self)
        self.workFolder = workFolder
        self.urlForCopy = None
        self.path = None
        self.makeHeader()
        self.copySourceFilesToWorkfolder()
        self.installEventFilter(EditorFilter(self))      
        self.editor_actions = self.getActionMap()
     
    def makeHeader(self):
        self.context =  { 'imgFolder': Resources.getImageFolderPath(),
                          'scriptFolderPath': Resources.getScriptsFolder(),
                          'cssFolderPath': Resources.getStylesFolder(), }
        f = file(Resources.getSource('header.html'))
        header = unicode(f.read())
        self.extendedHeader = header%self.context
    
    
    def getInterfacesElements(self):
        showInButton = QUtils.makeButton("", Resources.getIcon(Resources.iconOpenFolder), self.showInFolder)
        interfaceElements = {}
        interfaceElements["showInButton"] = showInButton
        return interfaceElements
    
    def getActionMap(self):
        actions = {
                   "insert table": 'onCreateTable', 
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
                    "insert object": self.onInsert,
                    "show in folder": self.showInFolder,
                    "find or replace": self.findReplace,
                }
        return actions
    
            
    def showInFolder(self):
        if self.path:
            QUtils.openFolder(self, self.get_path_to_folder(Editor.SELF))
    
    def findReplace(self):
        self.findReplaceDialog.show()
    
    def findNext(self):
        text = self.getTextToFind()
        self.findText(text)
    
    def findAll(self):
        text = self.getTextToFind()
        self.findText(text, QWebPage.HighlightAllOccurrences)

    def replaceNext(self):
        text = self.getTextToFind()
        newtext = self.getTextToReplace()
        self.js_event('replace', 'next', text, newtext)
    
    def replaceAll(self):
        newtext=None
        text = self.getTextToFind()
        self.js_event('replace', 'all', text, newtext)
    
    def getTextToFind(self):     
        text = self.findReplaceDialog.getLineText(0)   
        if not text:
            text = self.selectedText()
        return text

    def getTextToReplace(self):
        return self.findReplaceDialog.getLineText(1)
        

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
        icon = Resources.getSource("File.png")
        htmlText = "&nbsp;<div class='File'><a href='%s'><img src='%s'>%s</a></div>&nbsp" % (url, icon, text)
        self.insertHtml(htmlText)

    def copyImage(self, path):
        return copy_file(path, self.get_path_to_folder(Editor.IMG_FOLDER), None)

    def copyFile(self, link):        
        link = _qstr(link)
        if link.isEmpty():
            return
        url = QUtils.getGoodUrl(link)
        if url.isValid():
            dst = self.get_path_to_folder(Editor.FILES_FOLDER)
            make_dir_if_not_exist(dst) 
            url = copy_local_file(unicode(url.toString(), 'utf-8')[7:], dst)
            
            return {"url":url, "name": get_name(url)}

    def openLink(self, url):
        QtGui.QDesktopServices.openUrl(url)
        return True
    
    #---------------------------------------------------------------------------
    def openDoc(self, path):
        self.loadFromPath(path)
    
    
    def saveDoc(self, path=None):
        path = self.getPath(path)
        if not path: return
        
        success, f = QUtils.openFile(path)
        if success:        
            self.onSave()
            success = self.saveFile(f)
        self.setWindowModified(False)
        return success

    def getPath(self, path=None):
        if not path and hasattr(self, "path"): 
            path = self.path
        return path

    def onSave(self):
        return self.evaluateJavaScript('$(window).onSave()')
    
    def saveFile(self, aFile):
        html = self.getHtml() 
        #rx = QtCore.QRegExp("<head>([\s\S\r]*)</head>")
        #html.replace(rx, self.defaultHeader)
        html = html.toUtf8()
        c = aFile.write(html)
        success = c >= html.length()
        return success

    def getHtml(self):
        return self.page().mainFrame().toHtml()





    



    
    def loadFromPath(self, path):
        template = self.getTemplate(path)
        if not template:
            return False
        self.setHtml(template, QtCore.QUrl.fromLocalFile(path))
        self.page().setLinkDelegationPolicy(QWebPage.DelegateAllLinks)
        self.linkClicked[QtCore.QUrl].connect(self.openLink)
        self.setFocus()
        self.setPath(path)
        return True
    
    def getTemplate(self, path):
        if not os.path.exists(path): 
            return
        with open(path) as f:
            template = u''.join(f.readlines())
            template%self.context
            return template
#         f = QtCore.QFile(path)
#         if not f.open(QtCore.QFile.ReadOnly):
#             return
        
#         template = unicode(f.readAll(), 'utf-8')
#         template = render_template(template, self.context)
#         self.insert_header_if_not_exist(template)
#         return template

    def insert_header_if_not_exist(self, template):
        #template = re.sub(r'<head>[\w\W]*</head>', self.extendedHeader, data)
        pass
    
        
    def setPath(self, path):
        self.path  = path
    
    def newDoc(self, path=None):
        if not path:
            return
        src = join(Resources.getSourcesFolderPath(), "sources.html")
        shutil.copyfile(src, path)
        self.setPath(path)
        self.loadFromPath(path)
        
    def rename(self, oldPath, newPath):
        oldPath = unicode(oldPath)
        newPath = unicode(newPath)
        self.saveDoc()
        src = join(self.workFolder, oldPath)
        dst = join(self.workFolder, newPath)
        shutil.move(src, dst)
        os.rename(join(dst, oldPath + ".html"), join(dst, newPath + ".html"))
    
    #####################################################################################################
    #
    # Paste IMG 
    #
    #####################################################################################################  
    def pastePreparation(self):
        clipboard = QtGui.QApplication.clipboard() 
        
        text = clipboard.text("html")
        if not text: 
            return        
        
        newImgs = self.download_all_images_from_html(text)
        if not newImgs: 
            return
        
        self.replace_img_src_by_local_src(text, newImgs)
            
        data = QtCore.QMimeData()
        data.setHtml(text)
        clipboard.setMimeData(data)

    def download_all_images_from_html(self, text):
        dest = self.get_path_to_folder(Editor.IMG_FOLDER)
        newImgs = copy_img_html(text, dest, self.urlForCopy)
        return newImgs
                
    def replace_img_src_by_local_src(self, text, newImgs):
        # newImgs = [old_src: new_src]
        for img in newImgs:
            if img and newImgs[img]:
                text.replace(_qstr(img), _qstr(newImgs[img]))

    
    def setUrlForCopy(self):
        self.urlForCopy = self.path
    

    ###################################################################################################
    #
    # Events
    #
    ###################################################################################################
    def event(self, e):
        if e.type() in (QtCore.QEvent.KeyPress, ):
            if (e.matches(QtGui.QKeySequence.Italic) 
                or e.matches(QtGui.QKeySequence.Underline) 
                or e.matches(QtGui.QKeySequence.Bold)):
                e.ignore()
                return True
        #if e.type() == QWebView.l   
        return QWebView.event(self, e)
    
    def contextMenuEvent(self, *args, **kwargs):
        pass
    
    def  execute(self, cmd, s_arg = None):
        action = self.editor_actions.get(cmd)
        if not action: return
        if isinstance(action, basestring):
            self.js_event(action, s_arg)
        else:
            action()
    ###################################################################################################
    #
    # Utils js
    #
    ###################################################################################################
    
    def execCommand(self, cmd, arg = None):
        if arg:
            jsString = _qstr("document.execCommand(\"%1\", false, \"%2\")").arg(cmd).arg(arg)
        else:
            jsString = _qstr("document.execCommand(\"%1\", false, null)").arg(cmd)
        self.evaluateJavaScript(jsString)
    
    def evaluateJavaScript(self, js):
        frame = self.page().mainFrame()
        return frame.evaluateJavaScript(js);
    
    def insertHtml(self, htmlText):
        self.execCommand("insertHTML", htmlText)
    
    def js_event(self, event, *args):
        extra_parameters = ''
        for argument in args:
            extra_parameters += "'%s',"%argument
        if extra_parameters:
            js = "$('body').trigger('%s', [%s])"%(event, extra_parameters)
        else:
            js = "$('body').trigger('%s')"%event
        self.evaluateJavaScript(js)   
    
    def js_event_update(self, t, altKey, ctrlKey, shiftKey, which, keyCode):
        js = "update('%s', %s, %s, %s, %s, %s)"%(t, altKey, ctrlKey, shiftKey, which, keyCode)
        #print js
        self.evaluateJavaScript(js)
    
    ######################################################################################################################
    #
    # Utils
    #
    ######################################################################################################################
                
    def get_path_to_folder(self, folder_name):
        if folder_name == Editor.SOURCE_FOLDER:
            cur_dir = self.workFolder
        else:
            cur_dir = os.path.dirname(self.path)   
        return join(cur_dir, folder_name)
        
    
    
    def findAllElements(self, selector):
        return self.page().currentFrame().findAllElements(selector)
    
    ######################################################################################################################
    #
    # Observe
    #
    ######################################################################################################################

    def update(self, event):
        if event.type == ObservableEvent.start:
            self.on_start(event)
        
        if event.type == ObservableEvent.close:
            self.on_close(event)
        
        if event.type is ObservableEvent.execute:
            self.on_execute(event)

    def on_start(self, event):
        path = event.getParam(ObservableEvent.path)
        if os.path.exists(path):
            self.openDoc(path)


    def on_close(self, event):
        if hasattr(self, 'path') and self.path:
            self.saveDoc()
            self.delete_unnecessary()

    def on_execute(self, event):
        self.execute(event.getParam('command'), event.getParam('params'))

            
    #==============================================================================================
    # Start and Stop 
    #==============================================================================================     
    
    def copySourceFilesToWorkfolder(self):
        """
        копирует папку _source или только недостающие файлы 
        в директорию с заметками
        """
        src = Resources.getSourcesFolderPath()
        dest = self.get_path_to_folder(Editor.SOURCE_FOLDER)
        copy_folder(src, dest, lambda name: True)
        

    def delete_unnecessary(self):
        self.delete_unnecessary_img()
        self.delete_unnecessary_files()
    
    def delete_unnecessary_img(self):
        self.__delete_unnecessary('src', 'img', Editor.IMG_FOLDER)

    def delete_unnecessary_files(self):
        self.__delete_unnecessary('href', 'div.File>a', Editor.FILES_FOLDER)

    def __delete_unnecessary(self, attr, elem, folder):
        necesary = [get_name(e.attribute(attr)) for e in self.findAllElements(elem)]
        delete_files(self.get_path_to_folder(folder), lambda f:not f in necesary)
            