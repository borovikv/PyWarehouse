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
from Utils.QUtils import openFolder, getGoodUrl
from PyQt4.QtCore import QString as _qstr
from Dialogs.Dialog import DualLineDialog
locale.setlocale(locale.LC_ALL, '')
        

# Actions block
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
        self.findReplaceDialog = DualLineDialog(self)
        self.workFolder = workFolder
        self.urlForCopy = None
        self.path = None
        
        # copy nessesary files to workFolder
        self.sources_preparate()
        # context for makeHeader and load from path
        self.context =  { 'imgFolder': Resources.getImageFolderPath(),
                          'scriptFolderPath': Resources.getScriptsFolder(),
                          'cssFolderPath': Resources.getStylesFolder(), }
        self.makeHeader()
        self.installEventFilter(EditorFilter(self))      
        self.editor_actions = self.getActionMap()
     
    def makeHeader(self):
        self.defaultHeader = """<head>
        <meta http-equiv='Content-Type' content='text/html; charset=UTF-8'>
        <link rel='stylesheet' href='../_source/base.css' type='text/css' media='screen'/>
        %s
        </head>
        """
        
        f = file(Resources.getSource('header.html'))
        header = unicode(f.read())
        
        self.extendedHeader = render_template(header, self.context)
    
    #####################################################################################################
    #
    # Actions
    #
    #####################################################################################################
    
    def getInterfacesElements(self):
        showInButton = QUtils.makeButton("", Resources.getIcon(Resources.iconOpenFolder), self.showInFolder)
        interfaceElements = {}
        interfaceElements["showInButton"] = showInButton
        return interfaceElements
    
    def getActionMap(self):
        actions = {}
        actions["insert table"] = self.onCreateTable
        actions["column after"] = 'onInsertColAfter'
        actions["column before"] = 'onInsertColBefore'
        actions["row after"] = 'onInsertRowAfter'
        actions["row before"] = 'onInsertRowBefore'
        actions["delete column"] = 'onDeleteCol'
        actions["delete row"] = 'onDeleteRow'
        
        actions["bold"] = 'onBold'
        actions["underline"] = 'onUnderline'
        actions["italic"] = 'onItalic'
        actions["orderer list"] = 'onOList'
        actions["unorderer list"] = 'onUList'
        actions["highlight"] = 'onHighlight'
        actions["horizontal rule"] = 'insertHorizontalRule'
        actions["remove format"] = 'onRemoveFormat'
        
        #actions["insert tag"] = 'onTag'
        actions["insert task"] = 'onTask'
        actions["delete task"] = 'onDeleteTask'
        
        actions["insert object"] = self.onInsert
        
        actions["show in folder"] = self.showInFolder
        actions["find or replace"] = self.find_or_replace
        
        return actions
    
    def  execute(self, cmd, s_arg = None):
        action = self.editor_actions.get(cmd)
        if not action: return
        if isinstance(action, basestring):
            self.js_event(action)
        elif self.has_params(cmd) and s_arg:
            action(s_arg)
        else:
            action()
    
    def has_params(self, cmd):
        return cmd.lower() in ( 'insert table', 'find on page', 'replace')
            
    def showInFolder(self):
        if self.path:
            openFolder(self, self.get_path_to_folder(Editor.SELF))
    
    def find_or_replace(self):
        self.findReplaceDialog.show()
        text, newtext = ( self.findReplaceDialog.getFirstLineText(), 
                          self.findReplaceDialog.getSecondLineText() )
        if not text:
            text = self.selectedText()
        
        if not newtext:
            self.findText(text, QWebPage.HighlightAllOccurrences)
        else:
            self.js_event_with_param('replace', OLD_TEXT=text, NEW_TEXT=newtext)
        
    def onCreateTable(self, row_col="2,2"): 
        self.js_event_with_param("onCreateTable", ROW_COL=row_col)

    def onInsert(self):
        self.insertDialog.exec_()
        path = self.insertDialog.path
        if not path: return
        
        if is_image(path):
            f = copy_file(path, self.get_path_to_folder(Editor.IMG_FOLDER), None)
            if not f: return
            self.execCommand("insertImage", f)
        elif os.path.isfile(path):    
            f = self.insertFile(path)
            icon = Resources.getSource("File.png")
            htmlText = "&nbsp;<div class='File'><a href='%s'><img src='%s'>%s</a></div>&nbsp"%( f["url"], icon, f["name"])
            self.insertHtml(htmlText)
        else:
            self.execCommand("createLink", path);
             
    def insertFile(self, link):        
        link = _qstr(link)
        if link.isEmpty():
            return
        url = getGoodUrl(link)
        if url.isValid():
            dst = self.get_path_to_folder(Editor.FILES_FOLDER)
            make_dir_if_not_exist(dst) 
            url = copy_local_file(unicode(url.toString(), 'utf-8')[7:], dst)
            
            return {"url":url, "name": get_name(url)}

    def openLink(self, url):
        QtGui.QDesktopServices.openUrl(url)
        return True
    
    #####################################################################################################
    #
    # File operation
    #
    #####################################################################################################    
    def loadFromPath(self, path):
        if not QtCore.QFile.exists(path):
            return False
        
        f = QtCore.QFile(path)
        if not f.open(QtCore.QFile.ReadOnly):
            return False
        
        template = unicode(f.readAll(), 'utf-8')
        #template = re.sub(r'<head>[\w\W]*</head>', self.extendedHeader, data)
        template = render_template(template, self.context)
        self.setHtml(template, QtCore.QUrl.fromLocalFile(path))
        self.page().setLinkDelegationPolicy(QWebPage.DelegateAllLinks)
        self.linkClicked[QtCore.QUrl].connect(self.openLink)
        self.setFocus()
        self.setPath(path)
        
        return True
    
    def openDoc(self, path):
        self.loadFromPath(path)
    
    def saveDoc(self, path = None, doc=None):
        if not hasattr(self, "path"):
            self.newDoc()
        
        if not path:
            path = self.path
        
        data =  QtCore.QFile(path)
        success = data.open(QtCore.QFile.WriteOnly | QtCore.QFile.Truncate)
        if success:        
            self.evaluateJavaScript('$(window).unload()')
            html = doc or self.page().mainFrame().toHtml()
            #rx = QtCore.QRegExp("<head>([\s\S\r]*)</head>")
            #html.replace(rx, self.defaultHeader)
            html = html.toUtf8()
            c = data.write(html)
            success = (c >= html.length())
        self.setWindowModified(False)
        return success
        
    def setPath(self, path):
        self.path  = path
    
    def newDoc(self, path=None):
        src = join(Resources.getSourcesFolderPath(), "sources.html")
        shutil.copyfile(src, path)
        self.setPath(path)
        self.loadFromPath(path)
