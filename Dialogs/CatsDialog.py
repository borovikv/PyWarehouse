'''
Created on Jul 15, 2012

@author: vb
'''
from PyQt4 import QtGui
from PyQt4.QtCore import Qt, QUrl, QEvent
from Dialogs.Dialog import DialogBox
from Utils.Strings import getDescription
from Utils.Events import ObservableEvent
from Utils.Observable import Observable
import re


class CatsDialog(DialogBox, Observable):
    class Line(QtGui.QLineEdit):
        def __init__(self, items_list, parent=None):
            super(CatsDialog.Line, self).__init__(parent)
            self.items_list = items_list
            self.pattern_post = re.compile(r'(%s) .*'%('|'.join(items_list)))
            self.pattern_pre = re.compile(r'.* (%s)'%('|'.join(items_list)))
            
            
            #self.label = QtGui.QLabel(self)
            #self.label.setGeometry(5, 6 , self.width(), 15)
        
        def keyPressEvent(self, event):
            if event.key() in (Qt.Key_Up, Qt.Key_Down):
                self.parent().delegateEvent(event, self)
                event.ignore()
            elif event.key() in (Qt.Key_Return, Qt.Key_Enter):
                self.parent().evaluate()
            else:
                return QtGui.QLineEdit.keyPressEvent(self, event)       
        
        def keyReleaseEvent(self, event):
            if event.key() not in (Qt.Key_Return, Qt.Key_Enter):
                text = self.text().remove(self.selectedText())
                c = self.find_completion(text, self.items_list)
                self.parent().showCompletion(c)
            
            return QtGui.QLineEdit.keyReleaseEvent(self, event)
        
        def event(self, event):
            if ( event.type() in (QEvent.KeyPress, QEvent.KeyRelease) 
                 and event.key() == Qt.Key_Tab):
                self.parent().first()
                return True 
            return QtGui.QLineEdit.event(self, event)
        
        def find_completion(self, s, items):
            if s == "":
                return []
            
            pattern = re.compile(r'\b%s.*'%s)
            
            completion = []
            for i in items:
                if re.findall(pattern, i):
                    completion.append(i)
            if not completion:
                post = tuple(re.findall(self.pattern_post, s))
                pre = tuple(re.findall(self.pattern_pre, s))
                if post and pre:
                    completion = post + pre
                else:
                    completion = post or pre 
            return completion
        
    
    class ListWidget(QtGui.QListWidget):
        def __init__(self, parent=None): 
            super(CatsDialog.ListWidget, self).__init__(parent)  
            self.shortcut_focus = False
        
        def next(self):
            row = self.currentRow()
            row = row if row < self.count() - 1 else 0
            self.setCurrentRow(row)
               
        def prev(self):
            row = self.currentRow()
            row = row if row > 0 else self.count()
            self.setCurrentRow(row)
         
        def keyPressEvent(self, event):
            
            if self.shortcut_focus and event.key() == Qt.Key_Up:
                self.setCurrentRow(self.count() - 1)
                self.parent().choose(self.currentItem().text())
                self.shortcut_focus = False
            
            elif self.shortcut_focus and event.key() == Qt.Key_Down:
                self.setCurrentRow(0)
                self.parent().choose(self.currentItem().text())
                self.shortcut_focus = False 
            
            elif not self.shortcut_focus and event.key() in(Qt.Key_Up, Qt.Key_Down):
                QtGui.QListWidget.keyPressEvent(self, event)
                self.parent().choose(self.currentItem().text()) 
            
            elif event.key() in (Qt.Key_Enter, Qt.Key_Return):
                self.parent().choose(self.currentItem().text())   
                self.parent().delegateEvent(event, self)            
            
            else:
                self.parent().delegateEvent(event, self)
                event.ignore()
        
        def focusInEvent(self, event):
            self.shortcut_focus = event.reason() == Qt.ShortcutFocusReason
            if not self.shortcut_focus:
                self.parent().choose(self.currentItem().text()) 
            return QtGui.QListWidget.focusInEvent(self, event)
    ##############################################################################################
    #
    # Browser
    #
    ##############################################################################################
    class Browser(QtGui.QTextBrowser):
        def __init__(self, parent=None):
            super(CatsDialog.Browser, self).__init__()
    ##############################################################################################
    #
    # Initializing
    #
    ##############################################################################################
    def __init__(self, action_list, parent=None):
        width, height, color = 700, 400, "#aaa"
        DialogBox.__init__(self, width, height, color, parent)
        Observable.__init__(self)
        
        
        self.create_action_list(action_list)
        self.create_regexps(self.union_action_list)
        
        self.complection_list = CatsDialog.ListWidget(self)
        self.complection_list.setMaximumWidth(width*0.2)
        
        self.cmd = CatsDialog.Line(self.union_action_list, self)
        self.cmd.setFocus()    
        completer = QtGui.QCompleter(self.union_action_list)
        completer.setCompletionMode(QtGui.QCompleter.InlineCompletion)
        self.cmd.setCompleter(completer)
        self.browser = CatsDialog.Browser()
        self.browser.setFocusPolicy(Qt.NoFocus)
        
        css = "background-color:%s"%self.color
        self.complection_list.setStyleSheet(css)
        self.cmd.setStyleSheet(css)
        self.browser.setStyleSheet(css)
        
        

        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(self.complection_list)
        hbox.addWidget(self.browser)
        
        vboxCmd = QtGui.QVBoxLayout()
        vboxCmd.addWidget(self.cmd)
        vboxCmd.addLayout(hbox)
        self.setAutoFillBackground(True)
        self.setLayout(vboxCmd)
        self.setWindowModality(Qt.ApplicationModal)
    
    def create_action_list(self, action_list):
        self.action_list = action_list
        self.self_action_list = {
                                 "google": self.google, 
                                 "wikipedia": self.wikipedia,
                                 "search": self.search,
                                 "all": self.showAllCommands
                                 }
        self.union_action_list = self.action_list + self.self_action_list.keys()
        self.union_action_list.sort()
    
    def create_regexps(self, union_action_list):
        c = '|'.join(union_action_list)
        self.re_pre_cmd = re.compile(r'^(%s)\s*(.*)'%c)
        self.re_post_cmd = re.compile(r'^([^\s]*)\s+(%s)'%c)
    
    ##############################################################################################
    #
    # Events
    #
    ##############################################################################################
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.hide()
        return DialogBox.keyPressEvent(self, event)
    
    def show(self, text):
        self.selected_text = text
        return DialogBox.show(self)
    
    ##############################################################################################
    #
    # Interface for children components
    #
    ##############################################################################################
    
    def showCompletion(self, choices):
        self.complection_list.clear()
        if not choices:
            choices = self.get_default_list()
        for i in choices:
            item = QtGui.QListWidgetItem(self.complection_list)
            item.setText(i)
        self.complection_list.setCurrentItem(self.complection_list.item(0))
        self.cur_choice_display(choices[0])
    
    def delegateEvent(self, event, who):
        if isinstance(who, CatsDialog.ListWidget):
            self.cmd.setFocus(Qt.ShortcutFocusReason)
            self.cmd.deselect()
            self.cmd.keyPressEvent(event)
        elif isinstance(who, CatsDialog.Line):
            self.complection_list.setFocus(Qt.ShortcutFocusReason)
            self.complection_list.keyPressEvent(event)
    
    def choose(self, text):
        self.cmd.setText(text)
        self.cur_choice_display(text)
    
    def first(self):
        text = self.complection_list.item(0).text()
        self.choose(text)
    
    def cur_choice_display(self, choice):
        self.browser.clear()
        c = getDescription(choice) or ""
        self.browser.setHtml(self.parse_help(c)) 
         
    def evaluate(self):
        cmd, params = self.parse_cmd()
        if cmd and cmd in self.self_action_list:
            self.execute(cmd, params)
        elif cmd:
            event = ObservableEvent(ObservableEvent.execute, command=cmd, params=params)
            self.notifyObservers(event)
            self.hide()
    
    ##############################################################################################
    #
    # Utils
    #
    ##############################################################################################    
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
    
    def parse_help(self, text):
        cmd, params = self.parse_cmd()
        c = text + " " + params if self.has_params(cmd) else text
        return c
    
    def has_params(self, cmd):
        cmd = unicode(cmd).lower() 
        if cmd == 'all':
            return False
        elif cmd in self.self_action_list:
            return True
#        else:
#            return self.parent().has_params(cmd)
      
    def execute(self, cmd, params):
        self.self_action_list.get(cmd)(params)
        if cmd.lower() not in ('all', 'search'):
            self.hide()
 
         
    def get_default_list(self):
        keys = self.self_action_list.keys()
        keys.sort()
        return keys 
    
    def openUrl(self, url):
        QtGui.QDesktopServices.openUrl(QUrl(url))
    
    
    ##############################################################################################
    #
    # Self actions
    #
    ##############################################################################################    
    def google(self, *text):
        search_str = 'https://www.google.com/search?num=100&q=%s'%text[0]
        self.openUrl(search_str)
    
    def wikipedia(self, *text):
        self.openUrl('http://ru.wikipedia.org/w/index.php?search=%s'%text[0])
    
    def search(self, text):
        self.browser.setHtml("<a href='google.com'>%s</a>"%text)
    
    def showAllCommands(self, *text):
        self.showCompletion(self.union_action_list)
        
