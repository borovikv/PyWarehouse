from PyQt4 import QtGui, QtCore
#--------------------------------------------------------------------------------
from EditorPanel.Editor import Editor
from TreePanel.DOMTreeWidget import DOMTreeWidget
from Utils.Preferences import Preferences
from Utils.Observable import Observable
from Utils.NavigatorActions import NavigatorActions
from Utils.Keeper import Keeper
from Utils.Events import ObservableEvent
from Dialogs.CatsDialog import CatsDialog
from Utils.QUtils import makeButton, getShortcut, addShortcutAction, Icon

#--------------------------------------------------------------------------------

class Warehouse(QtGui.QWidget, Observable):
    
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        Observable.__init__(self)
        
        self.preferences = Preferences(self)
        notesFolder = self.preferences.notesFolder
                
        self.editorPanel = Editor(notesFolder, self)
        actions = NavigatorActions(self.editorPanel, notesFolder)
        self.treePanel = DOMTreeWidget(self.preferences.xmlPath, actions)
        
        self.registerObserver(self.treePanel)     
        self.registerObserver(self.editorPanel)

        self.catsDialog = CatsDialog(self.editorPanel.getActions(), self)
        self.catsDialog.registerObserver(self.editorPanel)
        self.catsDialog.registerObserver(self.treePanel)
        addShortcutAction(self, getShortcut('CTRL', 'SPACE'), self.showDialog)
        
        self.makeInterface()
        self.start()

    def makeInterface(self):
        self.setWindowTitle("Warehouse")
        self.setWindowIcon(Icon(Icon.window))
        
        self.hideButton = makeButton("", Icon(Icon.arrowLeft), self.hideShow)
        self.prefButton = makeButton("", Icon(Icon.preferences), self.preferences.setPreferences) 
        showInFolderBut = makeButton('', Icon(Icon.openFolder), 
                                     self.editorPanel.getAction('show in folder'))
        
        gbox = QtGui.QGridLayout()
        # Button Panel
        vboxLeft = QtGui.QVBoxLayout()
        vboxLeft.addWidget(self.hideButton)
        vboxLeft.addWidget(self.prefButton)
        if showInFolderBut:
            vboxLeft.addWidget(showInFolderBut)
        vboxLeft.insertStretch(-1)
        gbox.addLayout(vboxLeft, 0, 0)
        
        # Tree and editor panel
        self.spliter = QtGui.QSplitter()
        self.spliter.addWidget(self.treePanel)
        self.spliter.addWidget((self.editorPanel))
        vboxRight = QtGui.QVBoxLayout()
        vboxRight.addWidget(self.spliter)
        gbox.addLayout(vboxRight, 0, 1)

        self.setLayout(gbox)
        self.showMaximized()
        
    def showDialog(self):
        self.catsDialog.show(self.editorPanel.selectedText())
            
    def hideShow(self):
        if self.treePanel.width() != 0:
            self.hideTrePanel()
        else:
            self.showTreePanel()

    def hideTrePanel(self):
        self.navWidth = self.treePanel.width()
        self.editWidth = self.editorPanel.width()
        self.spliter.setSizes([0, self.navWidth + self.editWidth])
        self.hideButton.setIcon(Icon(Icon.arrowRight))

    def showTreePanel(self):
        self.spliter.setSizes([self.navWidth, self.editWidth])
        self.hideButton.setIcon(Icon(Icon.arrowLeft))
    
    def start(self):
        keeper = Keeper()
        lastState = keeper.getLastState()
        event = ObservableEvent(ObservableEvent.start, name=lastState)
        self.notifyObservers(event)
    
    def closeEvent(self, e):
        self.notifyObservers(ObservableEvent(ObservableEvent.close))

    def restart(self):
        if not hasattr(self, "editorPanel"):
            return
        self.editorPanel.saveDoc()
        actions = NavigatorActions(self.editorPanel, self.preferences.notesFolder)
        self.treePanel.updateModel(self.preferences.xmlPath, actions)
        
        

#------------------------------------------------------------------------------------------------

        
