'''
Created on 22.05.2012

@author: vb
'''
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
        
    
    
    def addChild(self, name):
        self.editorPanel.openDoc(name)
        
    def renameNode(self, oldPath, newPath):
        self.editorPanel.rename(oldPath, newPath)
             
    def itemClicked(self, name):
        self.editorPanel.openDoc(name)
        
    def deleteNode(self, name):
        self.editorPanel.deleteDoc(name)
        #self.editorPanel.openDoc()
        
    
        
