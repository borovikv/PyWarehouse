# -*- coding: utf-8 -*-
'''
Created on 21.02.2012

@author: vb
'''

from PyQt4 import QtCore, QtGui
from PyQt4.QtWebKit import QWebPage, QWebView
import os
import re
import shutil
import urllib2
import locale
import urllib
import urlparse

from EditorPanel.EditorFilter import EditorFilter
from Utils.Resources import Resources
from Utils.Events import ObservableEvent
from Dialogs.InsertDialog import InsertDialog


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
    
    def __init__(self, workFolder, parent = None):
        QWebView.__init__(self, parent)
        self.insertDialog = InsertDialog(self)
        self.workFolder = workFolder
        self.urlForCopy = None
        self.sources_preparate()
        css = []
        scripts = ["jquery", 
                   "utils", 
                   "formatting", 
                   "table", 
                   "task_and_tag",
                   "unload",
                   ]
        self.makeHeader(scripts, css)
        self.installEventFilter(EditorFilter(self))      
        self.editor_actions = self.getActionMap()

    def make_js_include(self, js):
        return "<script src='%s.js' type='text/javascript'></script>"%(
                os.path.join(Resources.getScriptsFolder(), js))
    
    def make_css_include(self, css):
        if not css: return ''
        return "<link rel='stylesheet' href='%s.css' type='text/css' media='screen'/>"%(
                os.path.join(Resources.getStylesFolder(), css))       
    
    def scriptTag(self):
        js = "<script type='text/javascript'>"
        js += "imgFolder = 'file://%s'"%Resources.getImageFolderPath()
        js += "</script>"
        return js
     
    def makeHeader(self, scripts, *css):
        def_head = """<head>
        <meta http-equiv='Content-Type' content='text/html; charset=UTF-8'>
        <link rel='stylesheet' href='../_source/base.css' type='text/css' media='screen'/>
        %s
        </head>
        """
        
        self.extendedHeader = ''
        for c in css:
            self.extendedHeader += self.make_css_include(c)
        self.extendedHeader += self.scriptTag()
        for js in scripts:
            self.extendedHeader += self.make_js_include(js)    
        self.extendedHeader = def_head % self.extendedHeader
        
        self.defaultHeader = def_head % ''
        
    
    
    #####################################################################################################
    #
    # Actions
    #
    #####################################################################################################
    
    def getInterfacesElements(self):
        showInButton = self.makeButton("", Resources.getIcon(Resources.iconOpenFolder), self.showInFolder)
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
        return actions
    
    def  execute(self, cmd, s_arg = None):
        action = self.editor_actions.get(cmd)
        if not action: return
        if isinstance(action, str):
            self.js_event(action)
        elif self.has_params(cmd) and s_arg:
            action(s_arg)
        else:
            action()
            
    def showInFolder(self):
        if hasattr(self, "path"):
            process2 = QtCore.QProcess(self)
            process2.start('xdg-open ' + "\"" + os.path.dirname(self.path) + "\"")
    
    def onCreateTable(self, row_col="2,2"): 
        self.evaluateJavaScript("ROW_COL='%s'"%row_col)
        self.js_event("onCreateTable")

    def onInsert(self):
        self.insertDialog.exec_()
        path = self.insertDialog.path
        if not path: return
        
        if os.path.splitext(path)[1] in (".png", ".jpg", ".gif", ".bmp", ".jpeg"):
            f = self.copyFile(path)
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
        link = QtCore.QString(link)
        if not link.isEmpty():
            url = self.guessUrlFromString(link)
            if url.isValid():
                # make folder Files in directory of page
                dst = os.path.dirname(self.path)
                dst += os.sep + Editor.FILES_FOLDER
                if not os.path.exists(dst):
                    os.mkdir(dst) 
                # end make
                
                url = self.copyLocalFile(unicode(url.toString(), 'utf-8')[7:], dst)
                
                
                return {"url":url, "name":os.path.split(url)[1] }

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
        
        data = unicode(f.readAll(), 'utf-8')
        data = re.sub(r'<head>[\w\W]*</head>', self.extendedHeader, data)
        self.setHtml(data, QtCore.QUrl.fromLocalFile(path))
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
        src = os.path.join(Resources.getSourcesFolderPath(), "sources.html")
        shutil.copyfile(src, path)
        self.setPath(path)
        self.loadFromPath(path)
