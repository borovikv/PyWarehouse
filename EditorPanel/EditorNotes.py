'''
Created on Jun 28, 2013

@author: drifter
'''
import os
from EditorPanel.Editor import Editor
from Utils.Observable import ObservableEvent

class EditorNotes(Editor):    
    def __init__(self, notesFolder, parent = None):
        super(EditorNotes, self).__init__(notesFolder, parent)   
        self.operation = {
            'add': self.openDoc,
            'open': self.openDoc,
            'delete': self.deleteDoc, 
            'rename': self.rename,
        }     
    
    def call(self, name, *args, **kwargs):
        operation = self.operation.get(name)
        if operation:
            operation(*args, **kwargs)    
    
    
    def newDoc(self, name):
        self.openDoc(name)
        
    def openDoc(self, name):
        name = unicode(name)
        path = self.getPathByName(name)
        self.createFolders(path)
        if hasattr(self, 'path') and self.path:
            self.saveDoc()
        Editor.openDoc(self, path)
    
    def deleteDoc(self, name):
        name = unicode(name)
        path = os.path.join(self.notesFolder, name)
        Editor.deleteDoc(self, path)
    
    def rename(self, oldName, newName):
        oldName = unicode(oldName)
        newName = unicode(newName)
        Editor.rename(self, self.getPathByName(oldName), self.getPathByName(newName))
    
    def on_start(self, event):
        name = event.getParam(ObservableEvent.name)
        if not name:
            return
        self.openDoc(name)

    def getPathByName(self, name):
        return os.path.join(self.notesFolder, name, name + '.html')
    
    def createFolders(self, path):
        dirname = os.path.dirname(path)
        if not os.path.exists(dirname):
            os.mkdir(dirname)
    