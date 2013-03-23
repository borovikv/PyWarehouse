'''
Created on 22.05.2012

@author: vb
'''
from PyQt4 import QtGui
import os
class Resources:
    iconWindow = "Icon"
    iconArrowLeft = "arrowLeft"
    iconArrowRight = "arrowRight"
    iconPrefIcon = "preferences-icon"
    iconEdit = "Edit"
    iconOpenFolder = "Show"
    
    @staticmethod
    def getMainFolder(): 
        _dir = os.path.dirname
        main_folder = _dir(_dir(__file__))
        return main_folder
    
    
    @staticmethod
    def getIcon(name):
        path = os.path.join(Resources.getImageFolderPath(), name + ".png")
        icon = QtGui.QIcon(path)
        return icon
    
    @staticmethod
    def getSourcesFolderPath():
        return os.path.join(Resources.getMainFolder(), "EditorPanel", "_source")
    
    @staticmethod
    def getSource(name):
        return os.path.join(Resources.getSourcesFolderPath(), name)
        
    
    @staticmethod
    def getImageFolderPath():
        return os.path.join(Resources.getMainFolder(), "images")
    
    @staticmethod
    def getSettingsFolderPath():
        return os.path.join(Resources.getMainFolder(), "Settings")
    
    @staticmethod
    def getScriptsFolder():
        return os.path.join(Resources.getMainFolder(), "EditorPanel", "JScripts")
    
    @staticmethod
    def getStylesFolder():
        return os.path.join(Resources.getMainFolder(), "EditorPanel", "Styles")
    
    
    #####################################################################################################
    #
    #                                          UTILS
    #
    #####################################################################################################
    @staticmethod
    def getPathToImg(imgName):
        return os.path.join(Resources.getImageFolderPath(), imgName)
    

    
    
    
    
    