#        source = QtCore.QFile(join(Resources.getSourcesFolderPath(), "sources.html"))
#        source.open(QtCore.QIODevice.ReadOnly)
#        html = _qstr.fromUtf8(source.readAll())
#        html = html.replace(QtCore.QRegExp('<head>[\w\W]*</head>'),
#                            self.extendedHeader)
#        
#        self.page().mainFrame().setHtml(html)
#        print self.page().mainFrame().toHtml()
#        self.setFocus()
#        self.page().setContentEditable(True)
#        self.setPath("")
#        
#        self.saveDoc(path, html)
        
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
    #  interface
    def pastePreparation(self):
        
        dest = self.get_path_to_folder(Editor.IMG_FOLDER)
        
        clipboard = QtGui.QApplication.clipboard() 
        
        text = clipboard.text("html")
        if not text: return
                
        newImgs = copy_img_html(text, dest, self.urlForCopy)
        #[old_src: new_src]
        if not newImgs: return
        
        for img in newImgs:
            if img and newImgs[img]:
                text.replace(_qstr(img), _qstr(newImgs[img]))
            
        data = QtCore.QMimeData()
        data.setHtml(text)
        clipboard.setMimeData(data)
                
    
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
    
    def js_event(self, event):
        js = "$('body').trigger('%s')"%event
        self.evaluateJavaScript(js)   
    
    def js_event_with_param(self, event, **params):
        for p in params:
            self.evaluateJavaScript("%s='%s'"%(p, params[p]))
        self.js_event(event)

            
    
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
            path = event.getParam(ObservableEvent.path)
            if os.path.exists(path):
                self.openDoc(path)
            else:
                self.newDoc()
            
        if event.type == ObservableEvent.close and hasattr(self, 'path') and self.path:
            self.saveDoc()
            self.delete_unnecessary()
        
        if event.type is ObservableEvent.execute:
            self.execute(event.getParam('command'), event.getParam('params'))
            
    #==============================================================================================
    # Start and Stop 
    #==============================================================================================     
    
    def sources_preparate(self):
        """
        копирует папку _source или только недостающие файлы 
        в директорию с заметками
        """
        src = Resources.getSourcesFolderPath()
        dest = self.get_path_to_folder(Editor.SOURCE_FOLDER)
        copy_folder(src, dest, lambda name: True)
        
    def delete_unnecessary(self):
        necesary_img = [get_name(e.attribute('src')) 
                    for e in self.findAllElements('img')]
        
        necesary_files = [get_name(e.attribute('href'))
                 for e in self.findAllElements('div.File>a')]
        
        delete_files(self.get_path_to_folder(Editor.IMG_FOLDER), lambda f: not f in necesary_img)
        delete_files(self.get_path_to_folder(Editor.FILES_FOLDER), lambda f: not f in necesary_files)
            