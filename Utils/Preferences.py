'''
Created on 22.05.2012

@author: vb
'''
import os
from XMLFile.XML import XML, createXmlWithRoot
from xml.dom.minidom import getDOMImplementation
from Dialogs.PreferencesDialog import PreferencesDialog
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
        preferences = os.path.join(Settings.USER_SETTINGS, "preferences.xml")
        
        if not os.path.exists(preferences):
            self.settingsXML = XML(preferences, createXmlWithRoot('preferences', 'XMLPath'))
            self.xmlPath = ""
            self.setPreferences()
        else:
            self.settingsXML = XML(preferences)
        
        xmlPath = self.settingsXML.getValueByTagName("XMLPath", "value")
        
        if not xmlPath or not os.path.exists(xmlPath):
            self.setPreferences()
        else:
            self.xmlPath = xmlPath
            
        return xmlPath
    
    
    
