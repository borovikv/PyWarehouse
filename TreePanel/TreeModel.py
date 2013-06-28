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

    def createDefaultXml(self):
        return "<" + XmlNames.rootName + " />"

    def __init__(self, xmlFileName, parent=None):
        QtGui.QStandardItemModel.__init__(self, parent)
        
        self.xml = NavigationalXML(xmlFileName, self.createDefaultXml())
        self.root = self.invisibleRootItem()
        self.isDroped = False
        self.fillModel(self.root, self.xml.getDocumentElement())
        self.itemChanged.connect(self.onItemChanged)
        
    
    def fillModel(self, root, xmlRoot): 
        if xmlRoot.hasChildNodes():
            nodeList = xmlRoot.childNodes
            for node in nodeList:
                name = node.getAttribute(XmlNames.attributeName)
                item = self.createItem(name)
                root.appendRow(item)
                self.fillModel(item, node)
    
    def createItem(self, attr):
        item = QtGui.QStandardItem()
        item.setText(self.getName(attr))
        item.setData(attr)
        return item
    
    def onItemChanged(self, item):
        if self.isDroped:
            self.move(item)
            self.isDroped = False
        self.saveChange()
    

    def move(self, item):
        parentItem = self.getParent(item)
        refChild = self.getRefChild(item, parentItem)
        _ = self.itemDataString
        self.xml.move(_(parentItem), _(item), _(refChild))

    
    def getParent(self, item):
        parentItem = item.parent()
        if not parentItem:
            parentItem = self.root
        return parentItem


    def getRefChild(self, item, parentItem):
        row = item.row() + 1
        isCurrentItemLast = row == parentItem.rowCount()
        if isCurrentItemLast: 
            # insert at the end of the children’s list
            return None
        else:
            return parentItem.child(row)

        
    def addChild(self, parent, attrValue):
        self.xml.createElement(self.itemDataString(parent), attrValue)
        item = self.createItem(attrValue)
        parent.appendRow(item)    
        return item   
       
    def deleteNode(self, item):  
        if item == self.root:
            return
        self.xml.deleteElement(self.itemDataString(item))
        parent = self.getParent(item)
        parent.removeRow(item.index().row())
            
    def renameNode(self, item, newAttrValue):
        if item == self.root:
            return
        self.xml.renameElement(self.itemDataString(item), newAttrValue)
        item.setData(newAttrValue) 
        item.setText(self.getName(newAttrValue))
    

    def getItemByStr(self, name, parent=None):
        parent = parent or self.root
        if parent.hasChildren():
            return self.search(name, parent)
        
    def search(self, name, parent):
        for j in range(parent.rowCount()):
            child = parent.child(j)
            if self.itemDataString(child) == name:
                return child
        return self.getItemByStr(name, child)
    
    
    def getId(self):
        return self.xml.getId()
        
    def incrimentId(self):
        self.xml.incrimentId()
        
    def saveChange(self, xml=None):
        self.xml.save()

    def itemDataString(self, item):
        if not item:
            return
        if item == self.root:
            return XmlNames.rootName
        try:
            return item.data().toString()
        except:
            print "item data model"
            return ''
    
    def getName(self, strName):
        strName = unicode(strName)
        end = strName.rfind("@")
        if end > 0:
            return strName[0:end]
        else:
            return strName
    
    
        
        
       
        
        
