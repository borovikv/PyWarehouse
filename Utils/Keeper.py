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
        
        if not os.path.exists(settings):
            self.stateXML = XML(settings, self.createXML())
        else:
            self.stateXML = XML(settings)  
    
    def createXML(self):
        impl = getDOMImplementation()
        xml = impl.createDocument(None, "State", None)
        state = xml.documentElement
        lastOpen = xml.createElement('lastState') 
        state.appendChild(lastOpen)
           
        return xml.toxml(encoding='utf-8')
        
    def getLastState(self):
        last = self.stateXML.getValueByTagName('lastState', 'value')
        return last
    
    def setLastState(self, last):
        self.stateXML.setValueByTagName('lastState', 'value', unicode(last))
        
               
    def update(self, message):
        pass
