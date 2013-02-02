'''
Created on 22.05.2012

@author: vb
'''
import os
import shutil


class NavigatorActions:

    def __init__(self, editor, workFolder):
        '''
        Constructor
        '''
        self.workFolder = workFolder
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
        self.editorPanel.newDoc(path)
        #self.editorPanel.saveDoc(path)
        #self.editorPanel.setPath(path)
        
    def renameNode(self, oldPath, newPath):
        self.editorPanel.rename(oldPath, newPath)
             
    def itemClicked(self, path):
        self.editorPanel.saveDoc()
        self.editorPanel.openDoc(self.getFoolPath(path))
        self.lastOpen = path
        
    def deleteNode(self, item):
        shutil.rmtree(os.path.join(self.workFolder, unicode(item)))
        self.editorPanel.newDoc()
        
    
    #####################################################################################################
    #
    #                                          UTILS
    #
    #####################################################################################################
    def getFoolPath(self, path):
        path = unicode(path)
        return os.path.join(self.workFolder, path, path + ".html")
    
        
