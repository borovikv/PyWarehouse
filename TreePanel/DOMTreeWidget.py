# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui;


from TreePanel.TreeDialog import TreeDialog;
from TreePanel.TreeModel import TreeModel;
from Utils.Events import ObservableEvent
from Utils.Keeper import Keeper

class DOMTreeWidget(QtGui.QTreeView):
    def __init__(self, xmlFileName, actions=None, parent=None):
        QtGui.QTreeView.__init__(self, parent, headerHidden=True)
        
        self.actions = actions
        self.dialog = TreeDialog(self) 
        self.model = TreeModel(xmlFileName)
        self.setModel(self.model) 
        self.clicked[QtCore.QModelIndex].connect(self.itemClick)  
        self.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        self.setDropIndicatorShown(True)
        self.showDropIndicator()
        
        self.createMenu()
        
    def updateModel(self, newXML):
        self.model = TreeModel(newXML)
        self.setModel(self.model)
    
    def createMenu(self):        
        addAction = QtGui.QAction('add', self)
        addAction.triggered.connect(self.addChild)
        
        deleteAction = QtGui.QAction('delete', self)
        deleteAction.triggered.connect(self.deleteNode)
        
        renameAction = QtGui.QAction("rename", self)
        renameAction.triggered.connect(self.renameNode)
        
        self.menu = QtGui.QMenu(self)
        self.menu.addAction(addAction)
        self.menu.addAction(renameAction)
        self.menu.addAction(deleteAction)
    
    ###############################################################################################
    #
    # EVENTS
    #
    ###############################################################################################
    
    def contextMenuEvent(self, event):
        self.menu.exec_(event.globalPos())
      
    def dropEvent(self, e):
        self.model.isDroped = True
        return QtGui.QTreeView.dropEvent(self, e)
    
    def mousePressEvent(self, e):
        index = self.indexAt(e.pos())
        item = self.model.itemFromIndex(index)
        if item:
            self.curent_item = item
        else:
            self.curent_item = self.model.root
        return QtGui.QTreeView.mousePressEvent(self, e)
    
    ###############################################################################################
    #
    # ACTIONS
    #
    ###############################################################################################
       
    def addChild(self):
        item = self.curent_item
        self.dialog.showDialog("")
        
        if self.dialog.result() == self.dialog.Accepted and self.dialog.getTextToFind() != "":
            newItem = self.model.addChild(item,
                                          self.dialog.getTextToFind() + '@' + str(self.model.getId()))
            self.model.incrimentId()
            self.scrollToItem(newItem)
            
            if self.actions:
                self.actions.call('add', newItem.data().toString())
          
    def deleteNode(self):
        item = self.curent_item
        if item == self.model.root:
            return
        
        self.actions.call('delete', self.item_data(item))
        self.model.deleteNode(item)
          
    def renameNode(self):
        item = self.curent_item
        if item == self.model.root:
            return
        
        data = unicode(self.item_data(item))
        i = data.rfind('@')
        if i >= 0:
            suffix = data[i:]
        else:
            suffix = ''
        
        oldPath = data[0:i]
        self.dialog.showDialog(oldPath)
        if self.dialog.result() == self.dialog.Accepted and self.dialog.getTextToFind() != "":
            value = self.dialog.getTextToFind() + suffix
            self.model.renameNodeAttribute(item, value)
            self.actions.call('rename', data, self.item_data(item))
            
    def itemClick(self):
        self.item = self.curent_item 
        name = self.item_data(self.item)
        self.actions.call('open', name)
              
    def update(self, event):
        if event.type == ObservableEvent.start and event.getParam(ObservableEvent.name):
            self.scrollToItem(event.getParam(ObservableEvent.name))
            
        if event.type == ObservableEvent.close and hasattr(self, "item"):
            keeper = Keeper()
            try:
                state = self.item_data(self.item)
            except:
                state = ""
            #print unicode(state, 'utf-8')
            keeper.setLastState(state)
    
    ###############################################################################################
    #
    # UTILS
    #
    ###############################################################################################
    def scrollToItem(self, item):
        if isinstance(item, (unicode, str)):
            item = self.model.getItemFromStr(item)
        
        if item:
            index = item.index()
            self.scrollTo(index)
            self.setCurrentIndex(index)

    def getFirst(self):
        first = self.model.root.child(0)
        return first
    
    def item_data(self, item):
        return item.data().toString() 
