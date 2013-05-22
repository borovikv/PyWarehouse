from PyQt4 import QtGui, QtCore
#--------------------------------------------------------------------------------
from EditorPanel.Editor import Editor
from TreePanel.DOMTreeWidget import DOMTreeWidget
from Utils.Preferences import Preferences
from Utils.Observable import Observable
from Utils.Resources import Resources
from Utils.NavigatorActions import NavigatorActions
from Utils.Keeper import Keeper
from Utils.Events import ObservableEvent
from Dialogs.CatsDialog import CatsDialog

#--------------------------------------------------------------------------------

class Warehouse(QtGui.QWidget, Observable):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        Observable.__init__(self)
        self.preferences = Preferences(self)
        notesFolder = self.preferences.getNotesFolder()
        
        self.editorPanel = Editor(notesFolder, self)
        actions = NavigatorActions(self.editorPanel, notesFolder)
        self.treePanel = DOMTreeWidget(self.preferences.xmlPath, actions)
        
        Observable.registerObserver(self, self.treePanel)     
        Observable.registerObserver(self, self.editorPanel)
        
        self.makeInterface()
        
        self.catsDialog = CatsDialog(self.editorPanel.editor_actions.keys(), self)
        self.catsDialog.registerObserver(self.editorPanel)
        self.catsDialog.registerObserver(self.treePanel)
        act = QtGui.QAction(self)
        act.setShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_Space))
        act.triggered.connect(self.showDialog)
        self.addAction(act)
        self.start()
    
    def makeButton(self, name, icon, func):
        but = QtGui.QPushButton(icon, name)
        but.clicked.connect(func) 
        return but
       
    def makeInterface(self):
        self.setWindowTitle("Warehouse")
        self.setWindowIcon(Resources.getIcon(Resources.iconWindow))
        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
             
        self.hideButton = self.makeButton("", Resources.getIcon(Resources.iconArrowLeft), self.hideShow)
        self.prefButton = self.makeButton("", Resources.getIcon(Resources.iconPrefIcon), self.preferences.setPreferences) 
        
        vboxLeft = QtGui.QVBoxLayout()
        vboxLeft.addWidget(self.hideButton)
        vboxLeft.addWidget(self.prefButton)
        elements = self.editorPanel.getInterfacesElements()
        for e in elements:
            vboxLeft.addWidget(elements[e])
        vboxLeft.insertStretch(-1)
        
        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#        tab = QtGui.QTabWidget()
#        tab.addTab(QWidget, QString)
#        
        
        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        self.spliter = QtGui.QSplitter()
        self.spliter.addWidget(self.treePanel)
        self.spliter.addWidget((self.editorPanel))
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.spliter)
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        gbox = QtGui.QGridLayout()
        gbox.addLayout(vboxLeft, 0, 0)
        gbox.addLayout(vbox, 0, 1)
        self.setLayout(gbox)
        self.showMaximized()
        
    def showDialog(self):
        self.catsDialog.show(self.editorPanel.selectedText())
            
    def hideShow(self):
        secondPanel = self.spliter.children()[self.spliter.indexOf(self.treePanel)]
        firstPanel = self.spliter.children()[self.spliter.indexOf(self.editorPanel)]
        if firstPanel.width() != 0:
            self.navWidth = secondPanel.width()
            self.editWidth = firstPanel.width()

        if firstPanel.width() != 0:
            self.spliter.setSizes([0, self.navWidth + self.editWidth])
            self.hideButton.setIcon(Resources.getIcon(Resources.iconArrowRight))
        else:
            self.spliter.setSizes([self.editWidth, self.navWidth])
            self.hideButton.setIcon(Resources.getIcon(Resources.iconArrowLeft))
    
    def closeEvent(self, e):
        Observable.notifyObservers(self, ObservableEvent(ObservableEvent.close))

    def start(self):
        
        
        event = ObservableEvent(ObservableEvent.start)
        keeper = Keeper()
        lastState = keeper.getLastState()
        event.setParam(ObservableEvent.name, lastState)
        if lastState:
            path = self.preferences.getNotePath(lastState)
            event.setParam(ObservableEvent.path, path)
        else:
            event.setParam(ObservableEvent.path, "")
        Observable.notifyObservers(self, event)
    
    def restart(self):
        if not hasattr(self, "editorPanel"):
            return
        
        self.editorPanel.saveDoc()
        self.editorPanel.newDoc()
        actions = NavigatorActions(self.editorPanel, self.preferences.getNotesFolder())
        self.treePanel.updateModel(self.preferences.xmlPath, actions)
        
        

#------------------------------------------------------------------------------------------------

        
