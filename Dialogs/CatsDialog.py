'''
Created on Jul 15, 2012

@author: vb
'''
from PyQt4 import QtGui
from PyQt4.QtCore import Qt, QUrl, QEvent
from Dialogs.Dialog import DialogBox
from Utils.Events import ObservableEvent
from Utils.Observable import Observable
import re

def getDescription(s):
    s = unicode(s)
    return {        
        "google"          : "search in google", 
        "wikipedia"       : "search in wikipedia ru",
        "search"          : "search in your notes",
        "all"             : "show all commands",
        "insert table"    : "insert table row col",
        "column after"    : "insert column after current column",
        "column before"   : "insert column before current column",
        "row after"       : "insert row after current row",
        "row before"      : "insert row before current row",
        "delete column"   : "delete current column",
        "delete row"      : "delete current row",
        "bold"            : "bold",
        "underline"       : "underline",
        "italic"          : "italic",
        "orderer list"    : "insert orderer list",
        "unorderer list"  : "insert unorderer list",
        "highlight"       : "highlight selectet text",
        "horizontal rule" : "insert horizontal rule",
        "remove format"   : "remove format",
        "insert tag"      : "insert tag",
        "insert task"     : "insert task",
        "insert object"   : "insert link, image or file",
        "show in folder"  : "show current note in file sistem",
     }.get(s, "")

#-------------------------------------------------------------------------------    
class Line(QtGui.QLineEdit):
    def __init__(self, parent=None):
        self.parent = parent
        super(Line, self).__init__(parent)
    
    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Up, Qt.Key_Down):
            self.parent.delegateEvent(event, self)
            event.ignore()
        elif event.key() in (Qt.Key_Return, Qt.Key_Enter):
            self.parent.evaluate()

        return QtGui.QLineEdit.keyPressEvent(self, event)       
    
    def keyReleaseEvent(self, event):
        if event.key() not in (Qt.Key_Return, Qt.Key_Enter):
            text = self.text().remove(self.selectedText())
            self.parent.showCompletion(text)
        
        return QtGui.QLineEdit.keyReleaseEvent(self, event)
    
    def event(self, event):
        if event.type() in (QEvent.KeyPress, QEvent.KeyRelease) and event.key() == Qt.Key_Tab:
            self.parent.selectFirst()
            return True 
        return QtGui.QLineEdit.event(self, event)
    
    def onUpdate(self, event):
        pass
    
    
    
#-------------------------------------------------------------------------------
class ListWidget(QtGui.QListWidget, Observable):
    def __init__(self, parent=None): 
        QtGui.QListWidget.__init__(self, parent)
        Observable.__init__(self)
        self.shortcut_focus = False
    
    def keyPressEvent(self, event):
        isArrowEvent = event.key() in ( Qt.Key_Down, Qt.Key_Up, )
        
        if self.shortcut_focus and isArrowEvent:
            row = 0 if event.key() == Qt.Key_Down else  self.count() - 1
            self.setCurrentRow(row)
            self.shortcut_focus = False 
        
        elif not self.shortcut_focus and isArrowEvent:
            super(ListWidget, self).keyPressEvent(event)
        
        if not isArrowEvent:
            e = ObservableEvent('keyPress', event=event)
            self.notifyObservers(e)
        text  = self.currentItem().text()
        e = ObservableEvent('selectText', text=text)
        self.notifyObservers(e)
    
    def onUpdate(self, event):
        pass
    
    def focusInEvent(self, event):
        self.shortcut_focus = event.reason() == Qt.ShortcutFocusReason
        if not self.shortcut_focus:
            self.parent().choose(self.currentItem().text()) 
        return QtGui.QListWidget.focusInEvent(self, event)

#-------------------------------------------------------------------------------
class Browser(QtGui.QTextBrowser):
    def __init__(self, parent=None):
        super(Browser, self).__init__()


