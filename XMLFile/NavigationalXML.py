'''
Created on 27.05.2012

@author: vb
'''
from XMLFile.XML import XML, XmlNames


class NavigationalXML(XML):
    
    def __init__(self, xml_file, xml_str=None, is_str_defoalt=False):
        XML.__init__(self, xml_file, xml_str, is_str_defoalt)
        root = self.getDocumentElement()
        self.elements = {XmlNames.rootName: root}
        self.initElements(root)
        
    def initElements(self, root):
        if root.hasChildNodes():
            nodeList = root.childNodes
            for node in nodeList:
                self.elements[node.getAttribute(XmlNames.attributeName)] = node
                self.initElements(node)
    
    def createElement(self, parent_element, new_element):
        parent_element = unicode(parent_element)
        new_element = unicode(new_element)
        if parent_element:
            parent = self.elements[parent_element]
        else:
            parent = self.getDocumentElement()
            
        new = XML.createElement(self, XmlNames.tagName)
        new.setAttribute(XmlNames.attributeName, new_element)
        parent.appendChild(new)
        self.save()
        self.elements[new_element] = new
        
    def renameElement(self, old, new):
        old = unicode(old)
        new = unicode(new)
        element = self.elements.pop(old)
        element.removeAttribute(XmlNames.attributeName)
        element.setAttribute(XmlNames.attributeName, new)
        self.elements[new] = element
    
    def deleteElement(self, element):
        element = unicode(element)
        element = self.elements.pop(element)
        parent = element.parentNode
        parent.removeChild(element)
        self.save()
        
    
    def move(self, parent, newChild, refChild):
        parent = self.elements[unicode(parent)]
        newChild = self.elements[unicode(newChild)]
        if refChild:
            refChild = self.elements[unicode(refChild)]
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

