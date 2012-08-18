'''
Created on 22.05.2012

@author: vb
'''
class Observable:
    def __init__(self):
        self.observers = []
    
    def registerObserver(self, observer):
        self.observers.append(observer)
        
    def removeObserver(self, observer):
        pass
    def notifyObservers(self, event):
        for observer in self.observers:
            observer.update(event)
        
