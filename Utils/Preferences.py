'''
Created on 22.05.2012

@author: vb
'''
import os
from XMLFile.XML import XML
from xml.dom.minidom import getDOMImplementation
from PyQt4 import QtCore
from Dialogs.PreferencesDialog import PreferencesDialog
from Utils.Resources import Resources
from MainFrame import Settings

class Preferences:
            
    def __init__(self, parent=None):
        self.parent = parent
        self.preferencesDialog = PreferencesDialog(self, parent=parent)
        self.setXMLPath()
        self.notesFolder = os.path.dirname(unicode(self.xmlPath))
    
    
    def setPreferences(self):
        self.preferencesDialog.show_prep()
        self.preferencesDialog.exec_()
    
    def getNotePath(self, name):
        return os.path.join(unicode(self.notesFolder), name, name + ".html")
    
    def update(self):
        self.xmlPath = unicode(self.preferencesDialog.xmlPath)
        if self.xmlPath:
            self.settingsXML.setValueByTagName("XMLPath", "value", self.xmlPath)
            self.parent.restart()
    
    def getXmlPath(self):
        if hasattr(self, "xmlPath"):
            return self.xmlPath
        else:
            return ""
    #############################################################################################
    #                                                                                           #
    #                                         UTILS                                             #
    #                                                                                           #
    #############################################################################################
    def setXMLPath(self): 
        settings = os.path.join(Settings.USER_SETTINGS, "settings.xml")
        
        if not os.path.exists(settings):
            self.settingsXML = XML(settings, self.createSettings())
            self.xmlPath = ""
            self.setPreferences()
        else:
            self.settingsXML = XML(settings)
        
        xmlPath = self.settingsXML.getValueByTagName("XMLPath", "value")
        
        if not xmlPath or not os.path.exists(xmlPath):
            self.setPreferences()
        else:
            self.xmlPath = xmlPath
            
        return xmlPath
    
    def createSettings(self):
        impl = getDOMImplementation()
        xml = impl.createDocument(None, "Settings", None)
        settings = xml.documentElement
        w = xml.createElement("XMLPath")
        settings.appendChild(w)
           
        return xml.toxml(encoding='utf-8')    

    
    
