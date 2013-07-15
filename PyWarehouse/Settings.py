'''
Created on Jun 28, 2013

@author: drifter
'''
import os

PROJECT_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
ICONS = os.path.join(PROJECT_PATH, 'images')
USER_SETTINGS = os.path.join(PROJECT_PATH, "Settings")
PROXY = {}

        

def getPathToIcon(name):
    return os.path.join(ICONS, name + '.png')
