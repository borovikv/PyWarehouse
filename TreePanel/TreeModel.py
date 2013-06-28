# -*- coding: utf-8 -*-
'''
Created on 10.01.2012

@author: vb
'''
from PyQt4.QtGui import QStandardItemModel;
from PyQt4 import QtGui
from XMLFile.NavigationalXML import NavigationalXML 
from XMLFile.XML import XmlNames


class TreeModel(QStandardItemModel):  
    def __init__(self, xmlFileName, parent=None):
        QtGui.QStandardItemModel.__init__(self, parent)
        
        self.xml = NavigationalXML(xmlFileName, "<" + XmlNames.rootName + " />", True)
        self.root = self.invisibleRootItem()
        self.isDroped = False
        
        self.fillModel(self.root, self.xml.getDocumentElement())
        self.itemChanged.connect(self.onItemChanged)
        
    
    def fillModel(self, root, xmlRoot):        
        if xmlRoot.hasChildNodes():
            nodeList = xmlRoot.childNodes
            for node in nodeList:
                path = node.getAttribute(XmlNames.attributeName)
                item = self.createItem(path)
                root.appendRow(item)
                self.fillModel(item, node)
    
    ###############################################################################################
    #
    # PUBLIC METHODS
    #
    ###############################################################################################
                
    def addChild(self, parent, attrValue):
        self.xml.createElement(self.item_data(parent), attrValue)
        item = self.createItem(attrValue)
        parent.appendRow(item)    
        return item   
       
    def deleteNode(self, item):  
        if item == self.root:
            return
        
        self.xml.deleteElement(self.item_data(item))
        parent = item.parent()
        if not parent:
            parent = self.root
        parent.removeRow(item.index().row())
            
    def renameNodeAttribute(self, item, newAttrValue):
        if item == self.root:
            return
        
        self.xml.renameElement(self.item_data(item), newAttrValue)
        item.setData(newAttrValue) 
        item.setText(self.getName(newAttrValue))
    
    def getItemFromStr(self, name, parent=None):
        if not parent:
            parent = self.root
        
        node = None
        if parent.hasChildren():
            for j in range(parent.rowCount()):
                child = parent.child(j)
                if self.item_data(child) == name:
                    return child
                
                node = self.getItemFromStr(name, child)
                if node:
                    return node
        
        return node
    
    def getId(self):
        return self.xml.getId()
        
    def incrimentId(self):
        self.xml.incrimentId()
    ###############################################################################################
    #
    # EVENTS
    #
    ###############################################################################################
    
    def onItemChanged(self, item):
        if self.isDroped:
            self.move(item)
            self.isDroped = False
            
        self.saveChange()
        
    ###############################################################################################
    #
    # UTILS
    #
    ###############################################################################################
        
    def saveChange(self, xml=None):
        self.xml.save()
    
    def move(self, item):
        parentItem = item.parent()
        if not parentItem:
            parentItem = self.root
            parent = XmlNames.rootName
        else:
            parent = self.item_data(parentItem)
        
        newChild = self.item_data(item)
        
        row = item.row()
        if row + 1 == parentItem.rowCount():
            refChild = None
        else:
            refChild = self.item_data(parentItem.child(row + 1))
        
        self.xml.move(parent, newChild, refChild)
        
    def item_data(self, item):
        return item.data().toString()
    
    def getName(self, strName):
        strName = unicode(strName)
        end = strName.rfind("@")
        if end > 0:
            return strName[0:end]
        else:
            return strName
    
    def createItem(self, attr):
        item = QtGui.QStandardItem()
        item.setText(self.getName(attr))
        item.setData(attr)
        return item
        
        
       
        
        