#-------------------------------------------------------------------------------
class CatsDialog(DialogBox, Observable):
    def __init__(self, actions, parent=None):
        
        width, height, color = 700, 400, "#aaa"
        DialogBox.__init__(self, width, height, color, parent)
        Observable.__init__(self)
        self.registerObserver(self)
                
        self.actions = actions
        self.catsActions = {
            "google": self.google, 
            "wikipedia": self.wikipedia,
            "search": self.search,
            "all": self.showAllCommands
        }
        c = '|'.join(self.getAllActions())
        self.re_pre_cmd = re.compile(r'^(%s)\s*(.*)'%c)
        self.re_post_cmd = re.compile(r'^([^\s]*)\s+(%s)'%c)

        self.createComplectionList(width)
        self.createCommandLine()
        self.complection_list.registerObserver(self)
        self.complection_list.registerObserver(self.cmd)
        self.createBrowser()
        self.setBackground()
        self.createUI()

    def createComplectionList(self, width):
        self.complection_list = ListWidget(self)
        self.complection_list.setMaximumWidth(width * 0.2)


    def createCommandLine(self):
        self.cmd = Line(self)
        self.cmd.setFocus()
        allActions = self.getAllActions()
        completer = QtGui.QCompleter(allActions)
        completer.setCompletionMode(QtGui.QCompleter.InlineCompletion)
        self.cmd.setCompleter(completer)


    def createBrowser(self):
        self.browser = Browser()
        self.browser.setFocusPolicy(Qt.NoFocus)


    def setBackground(self):
        css = "background-color:%s" % self.color
        self.complection_list.setStyleSheet(css)
        self.cmd.setStyleSheet(css)
        self.browser.setStyleSheet(css)


    def createUI(self):
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(self.complection_list)
        hbox.addWidget(self.browser)
        vboxCmd = QtGui.QVBoxLayout()
        vboxCmd.addWidget(self.cmd)
        vboxCmd.addLayout(hbox)
        self.setAutoFillBackground(True)
        self.setLayout(vboxCmd)
        self.setWindowModality(Qt.ApplicationModal)

    
    def getAllActions(self):
        allActions = self.actions + self.catsActions.keys()
        allActions.sort()
        return allActions
    
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.hide()
        return DialogBox.keyPressEvent(self, event)
    
    def show(self, text):
        self.selected_text = text
        return DialogBox.show(self)
    
    def showCompletion(self, text):
        self.complection_list.clear()
        actions = self.findActionsByString(text)
        for i in actions:
            item = QtGui.QListWidgetItem(self.complection_list)
            item.setText(i)
        self.complection_list.setCurrentItem(self.complection_list.item(0))
        self.setHelpText(actions[0])
    
    def findActionsByString(self, text):
        actions = None
        if not unicode(text).strip() == u"":
            pattern = re.compile(r'\b%s.*'%text)
            actions = [ i for i in self.getAllActions() if re.findall(pattern, i) ]
        return actions or self.getDefaultActions()
    
    def getDefaultActions(self):
        keys = self.catsActions.keys()
        keys.sort()
        return keys
    
    def delegateEvent(self, event, who):
        if isinstance(who, ListWidget):
            self.cmd.setFocus(Qt.ShortcutFocusReason)
            self.cmd.deselect()
            self.cmd.keyPressEvent(event)
        elif isinstance(who, Line):
            self.complection_list.setFocus(Qt.ShortcutFocusReason)
            self.complection_list.keyPressEvent(event)
    
    def selectFirst(self):
        text = self.complection_list.item(0).text()
        self.choose(text)

    def choose(self, text):
        self.cmd.setText(text)
        self.setHelpText(text)
    
    
    def setHelpText(self, choice):
        self.browser.clear()
        text = self.getHelpText(choice)
        self.browser.setHtml(text) 
         
    def getHelpText(self, choice):
        descr = getDescription(choice)
        cmd, params = self.parse_cmd()
        if not cmd == 'all' and params:
            return '%s => %s'%(descr, params)
        return descr

    def evaluate(self):
        cmd, params = self.parse_cmd()
        if cmd:
            event = ObservableEvent(ObservableEvent.execute, command=cmd, params=params)
            self.notifyObservers(event)
            self.hide()
        Observable.notifyObservers(self, event)
    
    def parse_cmd(self):
        cmd = unicode(self.cmd.text())
        f = self.re_pre_cmd.findall(cmd)
        if f:
            params = f[0][1] if f[0][1] else self.selected_text
            return f[0][0], params
        else:
            f = self.re_post_cmd.findall(cmd)
            if not f:
                return "", ""
            params = f[0][0] if f[0][0] else self.selected_text
            return f[0][1], params
    


    def onUpdate(self, event):
        if event.type == ObservableEvent.execute:
            self.onExecute(event)
        if event.type == ObservableEvent.selectTextEvent:
            text = event.getParam('text')
            self.choose(text)
            
    def onExecute(self, event):
        cmd, params = event.getParam('command'), event.getParam('params')
        action = self.catsActions.get(cmd)
        if action:
            action(params)
        if cmd.lower() not in ('all', 'search'):
            self.hide()
    
    def openUrl(self, url):
        QtGui.QDesktopServices.openUrl(QUrl(url))
    
    def google(self, *text):
        search_str = 'https://www.google.com/search?num=100&q=%s'%text[0]
        self.openUrl(search_str)
    
    def wikipedia(self, *text):
        self.openUrl('http://ru.wikipedia.org/w/index.php?search=%s'%text[0])
    
    def search(self, text):
        self.browser.setHtml("<a href='google.com'>%s</a>"%text)
    
    def showAllCommands(self, *text):
        self.showCompletion(self.getAllActions())
        
