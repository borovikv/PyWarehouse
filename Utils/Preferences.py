'''
Created on 22.05.2012

@author: vb
'''
import os
from XMLFile.XML import XML, createXmlWithRoot
from Dialogs.PreferencesDialog import PreferencesDialog
from PyWarehouse import Settings

class Preferences:
            
    def __init__(self, parent=None):
        self.path = os.path.join(Settings.USER_SETTINGS, "preferences.xml")
        self.parent = parent
        self.preferencesDialog = PreferencesDialog(self, parent=parent)
        self.setXMLPath()
        self.notesFolder = os.path.dirname(unicode(self.xmlPath))
    
    def setXMLPath(self): 
        self.preferences = self.getPreferencesXml()
        self.xmlPath = self.preferences.getValueByTagName("XMLPath", "value")
        if not self.xmlPath or not os.path.exists(self.xmlPath):
            self.xmlPath = ''
            self.setPreferences()

    def getPreferencesXml(self):
        defaultXml = createXmlWithRoot('preferences', 'XMLPath')
        fromFile = os.path.exists(self.path)
        return XML(self.path, defaultXml, fromFile)
    
    def setPreferences(self):
        self.preferencesDialog.show_prep()
        self.preferencesDialog.exec_()
    
    def update(self):
        xmlPath = unicode(self.preferencesDialog.xmlPath)
        if xmlPath:
            self.xmlPath = xmlPath
            self.preferences.setValueByTagName("XMLPath", "value", self.xmlPath)
            self.parent.restart()
    
    
    
