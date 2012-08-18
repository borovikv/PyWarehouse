'''
Created on 23.02.2012

@author: vb
'''
import codecs
from xml.dom.minidom import parse, parseString
import os

class XML:
    def __init__(self, xml_file, xml_str=None, is_str_defoalt=False):
        self.xml_file = xml_file
        
        if not xml_str and not is_str_defoalt:
            self.xml = parse(self.xml_file)
        elif xml_str and is_str_defoalt:
            try:
                self.xml = parse(self.xml_file)
            except:
                self.createXML(xml_str)
        else:
            self.createXML(xml_str)
            
        
    def save(self, dest=None):
        if not dest:
            dest = self.xml_file
        
        black_box_xml = None
        if os.path.exists(dest):
            black_box_xml = parse(dest)
        dir_name = os.path.dirname(dest)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        with codecs.open(dest, 'w', 'utf-8') as f:
            try:
                self.xml.writexml(f, encoding='utf-8')
                f.close() 
            except:
                if black_box_xml:
                    black_box_xml.writexml(f, encoding='utf-8')
            
    def createXML(self, xmlStr):           
        self.xml = parseString(xmlStr)  
        self.save() 
      
    def getValueByTagName(self, tag_name, attname, index=0):
        e = self.xml.getElementsByTagName(tag_name)[index]
        value = e.getAttribute(attname)
        return value
    
    def setValueByTagName(self, tag_name, value_name, value, index=0):
        e = self.xml.getElementsByTagName(tag_name)[index]       
        e.setAttribute(value_name, value)
        self.save() 
        
    def removeAttribute(self, tag_name, value, index=0):
        e = self.xml.getElementsByTagName(tag_name)[index]
        try:
            e.removeAttribute(value)
        except:
            print("MainFrame.preparation() except")
            
    def getDocumentElement(self):       
        return self.xml.documentElement    
  
    def createElement(self, tagName):
        return self.xml.createElement(tagName)
        
    
    
        
