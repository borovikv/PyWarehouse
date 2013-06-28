'''
Created on 23.02.2012

@author: vb
'''
import codecs
from xml.dom.minidom import parse, parseString
import os

class XML:


    def __init__(self, xml_file, xml_str=None, parseFromFile=True):
        self.xml_file = xml_file
        
        if parseFromFile:
            self.parseWithDefault(xml_str)
        else:
            self.createXML(xml_str)
            
    def parseWithDefault(self, xml_str):
        try:
            self.xml = parse(self.xml_file)
        except:
            self.createXML(xml_str)

    def createXML(self, xmlStr):           
        self.xml = parseString(xmlStr)  
        self.save() 
        
    def save(self, dest=None):
        if not dest:
            dest = self.xml_file
        self.createXMLDir(dest)
        self.backupXML(dest)
        with codecs.open(dest, 'w', 'utf-8') as f:
            try:
                self.xml.writexml(f, encoding='utf-8')
            except:
                self.restoreXML(f)

    def createXMLDir(self, dest):
        dir_name = os.path.dirname(dest)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)


    def backupXML(self, dest):
        self.backup = None
        if os.path.exists(dest):
            self.backup = parse(dest)


    def restoreXML(self, xmlFile):
        if self.backup:
            self.backup.writexml(xmlFile, encoding='utf-8')

    def getValueByTagName(self, tag_name, attname, index=0):
        e = self.xml.getElementsByTagName(tag_name)[index]
        return e.getAttribute(attname)
    
    def setValueByTagName(self, tag_name, value_name, value, index=0):
        e = self.xml.getElementsByTagName(tag_name)[index]       
        e.setAttribute(value_name, value)
        self.save() 
        
    def removeAttribute(self, tag_name, value, index=0):
        e = self.xml.getElementsByTagName(tag_name)[index]
        try:
            e.removeAttribute(value)
        except:
            print 'error removeAttribute'
            
    def getDocumentElement(self):       
        return self.xml.documentElement    
  
    def createElement(self, tagName):
        return self.xml.createElement(tagName)
        
    
class XmlNames:
    attributeName = "path"
    tagName = "Thought"
    rootName = "Warehouse"
    splitChar = "@"    
        
