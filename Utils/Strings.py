# -*- coding: utf-8 -*-
'''
Created on Jul 11, 2012

@author: vb
'''

def getTranslate(s, lang="ru"):
    translations = {
                    "warehouseXML": "path to file", 
                    "browse": "Browse"
    }
    if translations.has_key(s):
        return translations[s]
    else:
        return "" 


def getDescription(s):
    s = unicode(s)
    return {        
        "google"          : "search in google", 
        "wikipedia"       : "search in wikipedia ru",
        "search"          : "search in your notes",
        "all"             : "show all commands",
        "insert table"    : "insert table row col",
        "column after"    : "insert column after current column",
        "column before"   : "insert column before current column",
        "row after"       : "insert row after current row",
        "row before"      : "insert row before current row",
        "delete column"   : "delete current column",
        "delete row"      : "delete current row",
        "bold"            : "bold",
        "underline"       : "underline",
        "italic"          : "italic",
        "orderer list"    : "insert orderer list",
        "unorderer list"  : "insert unorderer list",
        "highlight"       : "highlight selectet text",
        "horizontal rule" : "insert horizontal rule",
        "remove format"   : "remove format",
        "insert tag"      : "insert tag",
        "insert task"     : "insert task",
        "insert object"   : "insert link, image or file",
        "show in folder"  : "show current note in file sistem",
     }.get(s)
    