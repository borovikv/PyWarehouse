'''
Created on 27.05.2012

@author: vb
'''
class ObservableEvent:
    nodeName = "name"
    start = "Start"
    close = "Close"
    path = "path"
    name = "name"
    execute = "execute"
    
    def __init__(self, t, params = None):
        self.type = t
        self.params = params if params and isinstance(params, dict) else {}
    
    def setParam(self, name, value):
        self.params[name] = value
    
    def getParam(self, name):
        return self.params[name]
