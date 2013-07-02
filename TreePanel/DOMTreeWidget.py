# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui;


from TreePanel.TreeDialog import TreeDialog;
from TreePanel.TreeModel import TreeModel;
from Utils.Events import ObservableEvent
from Utils.Keeper import Keeper
from Utils.QUtils import createQAction

class DOMTreeWidget(QtGui.QTreeView):
    def __init__(self, xmlFileName, actions=None, parent=None):
        QtGui.QTreeView.__init__(self, parent, headerHidden=True)
        
        self.actions = actions
        self.dialog = TreeDialog(self) 
        self.model = TreeModel(xmlFileName)
        self.currentItem = self.model.root
        self.setModel(self.model) 
        self.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        self.setDropIndicatorShown(True)
        self.showDropIndicator()
        
        self.clicked[QtCore.QModelIndex].connect(self.itemClick)  
        self.createMenu()
        

    def createMenu(self):        
        self.menu = QtGui.QMenu(self)
        self.menu.addAction( createQAction(self, 'add', self.addChild) )
        self.menu.addAction( createQAction(self, 'delete', self.deleteNode) )
        self.menu.addAction( createQAction(self, 'rename', self.renameNode) )
    
    ############################################################################
    #
    # EVENTS
    #
    ############################################################################
    def updateModel(self, newXML):
        self.model = TreeModel(newXML)
        self.setModel(self.model)
    
    def contextMenuEvent(self, event):
        self.menu.exec_(event.globalPos())
      
    def dropEvent(self, e):
        self.model.isDroped = True
        return QtGui.QTreeView.dropEvent(self, e)
    
    def mousePressEvent(self, e):
        index = self.indexAt(e.pos())
        item = self.model.itemFromIndex(index)
        if item:
            self.currentItem = item
        else:
            self.currentItem = self.model.root
        return QtGui.QTreeView.mousePressEvent(self, e)
    
    ############################################################################
    #
    # ACTIONS
    #
    ############################################################################
    # CLICK
    def itemClick(self):
        self.item = self.currentItem
        name = self.itemDataString(self.currentItem)
        self.callAction('open', name)
       
    # ADDCHILd
    def addChild(self):
        self.dialog.showDialog("")
        if self.dialog.hasResult():
            newItem = self.createNode(self.currentItem)
            self.callAction('add', self.itemDataString(newItem))

    def createNode(self, item):
        newItem = self.model.addChild(item, self.createName())
        self.model.incrimentId()
        self.scrollToItem(newItem)
        return newItem

    def createName(self):
        return self.dialog.getText() + '@' + str(self.model.getId())

    # DELETE
    def deleteNode(self):
        if self.currentItem == self.model.root:
            return
        self.callAction('delete', self.itemDataString(self.currentItem))
        self.model.deleteNode(self.currentItem)

    # RENAME
    def renameNode(self):
        if self.currentItem == self.model.root:
            return
        oldName, suffix, data = self.splitName(self.currentItem)
        self.dialog.showDialog(oldName)
        if self.dialog.hasResult():
            newName = self.dialog.getText() + suffix
            self.model.renameNode(self.currentItem, newName)
            self.callAction('rename', data, newName)

    def splitName(self, item):
        data = unicode(self.itemDataString(item))
        i = data.rfind('@')
        if i >= 0:
            suffix = data[i:]
        else:
            suffix = ''
        oldName = data[0:i]
        return oldName, suffix, data

    
    def callAction(self, name, *args, **kwargs):
        if self.actions:
            self.actions.call(name, *args, **kwargs)

    # UPDATE
    def onUpdate(self, event):
        isStartEvent = ( event.type == ObservableEvent.start 
                         and event.getParam(ObservableEvent.name))
        if isStartEvent:
            self.scrollToItem(event.getParam(ObservableEvent.name))
            
        isCloseEvent = ( event.type == ObservableEvent.close 
                         and hasattr(self, "item") )
        if isCloseEvent:
            keeper = Keeper()
            keeper.setLastState(self.getCurrentState())
    
    def getCurrentState(self):
        try:
            state = self.itemDataString(self.currentItem)
        except:
            state = ""
        return state

    
    def scrollToItem(self, item):
        if isinstance(item, (unicode, str)):
            item = self.model.getItemByStr(item)
        
        if item:
            index = item.index()
            self.scrollTo(index)
            self.setCurrentIndex(index)

    def getFirst(self):
        first = self.model.root.child(0)
        return first
    
    def itemDataString(self, item):
        return item.data().toString() 
