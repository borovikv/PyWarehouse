'''
Created on 27.05.2012

@author: vb
'''
from XMLFile.XML import XML, XmlNames


class NavigationalXML(XML):
    
    def __init__(self, xml_file, xml_str=None, parseFromFile=False):
        XML.__init__(self, xml_file, xml_str, parseFromFile)
        root = self.getDocumentElement()
        self.elements = { XmlNames.rootName: root }
        self.initElements(root)
        

    def initElements(self, root):
        if root.hasChildNodes():
            nodeList = root.childNodes
            for node in nodeList:
                self.elements[self.getName(node)] = node
                self.initElements(node)

    def getName(self, node):
        return node.getAttribute(XmlNames.attributeName)

    

    def getCurrentElement(self, name):
        if name and self.elements.has_key(name):
            return self.elements[name]
        return self.getDocumentElement()

    def createElement(self, name, newName):
        name = unicode(name)
        newName = unicode(newName)

        newElem = XML.createElement(self, XmlNames.tagName)
        newElem.setAttribute(XmlNames.attributeName, newName)
        parent = self.getCurrentElement(name)
        parent.appendChild(newElem)
        self.save()
        self.elements[newName] = newElem
        
    
    def renameElement(self, oldName, newName):
        oldName = unicode(oldName)
        newName = unicode(newName)
        if self.elements.has_key(oldName):
            element = self.elements.pop(oldName)
            element.removeAttribute(XmlNames.attributeName)
            element.setAttribute(XmlNames.attributeName, newName)
            self.elements[newName] = element
    
    
    def deleteElement(self, name):
        name = unicode(name)
        if self.elements.has_key(name):
            element = self.elements.pop(name)
            parent = element.parentNode
            parent.removeChild(element)
            self.save()
        
    
    def move(self, parent, newChild, refChild=None):
        parent = self.elements.get(unicode(parent))
        newChild = self.elements.get(unicode(newChild))
        if refChild:
            refChild = self.elements.get(unicode(refChild))
        if parent and newChild:    
            parent.insertBefore(newChild, refChild)
    
    
    def getId(self):
        i = self.elements[XmlNames.rootName].getAttribute("id")
        if not i:
            return 0
        return int(i)
    
    def incrimentId(self):
        i = self.getId() + 1
        self.elements[XmlNames.rootName].setAttribute("id", str(i))
        self.save()

