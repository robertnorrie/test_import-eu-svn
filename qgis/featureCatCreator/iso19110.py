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
import urllib2
import xml.etree.ElementTree as etree


def getTemplateContent(templatePath):
    # is the template path an URL or a file system path?
    
    templateContent = None

    # testing if the path is empty
    if templatePath.trimmed().isEmpty():
        raise ValueError, "The text field specifying the template path is empty."
        
    # testing if the path is a file system path
    isAFileSystemPath = False
    isAFileUrlPath = False
    if os.path.exists(str(templatePath)):
        isAFileSystemPath = True
        
        file = open(str(templatePath), "r")
        
        try:
            templateContent = file.read()
            return templateContent
        finally:
            file.close()
            
    # try to retrieve the template from the web
    else:
        # retrieving the content of the file
        
        try:
            templateContent = urllib2.urlopen(str(templatePath)).read()
            isAFileUrlPath = True
            return templateContent
        except urllib2.URLError, e:
            isAFileUrlPath = False
    
    if not (isAFileSystemPath or isAFileUrlPath):
        raise ValueError, "The path of the template is not a valid file system path nor a valid URL."

    
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
        
        # updating the date of the feature catalog
        self.updateFcVersionDate()
    
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
        return etree.tostring(self.etDoc, encoding="utf-8")

    def save(self, filePath):
        file = open(filePath, 'w')
        file.write(etree.tostring(self.etDoc, encoding="utf-8"))
        file.close()

    def updateWithParams(self, params):
        # update the feature catalogue name, scope and version number
        self.setFcName(params["fc_name"])
        self.setFcScope(params["fc_scope"])
        self.setFcVersionNumber(params["fc_versionNumber"])
        
        # update the feature  type name and definition
        self.setFtName(params["ft_name"])
        self.setFtDefinition(params["ft_definition"])
        
        # update the fields/attributes
            
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


    def getFtName(self):
        ftName = self.etDoc.findall("./{%s}featureType/{%s}FC_FeatureType/{%s}typeName/{%s}LocalName" % (GFC_NS, GFC_NS, GFC_NS, GCO_NS))[0].text
        return ftName

    def setFtName(self, newName):
        ftNames = self.etDoc.findall("./{%s}featureType/{%s}FC_FeatureType/{%s}typeName/{%s}LocalName" % (GFC_NS, GFC_NS, GFC_NS, GCO_NS))
        if len(ftNames) != 1:
            self.cleanFtName()
            
        ftNames[0].text = newName

    def cleanFtName(self):
        pass

   
    def getFtDefinition(self):
        ftDefinition = self.etDoc.findall("./{%s}featureType/{%s}FC_FeatureType/{%s}definition/{%s}CharacterString" % (GFC_NS, GFC_NS, GFC_NS, GCO_NS))[0].text
        return ftDefinition

    def setFtDefinition(self, newScope):
        ftDefinitions = self.etDoc.findall("./{%s}featureType/{%s}FC_FeatureType/{%s}definition/{%s}CharacterString" % (GFC_NS, GFC_NS, GFC_NS, GCO_NS))
        if len(ftDefinitions) != 1:
            self.cleanFtDefinition()
            
        ftDefinitions[0].text = newScope

    def cleanFtDefinition(self):
        pass

