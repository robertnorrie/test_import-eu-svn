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
import xml.etree.ElementTree as etree


def getTemplateContent(templatePath):
    # is the template path an URL or a file system path?

    # testing if the path is empty
    if templatePath.trimmed().isEmpty():
        raise ValueError, "The text field specifying the template path is empty."
        
    # testing if the path is a file system path
    if os.path.exists(templatePath):
        return getTemplateContentFromFileSystemPath(str(templatePath))
    
    # try to retrieve the template from the web
    else:
        qUrl = QtCore.QUrl(templatePath)
        print qUrl
        print qUrl.isValid()
        if not qUrl.isValid():
            raise IOError, "The path of the template is not a valid URL."
        
        return getTemplateContentFromUrl(str(templatePath))
    
    return None


def getTemplateContentFromUrl(templateUrl):
    # retrieving the content of the file
    import urllib2
    templateContent = None
    
    try:
        templateContent = urllib2.urlopen(templateUrl).read()
    except urllib2.URLError, e:
        raise IOError, "The path of the template is not a valid URL."
    
    return templateContent

    
def getTemplateContentFromFileSystemPath(templateFileSystemPath):
    file = open(templateFileSystemPath, "r")
    templateContent = None
    
    try:
        templateContent = file.read()
    finally:
        file.close()
        
    return templateContent

    
class iso19110Doc:
    
    def __init__(self, templatePath):
        
        templateContent = getTemplateContent(templatePath)
        self.templateContent = templateContent.decode('utf-8')
        #print templateContent
        #self.templateContent = "sdfsfsdf"
        self.checkTemplateValidity()
        
        # using QtXml
        self.domDoc = QtXml.QDomDocument()
        self.domDoc.setContent(QtCore.QString(self.templateContent))
        
        # using etree
        self.etDoc = etree.fromstring(self.templateContent)
    
    def checkTemplateValidity(self):
        templateDomDoc = QtXml.QDomDocument()
        
        # check if the template is a valid XML document
        domParsingResult =  templateDomDoc.setContent(QtCore.QString(self.templateContent))
        if not domParsingResult[0]:
            raise IOError, "The selected iso19110 template is not a valid XML document (%s at line %d and column %d)" % (domParsingResult[1], domParsingResult[2], domParsingResult[3])
        
        # check the declaration of namespaces
        
        # check the presence and cardinality of required elements
        # gfc:FC_FeatureCatalogue
        
        # gfc:FC_FeatureCatalogue/gfc:producer
        
        pass
    
    def toString(self):
        #return self.domDoc.toString(2)
        return etree.tostring(self.etDoc)

    def updateWithParams(self, params):
        # update the feature catalogue name, scope and version number
        
        # update the feature  type name and definition
        
        # update the attributes
            
            # update the type, definition and cardinality of the attribute
            
            # update the listed values of the attribute
        
        pass


    def getFcName(self):
        fcName = self.etDoc.findall("./{%s}name/{%s}CharacterString" % (GFC_NS, GCO_NS))[0].text
        return fcName

    def setFcName(self, newName):
        fcNames = self.etDoc.findall("./{%s}name/{%s}CharacterString" % (GFC_NS, GCO_NS))
        if len(fcNames) != 1:
            self.cleanFcName()
            
        fcNames[0].text = newName

    def cleanFcName(self):
        pass

   
    def getFcScope(self):
        fcScope = self.etDoc.findall("./{%s}scope/{%s}CharacterString" % (GFC_NS, GCO_NS))[0].text
        return fcScope

    def setFcScope(self, newScope):
        fcScopes = self.etDoc.findall("./{%s}scope/{%s}CharacterString" % (GFC_NS, GCO_NS))
        if len(fcScopes) != 1:
            self.cleanFcScope()
            
        fcScopes[0].text = newScope

    def cleanFcScope(self):
        pass


    def getFcVersionNumber(self):
        fcVersion = self.etDoc.findall("./{%s}versionNumber/{%s}CharacterString" % (GFC_NS, GCO_NS))[0].text
        return fcVersion

    def setFcVersionNumber(self, newVersionNumber):
        fcVersions = self.etDoc.findall("./{%s}versionNumber/{%s}CharacterString" % (GFC_NS, GCO_NS))
        if len(fcVersions) != 1:
            self.cleanFcVersionNumber()
            
        fcVersions[0].text = newVersionNumber

    def cleanFcVersionNumber(self):
        pass


    def updateFcVersionDate(self):
        fcDates = self.etDoc.findall("./{%s}versionDate" % (GFC_NS))
        if len(fcDates) != 1:
            self.cleanFcVersionDate()
        
        # remove all child elements
        dateValues = fcDates[0].getchildren()
        for dateValue in dateValues:
            fcDates[0].remove(dateValue)
            
        # set the new value
        import datetime
        today = datetime.date.today()
        format = "%Y-%m-%d"        
        newDateNode = etree.SubElement(fcDates[0], "{%s}%s" % (GCO_NS, "Date"))
        newDateNode.text = today.strftime(format)
        
    def cleanFcVersionDate(self):
        pass

