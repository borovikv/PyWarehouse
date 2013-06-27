'''
Created on 22.05.2012

@author: vb
'''
import os
import shutil


class NavigatorActions:

    def __init__(self, editor, notesFolder):
        '''
        Constructor
        '''
        self.notesFolder = notesFolder
        self.editorPanel = editor
        actions = {}
        actions["addChild"] = self.addChild
        actions["renameNode"] = self.renameNode
        actions["itemClick"] = self.itemClicked
        actions["deleteNode"] = self.deleteNode
        
    
    
    def addChild(self, path):
        path = self.getFoolPath(path)
        dirname = os.path.dirname(path)
        os.mkdir(dirname)
        
        if hasattr(self.editorPanel, 'path') and self.editorPanel.path:
            self.editorPanel.saveDoc()
        self.editorPanel.openDoc(path)
        
    def renameNode(self, oldPath, newPath):
        self.editorPanel.rename(oldPath, newPath)
             
    def itemClicked(self, path):
        self.editorPanel.saveDoc()
        self.editorPanel.openDoc(self.getFoolPath(path))
        self.lastOpen = path
        
    def deleteNode(self, item):
        self.editorPanel.deleteDoc(unicode(item))
        #self.editorPanel.openDoc()
        
    
    #####################################################################################################
    #
    #                                          UTILS
    #
    #####################################################################################################
    def getFoolPath(self, path):
        path = unicode(path)
        return os.path.join(self.notesFolder, path, path + ".html")
    
        
