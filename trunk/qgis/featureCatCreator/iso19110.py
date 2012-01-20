# -*- coding: utf-8 -*-

# This is a module dedicated to generating ISO19110 XML data
# given specific parameters.

# Namespaces used by iso 19110 docs
GFC_NS = "http://www.isotc211.org/2005/gfc"
GCO_NS = "http://www.isotc211.org/2005/gco"
GML_NS = "http://www.opengis.net/gml"
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
        
        # remove fields not present in param
        self.removeExtraFields(params["fields"])
        
        # update the fields/attributes
        for field in params["fields"]:
            self.updateField(field)
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
        
        if isinstance(newName, QtCore.QString):
            fcNames[0].text = unicode(newName)
        else:
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
            
        if isinstance(newScope, QtCore.QString):
            fcScopes[0].text = unicode(newScope)
        else:
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
            
        if isinstance(newVersionNumber, QtCore.QString):
            fcVersions[0].text = unicode(newVersionNumber)
        else:
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
            
        if isinstance(newName, QtCore.QString):
            ftNames[0].text = unicode(newName)
        else:
            ftNames[0].text = newName

    def cleanFtName(self):
        pass

   
    def getFtDefinition(self):
        ftDefinition = self.etDoc.findall("./{%s}featureType/{%s}FC_FeatureType/{%s}definition/{%s}CharacterString" % (GFC_NS, GFC_NS, GFC_NS, GCO_NS))[0].text
        return ftDefinition

    def setFtDefinition(self, newDefinition):
        ftDefinitions = self.etDoc.findall("./{%s}featureType/{%s}FC_FeatureType/{%s}definition/{%s}CharacterString" % (GFC_NS, GFC_NS, GFC_NS, GCO_NS))
        if len(ftDefinitions) != 1:
            self.cleanFtDefinition()
            
        if isinstance(newDefinition, QtCore.QString):
            ftDefinitions[0].text = unicode(newDefinition)
        else:
            ftDefinitions[0].text = newDefinition

    def cleanFtDefinition(self):
        pass


    def cleanFt(self):
        # Remove extra typeName
        # Remove extra definition
        # Remove extra isAbstract

        # For each carrierOfCharacteristics
        
            # Remove extra FC_FeatureAttribute
            
        # For each FC_FeatureAttribute
        
            # Remove extra memberName
            # Remove extra definition
            # Remove extra cardinality
            # Remove extra valueType
        pass

    def removeExtraFields(self, paramFields):
        # List of the field names in the paramField parameter
        fieldNamesInParams = [unicode(f["name"]) for f in paramFields]
        
        # Get the feature type element
        etreeFeatureTypes = self.etDoc.findall("./{%s}featureType/{%s}FC_FeatureType" % (GFC_NS, GFC_NS))
        if len(etreeFeatureTypes) > 0:
            featureTypeElement = etreeFeatureTypes[0]
            
            # Loop over the carrierOfCharacteristics elements
            etreeCarrierOfCharacteristics = featureTypeElement.findall("./{%s}carrierOfCharacteristics" % (GFC_NS))
            for etreeCoC in etreeCarrierOfCharacteristics:
                
                # Get the field name
                fieldNamesElements = etreeCoC.findall("./{%s}FC_FeatureAttribute/{%s}memberName/{%s}LocalName" % (GFC_NS, GFC_NS, GCO_NS))

                # Removal of the carrierOfCharacteristics element if its name is not in the names of the paramFields parameter
                if len(fieldNamesElements) == 0 or fieldNamesElements[0].text not in fieldNamesInParams:
                    featureTypeElement.remove(etreeCoC)


    def updateField(self, paramField):
        
        # Does the field exist?
        # if not create a new one
        fieldName = unicode(paramField["name"])
        fieldElement = self.getFieldElement(fieldName, True)

        # Update definition
        element = fieldElement.find("./{%s}FC_FeatureAttribute/{%s}definition/{%s}CharacterString" % (GFC_NS, GFC_NS, GCO_NS))
        if element: element.text = unicode(paramField["definition"])

        # Update cardinality
        lower = "1"
        upper = "1"
        
        cardValues = unicode(paramField["cardinality"]).split("..")
        if len(cardValues) == 1:
            if cardValues[0] in ["0", "1"]:
                lower = cardValues[0]
        elif len(cardValues) == 2:
            if cardValues[0] in ["0", "1"]:
                lower = cardValues[0]
            
            if cardValues[1] in ["1", "n"]:
                upper = cardValues[1]
        
        # lower
        lowerElement = fieldElement.find("./{%s}FC_FeatureAttribute/{%s}cardinality/{%s}Multiplicity/{%s}range/{%s}MultiplicityRange/{%s}lower/{%s}Integer" % (GFC_NS, GFC_NS, GCO_NS, GCO_NS, GCO_NS, GCO_NS, GCO_NS))
        if lowerElement != None:
            lowerElement.text = lower

        # upper
        upperElement = fieldElement.find("./{%s}FC_FeatureAttribute/{%s}cardinality/{%s}Multiplicity/{%s}range/{%s}MultiplicityRange/{%s}upper/{%s}UnlimitedInteger" % (GFC_NS, GFC_NS, GCO_NS, GCO_NS, GCO_NS, GCO_NS, GCO_NS))
        if upperElement != None:
            if upper == "1":
                upperElement.text = "1"
                upperElement.attrib["isInfinite"] = "false"
            else:
                upperElement.text = ""
                upperElement.attrib["isInfinite"] = "true"

        # Update listed values
        # Remove all listed values
        listedValuesElements = fieldElement.findall("./{%s}FC_FeatureAttribute/{%s}listedValue" % (GFC_NS, GCO_NS))
        for listedValue in listedValuesElements:
            fieldElement.remove(listedValue)
        
        # Insert the new values
        parentElement = fieldElement.find("./{%s}FC_FeatureAttribute" % (GFC_NS))
        for paramListedValue in paramField['values']:
            lv = etree.Element("{%s}listedValue" % (GFC_NS))
            lvlv = etree.SubElement(lv, "{%s}FC_ListedValue" % (GFC_NS))
            lvlvlbl = etree.SubElement(lvlv, "{%s}label" % (GFC_NS))
            lvlvlblcs = etree.SubElement(lvlvlbl, "{%s}CharacterString" % (GCO_NS))
            lvlvlblcs.text = unicode(paramListedValue["label"])
            lvlvcod = etree.SubElement(lvlv, "{%s}code" % (GFC_NS))
            lvlvcodcs = etree.SubElement(lvlvcod, "{%s}CharacterString" % (GCO_NS))
            lvlvcodcs.text = unicode(paramListedValue["code"])
            lvlvdef = etree.SubElement(lvlv, "{%s}definition" % (GFC_NS))
            lvlvdefcs = etree.SubElement(lvlvdef, "{%s}CharacterString" % (GCO_NS))
            lvlvdefcs.text = unicode(paramListedValue["definition"])
            parentElement.insert(len(parentElement.getchildren())-1, lv)
        
        # Update value type
        element = fieldElement.find("./{%s}FC_FeatureAttribute/{%s}valueType/{%s}TypeName/{%s}aName/{%s}CharacterString" % (GFC_NS, GFC_NS, GCO_NS, GCO_NS, GCO_NS))
        if element: element.text = unicode(paramField["type"])


    def getFieldElement(self, fieldName, createEmptyField = False):
        fieldElement = None
        
        # Get the feature type element
        etreeFeatureTypes = self.etDoc.findall("./{%s}featureType/{%s}FC_FeatureType" % (GFC_NS, GFC_NS))
        if len(etreeFeatureTypes) > 0:
            
            featureTypeElement = etreeFeatureTypes[0]
            
            # Loop over the carrierOfCharacteristics elements
            etreeCarrierOfCharacteristics = featureTypeElement.findall("./{%s}carrierOfCharacteristics" % (GFC_NS))
            for etreeCoC in etreeCarrierOfCharacteristics:
                
                # Compare the field name
                fieldNamesElements = etreeCoC.findall("./{%s}FC_FeatureAttribute/{%s}memberName/{%s}LocalName" % (GFC_NS, GFC_NS, GCO_NS))
                if len(fieldNamesElements) == 1 and fieldNamesElements[0].text == fieldName:
                    fieldElement = etreeCoC.find("./{%s}FC_FeatureAttribute" % (GFC_NS))

            # Create a new carrierOfCharacteristics element
            if not fieldElement and createEmptyField:
                fieldElement = self.insertEmptyField(featureTypeElement, fieldName)
            
        return fieldElement

    def insertEmptyField(self, parentElement, fieldName):
        coc = etree.SubElement(parentElement, "{%s}carrierOfCharacteristics" % (GFC_NS))
        cocfa = etree.SubElement(coc, "{%s}FC_FeatureAttribute" % (GFC_NS))
        cocfamn = etree.SubElement(cocfa, "{%s}memberName" % (GFC_NS))
        cocfamnln = etree.SubElement(cocfamn, "{%s}LocalName" % (GCO_NS))
        cocfamnln.text = fieldName
        cocfadef = etree.SubElement(cocfa, "{%s}definition" % (GFC_NS))
        cocfadefcs = etree.SubElement(cocfadef, "{%s}CharacterString" % (GCO_NS))
        cocfacar = etree.SubElement(cocfa, "{%s}cardinality" % (GFC_NS))
        cocfacarm = etree.SubElement(cocfacar, "{%s}Multiplicity" % (GCO_NS))
        cocfacarmr = etree.SubElement(cocfacarm, "{%s}range" % (GCO_NS))
        cocfacarmrmr = etree.SubElement(cocfacarmr, "{%s}MultiplicityRange" % (GCO_NS))
        cocfacarmrmrl = etree.SubElement(cocfacarmrmr, "{%s}lower" % (GCO_NS))
        cocfacarmrmrli = etree.SubElement(cocfacarmrmrl, "{%s}Integer" % (GCO_NS))
        cocfacarmrmrli.text = "1"
        cocfacarmrmru = etree.SubElement(cocfacarmrmr, "{%s}upper" % (GCO_NS))
        cocfacarmrmruu = etree.SubElement(cocfacarmrmru, "{%s}UnlimitedInteger" % (GCO_NS))
        cocfacarmrmruu.text = "1"
        cocfacarmrmruu.attrib["isInfinite"] = "false"
        cocfacarmrmruu.attrib["{%s}nil" % XSI_NS] = "false"
        cocfaun = etree.SubElement(cocfa, "{%s}valueMeasurementUnit" % (GFC_NS))
        cocfaunun = etree.SubElement(cocfaun, "{%s}UnitDefinition" % (GML_NS))
        cocfaunun.attrib["{%s}id" % GML_NS] = "unknown"
        cocfaunundes = etree.SubElement(cocfaunun, "{%s}description" % (GML_NS))
        cocfaununid = etree.SubElement(cocfaunun, "{%s}identifier" % (GML_NS))
        cocfaununid.attrib["codeSpace"] = "unknown"
        cocfavt = etree.SubElement(cocfa, "{%s}valueType" % (GFC_NS))
        cocfavttn = etree.SubElement(cocfavt, "{%s}TypeName" % (GCO_NS))
        cocfavttnan = etree.SubElement(cocfavttn, "{%s}aName" % (GCO_NS))
        cocfavttnancs = etree.SubElement(cocfavttnan, "{%s}CharacterString" % (GCO_NS))
    
        return coc

