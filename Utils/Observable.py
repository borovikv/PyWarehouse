'''
Created on 22.05.2012

@author: vb
'''
class ObservableEvent:
    nodeName = "name"
    start = "Start"
    close = "Close"
    path = "path"
    name = "name"
    execute = "execute"
    selectTextEvent = 'selectText'
    keyPressEvent = 'keyPressEvent'
    
    def __init__(self, t, **params):
        self.type = t
        self.params = params
    
    def setParam(self, name, value):
        self.params[name] = value
    
    def getParam(self, name):
        return self.params[name]
    
class Observable:
    def __init__(self):
        self.observers = []
    
    def registerObserver(self, observer):
        self.observers.append(observer)
        
    def removeObserver(self, observer):
        pass
    def notifyObservers(self, event):
        for observer in self.observers:
            observer.onUpdate(event)
        
