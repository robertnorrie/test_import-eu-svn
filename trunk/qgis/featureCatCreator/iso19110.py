# -*- coding: utf-8 -*-

# This is a module dedicated to generating ISO19110 XML data
# given specific parameters.

# Namespaces used by iso 19110 docs
GFC_NS = "http://www.isotc211.org/2005/gfc"
GCO_NS = "http://www.isotc211.org/2005/gco"
XSI_NS = "http://www.w3.org/2001/XMLSchema-instance"

from PyQt4 import QtXml
from PyQt4 import QtCore

import os.path

def generateXML(templatePath, param):
    # Is the template path an URL or a file system path?

    # Testing if the path is empty
    if templatePath.trimmed().isEmpty():
        raise Exception, "The text field specifying the template path is empty."
        
    # Testing if the path is a file system path
    if os.path.exists(templatePath):
        return getTemplateContentFromFileSystemPath(templatePath)
    
    # Testing if the URL is valid
    else:
        qUrl = QtCore.QUrl(templatePath)
        if not qUrl.isValid():
            raise Exception, "The path of the template is not a valid URL."
        
        return getTemplateContentFromUrl(templatePath)
    
    return None


def getTemplateContentFromUrl(templateUrl):
    # Retrieving the content of the file
    import urllib2
    return urllib2.urlopen(templateUrl).read()

    
def getTemplateContentFromFileSystemPath(templateFileSystemPath):
    file = open(templateFileSystemPath, "r")
    templateContent = None
    
    try:
        templateContent = file.read()
    finally:
        file.close()
        
    return templateContent

    
class iso19110Doc:

    def __init__(self, templateContent, param):
        pass
        
    def getContent(self):
        return u""
        
    def updateFcName(self, newName):
        pass
        
    def updateFcScope(self, newScope):
        pass
        
    def updateFcVersionNumber(self, newVersionNumber):
        pass
        
        