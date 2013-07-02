# -*- coding: utf-8 -*-
'''
Created on Jul 11, 2012

@author: vb
'''

def getTranslate(s, lang="ru"):
    translations = {
                    "warehouseXML": "path to file", 
                    "browse": "Browse",
                    "close": "Close"
    }
    if translations.has_key(s):
        return translations[s]
    else:
        return "" 


