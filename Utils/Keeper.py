# -*- coding: utf-8 -*-
'''
Created on 22.05.2012

@author: vb
'''
import os
from XMLFile.XML import XML, createXmlWithRoot
from xml.dom.minidom import getDOMImplementation
from MainFrame import Settings

class Keeper:
    def __init__(self):
        settings = os.path.join(Settings.USER_SETTINGS, "Keeper.xml")
        defaultXml = createXmlWithRoot('State', 'lastState')
        self.stateXML = XML(settings, defaultXml, os.path.exists(settings))
    
    def getLastState(self):
        last = self.stateXML.getValueByTagName('lastState', 'value')
        return last
    
    def setLastState(self, last):
        self.stateXML.setValueByTagName('lastState', 'value', unicode(last))
        
               
    def update(self, message):
        pass