#        source = QtCore.QFile(os.path.join(Resources.getSourcesFolderPath(), "sources.html"))
#        source.open(QtCore.QIODevice.ReadOnly)
#        html = QtCore.QString.fromUtf8(source.readAll())
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
        #print oldPath, newPath
        self.saveDoc()
        src = os.path.join(self.workFolder, oldPath)
        dst = os.path.join(self.workFolder, newPath)
        shutil.move(src, dst)
        os.rename(os.path.join(dst, oldPath + ".html"), os.path.join(dst, newPath + ".html"))
    
    #####################################################################################################
    #
    # Paste IMG 
    #
    #####################################################################################################    
    def pastePreparation(self):
        clipboard = QtGui.QApplication.clipboard()
        
        text = clipboard.text("html")
        if not text: return
        
        imgs = self.getAllImg(text)
        if not imgs: return
                
        newImgs = self.copyImg(imgs)
        if not newImgs: return
        
        for img in newImgs:
            if img and newImgs[img]:
                old = QtCore.QString(img)
                new = QtCore.QString(newImgs[img])
                text.replace(old, new)
            
        data = QtCore.QMimeData()
        data.setHtml(text)
        clipboard.setMimeData(data)
                
    def getAllImg(self, html):
        imgReg = re.compile("<img\s[^>]*?>")
        match = imgReg.findall(html)
        return match
    
    def copyImg(self, imgs):
        newImgs = {}
        for img in imgs:
            newImgs[img] = self.copyFileImg(img)
        return newImgs        
        
    def copyFileImg(self, img):
        imgReg = re.compile("src\s*=\s*[\"']([^\"']*?)[\"']")
        #get path to original file
        oldPath = imgReg.search(img).groups()[0]

        path = self.copyFile(oldPath)
        if path:
            img = "" + img     
            # replace src="xxx/yyy/zzz.abc" - src="IMG/zzz.abc"
            img.replace(oldPath, path)
            return img
        else:
            return None      
               
    def copyFile(self, src):

        dest = os.path.dirname(self.path)
        dest += os.sep + Editor.IMG_FOLDER
        if not os.path.exists(dest):
            os.mkdir(dest) 
        
        link = self.getFullPathFromStr(self.linkPreparation(src))
        newPath = None
        if link:
            path = link["link"]
            if link["type"] == "http":
                newPath = Editor.IMG_FOLDER + os.sep + self.downloadFile(path, dest)
                
            if link["type"] == "local":
                newPath = self.copyLocalFile(path, dest) 
        return newPath
    
    def copyLocalFile(self, src, dest):
        
        fileName = os.path.split(src)[1]        
        newFile = os.path.join(dest, fileName)

        try:

            if os.path.exists(newFile) and self.path != self.urlForCopy:
                f, ext = os.path.splitext(fileName)
                s = re.search("(.*)\(([0-9]+)\)$", f)

                if s:
                    counter = int(s.group(2))
                    counter = "(" + str(counter + 1) + ")"
                    fn = s.group(1) + counter + ext
                else:
                    fn = f + "(1)" + ext
                
                dst = os.path.join(dest, fn)
                shutil.copyfile(src, dst)
            elif not os.path.exists(newFile):
                shutil.copy(src, dest)
                
            newPath = os.path.join(os.path.split(dest)[1], fileName)
        except:
            print("exept copyFile")
            newPath = None
        
        return newPath
    
    def downloadFile(self, url, destination):
        _filepath, filename = os.path.split(urlparse.urlparse(url).path)
        urllib.urlretrieve(url, destination + os.sep + filename)
        return filename
        
    def setUrlForCopy(self):
        self.urlForCopy = self.path
    
    def linkPreparation(self, link):
        link = link.replace("&amp;", "&") 
        if isinstance(link, unicode):
            return link
        try:
            link = link.toUtf8()
        except:
            print('link.toUtf8() error')
        link = unicode(link, 'utf-8')

        try:
            link = self.decodeURI(link)
        except:
            print("bad decode")
        
        return link
        
    
    def decodeURI(self, uri):
        return urllib.unquote(uri.encode('ascii'))    
    
    def getFullPathFromStr(self, link):
        
        objUrl = urlparse.urlparse(link)
        
        if objUrl.scheme == 'file' and os.path.exists(objUrl.path):
            return {"type": "local", "link" : objUrl.path}
        
        if objUrl.scheme == 'http':
            return {"type": "http", "link" : link}
        
        if objUrl.netloc:
            try:
                fullpath = 'http' + link
                urllib2.urlopen(fullpath)
                return {"type": "http", "link" : fullpath}
            except:
                print("bad location 1")
                
                
        if objUrl.path.startswith('www.'):
            #try to open file on http if false fale may by local
            try:
                fullpath = "http://" + link
                urllib2.urlopen(fullpath)
                return {"type": "http", "link" : fullpath}
            except:
                print("bad location 2")
                    
        
        # Might be a file
        if os.path.exists(link):
            return {"type": "local", "link" : link}
        
        # Might be a shorturl 
        if self.urlForCopy:
            #print(link, objUrl, self.urlForCopy)
            par = os.path.dirname(self.urlForCopy)
            fullpath = os.path.join(par, link)
            return {"type" : "local", "link" : fullpath}
        
        # Might be a shorturl from www or other surces
            
        return None    
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
    # Utils
    #
    ###################################################################################################
    def tr(self, str_):
        return QtCore.QObject.tr(QtCore.QObject(), str_)
    
    def execCommand(self, cmd, arg = None):
        if arg:
            jsString = QtCore.QString("document.execCommand(\"%1\", false, \"%2\")").arg(cmd).arg(arg)
        else:
            jsString = QtCore.QString("document.execCommand(\"%1\", false, null)").arg(cmd)
        self.evaluateJavaScript(jsString)
    
    def evaluateJavaScript(self, js):
        frame = self.page().mainFrame()
        return frame.evaluateJavaScript(js);
    
    def insertHtml(self, htmlText):
        self.execCommand("insertHTML", htmlText)
    
    def js_event(self, event):
        js = "$('body').trigger('%s')"%event
        self.evaluateJavaScript(js)   
    
    def js_event_update(self, t, altKey, ctrlKey, shiftKey, which, keyCode):
        js = "update('%s', %s, %s, %s, %s, %s)"%(t, altKey, ctrlKey, shiftKey, which, keyCode)
        #print js
        self.evaluateJavaScript(js)
            
    def guessUrlFromString(self, link):
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
        
    def makeButton(self, name, icon, func):
        if icon:
            but = QtGui.QPushButton(icon, name)
        else:
            but = QtGui.QPushButton(name)
        but.clicked.connect(func) 
        return but 
    
    def sources_preparate(self):
        sourceFolder = os.path.join(self.workFolder, '_source')
        src = os.path.join(Resources.getSourcesFolderPath())
        def func(arg, dirname, names):
            for name in names:
                path = os.path.join(sourceFolder, name)
                if not os.path.exists(path):
                    src = os.path.join(dirname, name)
                    shutil.copy(src, path)
                    
        if not os.path.exists(sourceFolder):
            shutil.copytree(src, sourceFolder)
        else:
            os.path.walk(src, func, None)
        
    def delete_unnecessary(self):
        cur_dir = os.path.dirname(self.path)
        img_folder = os.path.join(cur_dir, Editor.IMG_FOLDER)
        files_folder = os.path.join(cur_dir, Editor.FILES_FOLDER)
        necesary_img = [os.path.basename(unicode(e.attribute('src'), 'utf-8')) 
                    for e in self.page().currentFrame().findAllElements('img')]
        
        necesary_files = [os.path.basename(unicode(e.attribute('href'), 'utf-8'))
                 for e in self.page().currentFrame().findAllElements('div.File>a')]
        
            
        for _, _, files in os.walk(img_folder):
            for f in files:
                if not f in necesary_img:
                    os.remove(os.path.join(img_folder, f))
        
        for _, _, files in os.walk(files_folder):
            for f in files:
                if not f in necesary_files:
                    os.remove(os.path.join(files_folder, f))
                
    
    def has_params(self, cmd):
        return cmd.lower() == 'insert table'
    
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
            
            
            