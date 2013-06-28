# -*- coding: utf-8 -*-
'''
Created on 22.05.2012

@author: vb
'''
import os
from XMLFile.XML import XML
from xml.dom.minidom import getDOMImplementation
from MainFrame import Settings

class Keeper:
    def __init__(self):
        settings = os.path.join(Settings.USER_SETTINGS, "Keeper.xml")
        self.stateXML = XML(settings, self.createXML(), os.path.exists(settings))
    
    def createXML(self):
        impl = getDOMImplementation()
        xml = impl.createDocument(None, "State", None)
        lastOpen = xml.createElement('lastState') 
        root = xml.documentElement
        root.appendChild(lastOpen)
           
        return xml.toxml(encoding='utf-8')
        
    def getLastState(self):
        last = self.stateXML.getValueByTagName('lastState', 'value')
        return last
    
    def setLastState(self, last):
        self.stateXML.setValueByTagName('lastState', 'value', unicode(last))
        
               
    def update(self, message):
        pass
