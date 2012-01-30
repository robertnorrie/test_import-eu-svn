# -*- coding: utf-8 -*-
"""
/***************************************************************************
 featureCatCreator
                                 A QGIS plugin
    Generates, for a selected datasource, a feature catalogue metadata
    record in XML format compliant with ISO19110 standard.
    This project has been funded by the EEA (European Environment Agency) :
    http://www.eea.europa.eu
    The project has been developped by Neogeo and Oslandia :
    http://www.neogeo-online.net/
    http://www.oslandia.com
                             -------------------
        begin                : 2012-01-17
        copyright            : (C) 2012 Neogeo & Oslandia, funded by EEA
        email                : vincent.picavet@oslandia.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

# This is a module dedicated to generating ISO19110 XML data
# given specific parameters.

# Namespaces used by iso 19110 docs
GFC_NS = "http://www.isotc211.org/2005/gfc"
GCO_NS = "http://www.isotc211.org/2005/gco"
GML_NS = "http://www.opengis.net/gml"
GMD_NS = "http://www.isotc211.org/2005/gmd"
XSI_NS = "http://www.w3.org/2001/XMLSchema-instance"

#from PyQt4 import QtGui
from PyQt4 import QtXml # Used only to prettyfy the xml doc content
from PyQt4 import QtCore

import os.path
import urllib2
import xml.etree.ElementTree as etree
import xml.dom.minidom as minidom # Used to normalize the naamespaces
import codecs
import copy
import uuid # Used for the gml:id attributes
from xml.parsers.expat import ExpatError # Used for accessing the ExpatError exception members


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



def cloneElementAndCleanNs(oldEl, newDoc, uriNsMap, declNs):
    # Create the new element
    namespace = oldEl.namespaceURI
    newEl = newDoc.createElementNS(namespace, "%s:%s" % (uriNsMap[namespace], oldEl.localName))
    
    # Clone attributes
    nbAttrs = oldEl.attributes.length
    for i in range(nbAttrs):
        attr = oldEl.attributes.item(i)
        
        if attr.prefix == "xmlns":
            if attr.value in declNs:
                # If the namespace is already declared we don't declare it once again
                pass
            elif attr.value in uriNsMap:
                # If the namespace is known one we change its prefix
                newEl.setAttribute("%s:%s" % (attr.prefix, uriNsMap[attr.value]), attr.value)
            
            # The namespace is added to the declared namespace list if it's not already in it
            if attr.value not in declNs:
                declNs.append(attr.value)
        elif attr.namespaceURI != None:
            newEl.setAttributeNS(attr.namespaceURI, "%s:%s" % (uriNsMap[attr.namespaceURI], attr.localName), attr.value)
        else:
            newEl.setAttribute("%s" % attr.localName, attr.value)
    
    # If some of the namespaces of the uriNsMap dictionary are not yet declared we declare them
    for ns in uriNsMap:
        if ns not in declNs:
            newEl.setAttribute("%s:%s" % ("xmlns", uriNsMap[ns]), ns)
            declNs.append(ns)
    
    # Clone subelements
    for child in oldEl.childNodes:
        if child.nodeType == child.TEXT_NODE:
            if len(child.nodeValue.strip()) > 0:
                newChild = child.cloneNode(False)
                newChild.nodeValue = newChild.nodeValue.strip()
                newEl.appendChild(newChild)
        elif child.nodeType == child.ELEMENT_NODE:
            newChild = cloneElementAndCleanNs(child, newDoc, uriNsMap, copy.copy(declNs))
            newEl.appendChild(newChild)
        else:
            newChild = child.cloneNode(False)
            newEl.appendChild(newChild)
    
    return newEl


def normalizeNamespaces(xmlDocContent):
    nsmap = {GFC_NS: "gfc", GCO_NS:"gco", GML_NS:"gml", GMD_NS:"gmd", XSI_NS:"xsi"}
    oldDoc = minidom.parseString(xmlDocContent)
    oldRoot = oldDoc.documentElement

    newDoc = minidom.Document()
    newRoot = cloneElementAndCleanNs(oldRoot, newDoc, nsmap, declNs=[])
    newDoc.appendChild(newRoot)

    #return newDoc.toprettyxml(indent="  ")
    return newDoc.toxml()


def getIndexOfLastSubElement(parentEl, subElNames):
    result = 0
    
    subEls = parentEl.getchildren()
    nbSubEls = len(subEls)
    if len(subEls) > 0:
        for i in range(nbSubEls-1,-1,-1):
            if subEls[i].tag in subElNames:
                result = i+1
                break
    
    return result


def insertSubElementAfter(parentEl, childEl, subElNames):
    index = getIndexOfLastSubElement(parentEl, subElNames)
    parentEl.insert(index, childEl)


def removeSubElements(etreeElement, subElementsTag, numberOfElementsToBeLeft):
    subElements = etreeElement.findall(subElementsTag)
    for subElement in subElements[numberOfElementsToBeLeft:]:
        etreeElement.remove(subElement)


class iso19110Doc:
    
    def __init__(self, templatePath):
        templateContent = getTemplateContent(templatePath)
        self.templateContent = templateContent.decode('utf-8')
        self.checkTemplateValidity()
        
        #self.etDoc = etree.fromstring(self.templateContent)
        self.etDoc = etree.fromstring(self.templateContent.encode('utf-8'))

        
    def checkTemplateValidity(self):
        templateDomDoc = QtXml.QDomDocument()
        
        # check if the template is a valid XML document
        domParsingResult =  templateDomDoc.setContent(QtCore.QString(self.templateContent))
        if not domParsingResult[0]:
            raise ValueError, "The selected iso19110 template is not a valid XML document (%s at line %d and column %d)" % (domParsingResult[1], domParsingResult[2], domParsingResult[3])
        
        # check the presence and cardinality of required elements
        # gfc:FC_FeatureCatalogue
        etDoc = etree.fromstring(self.templateContent.encode('utf-8'))
        #etDoc = etree.fromstring(self.templateContent)
        if etDoc.tag != "{%s}FC_FeatureCatalogue" % GFC_NS:
            raise ValueError, "The selected iso19110 template is not a valid: the root element name is not %s:FC_FeatureCatalogue" % GFC_NS
        
        # gfc:producer
        producers = etDoc.findall("./{%s}producer/{%s}CI_ResponsibleParty" % (GFC_NS, GMD_NS))
        if len(producers) == 0:
            raise ValueError, "The selected iso19110 template is not a valid: it does not contain an {%s}producer/{%s}CI_ResponsibleParty element" % (GFC_NS, GMD_NS)
        elif len(producers) > 1:
            raise ValueError, "The selected iso19110 template is not a valid: it contains more than one {%s}producer/{%s}CI_ResponsibleParty element" % (GFC_NS, GMD_NS)

    
    def toString(self):
        docContent = etree.tostring(self.etDoc, encoding="utf-8")
        
        docContent = normalizeNamespaces(docContent)
        
        # Prettyfy the xml doc content
        qDomDoc = QtXml.QDomDocument()
        #qDomDoc.setContent(QtCore.QString(docContent.decode('utf-8')))
        qDomDoc.setContent(QtCore.QString(docContent))
        docContent = unicode(qDomDoc.toString(2))
        
        return docContent

    def save(self, filePath):
        file = codecs.open(filePath, 'w', "utf-8")
        file.write(self.toString())
        file.close()

    def updateWithXmlContent(self, xmlViewContent):
        try:
            self.etDoc = etree.fromstring(unicode(xmlViewContent).encode('utf-8'))
        except ExpatError, e:
            raise ValueError("The content of the XML document is not valid:\n\nError : %s" % (e.message))

    def updateWithParams(self, params):
        # udate uuid with a new one
        self.setFcUuid()

        # update the feature catalogue name, scope and version number
        self.setFcName(params["fc_name"])
        self.setFcScope(params["fc_scope"])
        self.setFcVersionNumber(params["fc_versionNumber"])
        
        # updating the date of the feature catalog
        self.updateFcVersionDate()
        
        # clean the feature type
        self.cleanFt()
        
        # update the feature type name and definition
        self.setFtName(params["ft_name"])
        self.setFtDefinition(params["ft_definition"])
        
        # remove fields not present in param
        self.removeExtraFields(params["fields"])
        
        # update the fields/attributes
        for field in params["fields"]:
            self.updateField(field)

    def extractParamsFromContent(self):
        params = {}
        
        # Feature catalogue properties
        fcName = self.getFcName()
        if fcName != None:
            params["fc_name"] = QtCore.QString(fcName)
        else:
            params["fc_name"] = None

        fcScope = self.getFcScope()
        if fcScope != None:
            params["fc_scope"] = QtCore.QString(fcScope)
        else:
            params["fc_scope"] = None

        fcVersionNumber = self.getFcVersionNumber()
        if fcVersionNumber != None:
            params["fc_versionNumber"] = QtCore.QString(fcVersionNumber)
        else:
            params["fc_versionNumber"] = None
        
        # Feature type general properties
        ftName = self.getFtName()
        if ftName != None:
            params["ft_name"] = QtCore.QString(ftName)
        else:
            params["ft_name"] = None
        
        ftDefinition = self.getFtDefinition()
        if ftDefinition != None:
            params["ft_definition"] = QtCore.QString(ftDefinition)
        else:
            params["ft_definition"] = None
        
        # Attributes properties
        params["fields"] = []
        ft = self.etDoc.find("./{%s}featureType" % (GFC_NS))
        cocs = ft.findall("./{%s}FC_FeatureType/{%s}carrierOfCharacteristics" % (GFC_NS, GFC_NS))
        
        fieldIndex = 0
        for coc in cocs:
            paramField = {}
            
            # Index
            paramField["index"] = fieldIndex
            
            # Name
            namEl = coc.find("./{%s}FC_FeatureAttribute/{%s}memberName/{%s}LocalName" % (GFC_NS, GFC_NS, GCO_NS))
            if namEl != None and namEl.text != None:
                paramField["name"] = QtCore.QString(namEl.text)
            else:
                paramField["name"] = None
            
            # Definition
            defEl = coc.find("./{%s}FC_FeatureAttribute/{%s}definition/{%s}CharacterString" % (GFC_NS, GFC_NS, GCO_NS))
            if defEl != None and defEl.text != None:
                paramField["definition"] = QtCore.QString(defEl.text)
            else:
                paramField["definition"] = None
            
            # Cardinality
            lower = "0"
            upper = "1"
            lowerEl = coc.find("./{%s}FC_FeatureAttribute/{%s}cardinality/{%s}Multiplicity/{%s}range/{%s}MultiplicityRange/{%s}lower/{%s}Integer" % (GFC_NS, GFC_NS, GCO_NS, GCO_NS, GCO_NS, GCO_NS, GCO_NS))
            if lowerEl != None and lowerEl.text in ("0", "1"):
                lower = lowerEl.text
            upperEl = coc.find("./{%s}FC_FeatureAttribute/{%s}cardinality/{%s}Multiplicity/{%s}range/{%s}MultiplicityRange/{%s}upper/{%s}UnlimitedInteger" % (GFC_NS, GFC_NS, GCO_NS, GCO_NS, GCO_NS, GCO_NS, GCO_NS))
            if upperEl != None and upperEl.text != "1":
                upper = "n"
            paramField["cardinality"] = QtCore.QString("%s..%s" % (lower, upper))

            # Type
            typEl = coc.find("./{%s}FC_FeatureAttribute/{%s}valueType/{%s}TypeName/{%s}aName/{%s}CharacterString" % (GFC_NS, GFC_NS, GCO_NS, GCO_NS, GCO_NS))
            if typEl != None and typEl.text != None:
                paramField["type"] = QtCore.QString(typEl.text)
            else:
                paramField["type"] = None

            # Values
            paramField["values"] = []
            valEls = coc.findall("./{%s}FC_FeatureAttribute/{%s}listedValue/{%s}FC_ListedValue" % (GFC_NS, GFC_NS, GFC_NS))
            for valEl in valEls:
                paramValue = {}
                
                # Code
                codEl = valEl.find("./{%s}code/{%s}CharacterString" % (GFC_NS, GCO_NS))
                if codEl != None and codEl.text != None:
                    paramValue["code"] = QtCore.QString(codEl.text)
                else:
                    paramValue["code"] = None
                
                # Definition
                defEl = valEl.find("./{%s}definition/{%s}CharacterString" % (GFC_NS, GCO_NS))
                if defEl != None and defEl.text != None:
                    paramValue["definition"] = QtCore.QString(defEl.text)
                else:
                    paramValue["definition"] = None
                
                # Label
                labEl = valEl.find("./{%s}label/{%s}CharacterString" % (GFC_NS, GCO_NS))
                if labEl != None and labEl.text != None:
                    paramValue["label"] = QtCore.QString(labEl.text)
                else:
                    paramValue["label"] = None
                
                paramField["values"].append(paramValue)

            params["fields"].append(paramField)
            fieldIndex = fieldIndex + 1
            
        return params

    def getFcName(self):
        try:
            fcName = self.etDoc.findall("./{%s}name/{%s}CharacterString" % (GFC_NS, GCO_NS))[0].text
        except IndexError, e:
            fcName = ""
        return fcName

    def setFcName(self, newName):
        fcNames = self.etDoc.findall("./{%s}name/{%s}CharacterString" % (GFC_NS, GCO_NS))
        if len(fcNames) != 1:
            self.cleanFcName()
        
        fcName = self.etDoc.find("./{%s}name/{%s}CharacterString" % (GFC_NS, GCO_NS))
        if isinstance(newName, QtCore.QString):
            fcName.text = unicode(newName)
        else:
            fcName.text = newName

    def setFcUuid(self):
        self.etDoc.attrib["uuid"] = str(uuid.uuid4())

    def cleanFcName(self):
        fcNames = self.etDoc.findall("./{%s}name" % (GFC_NS))
        if len(fcNames) > 1:
            removeSubElements(self.etDoc, "{%s}name" % (GFC_NS), 1)
        if len(fcNames) == 0:
            nm = etree.Element("{%s}name" % (GFC_NS))
            nmcs = etree.SubElement(nm, "{%s}CharacterString" % (GCO_NS))
            self.etDoc.insert(0, nm)
        
        fcName = self.etDoc.find("./{%s}name" % (GFC_NS))
        fcNameCss = fcName.findall("./{%s}CharacterString" % (GCO_NS))
        if len(fcNameCss) > 1:
            removeSubElements(fcName, "{%s}CharacterString" % (GCO_NS), 1)
        if len(fcNameCss) == 0:
            etree.SubElement(fcName, "{%s}CharacterString" % (GCO_NS))

   
    def getFcScope(self):
        try:
            fcScope = self.etDoc.findall("./{%s}scope/{%s}CharacterString" % (GFC_NS, GCO_NS))[0].text
        except IndexError, e:
            fcScope = ""
        return fcScope

    def setFcScope(self, newScope):
        fcScopes = self.etDoc.findall("./{%s}scope/{%s}CharacterString" % (GFC_NS, GCO_NS))
        if len(fcScopes) != 1:
            self.cleanFcScope()
            
        fcScope = self.etDoc.find("./{%s}scope/{%s}CharacterString" % (GFC_NS, GCO_NS))
        if isinstance(newScope, QtCore.QString):
            fcScope.text = unicode(newScope)
        else:
            fcScope.text = newScope

    def cleanFcScope(self):
        fcScopes = self.etDoc.findall("./{%s}scope" % (GFC_NS))
        if len(fcScopes) > 1:
            removeSubElements(self.etDoc, "{%s}scope" % (GFC_NS), 1)
        if len(fcScopes) == 0:
            sc = etree.Element("{%s}scope" % (GFC_NS))
            sccs = etree.SubElement(sc, "{%s}CharacterString" % (GCO_NS))
            insertSubElementAfter(self.etDoc, sc, ("{%s}name" % (GFC_NS)))
        
        fcScope = self.etDoc.find("./{%s}scope" % (GFC_NS))
        fcScopeCss = fcScope.findall("./{%s}CharacterString" % (GCO_NS))
        if len(fcScopeCss) > 1:
            removeSubElements(fcScope, "{%s}CharacterString" % (GCO_NS), 1)
        if len(fcScopeCss) == 0:
            etree.SubElement(fcScope, "{%s}CharacterString" % (GCO_NS))


    def getFcVersionNumber(self):
        try:
            fcVersion = self.etDoc.findall("./{%s}versionNumber/{%s}CharacterString" % (GFC_NS, GCO_NS))[0].text
        except IndexError, e:
            fcVersion = ""
        return fcVersion

    def setFcVersionNumber(self, newVersionNumber):
        fcVersions = self.etDoc.findall("./{%s}versionNumber/{%s}CharacterString" % (GFC_NS, GCO_NS))
        if len(fcVersions) != 1:
            self.cleanFcVersionNumber()
            
        fcVersion = self.etDoc.find("./{%s}versionNumber/{%s}CharacterString" % (GFC_NS, GCO_NS))
        if isinstance(newVersionNumber, QtCore.QString):
            fcVersion.text = unicode(newVersionNumber)
        else:
            fcVersion.text = newVersionNumber

    def cleanFcVersionNumber(self):
        fcVersions = self.etDoc.findall("./{%s}versionNumber" % (GFC_NS))
        if len(fcVersions) > 1:
            removeSubElements(self.etDoc, "{%s}versionNumber" % (GFC_NS), 1)
        if len(fcVersions) == 0:
            vn = etree.Element("{%s}versionNumber" % (GFC_NS))
            vncs = etree.SubElement(vn, "{%s}CharacterString" % (GCO_NS))
            insertSubElementAfter(self.etDoc, vn, ("{%s}name" % (GFC_NS), "{%s}scope" % (GFC_NS)))
        
        fcVersion = self.etDoc.find("./{%s}versionNumber" % (GFC_NS))
        fcVersionCss = fcVersion.findall("./{%s}CharacterString" % (GCO_NS))
        if len(fcVersionCss) > 1:
            removeSubElements(fcVersion, "{%s}CharacterString" % (GCO_NS), 1)
        if len(fcVersionCss) == 0:
            etree.SubElement(fcVersion, "{%s}CharacterString" % (GCO_NS))


    def updateFcVersionDate(self):
        fcDates = self.etDoc.findall("./{%s}versionDate" % (GFC_NS))
        if len(fcDates) != 1:
            self.cleanFcVersionDate()
        
        # remove all child elements
        fcDate = self.etDoc.find("./{%s}versionDate" % (GFC_NS))
        dateValues = fcDate.getchildren()
        for dateValue in dateValues:
            fcDate.remove(dateValue)
            
        # set the new value
        import datetime
        today = datetime.date.today()
        format = "%Y-%m-%d"        
        newDateNode = etree.SubElement(fcDate, "{%s}%s" % (GCO_NS, "Date"))
        newDateNode.text = today.strftime(format)
        
    def cleanFcVersionDate(self):
        fcDates = self.etDoc.findall("./{%s}versionDate" % (GFC_NS))
        if len(fcDates) > 1:
            removeSubElements(self.etDoc, "{%s}versionDate" % (GFC_NS), 1)
        if len(fcDates) == 0:
            vd = etree.Element("{%s}versionDate" % (GFC_NS))
            vddt= etree.SubElement(vd, "{%s}Date" % (GCO_NS))
            insertSubElementAfter(self.etDoc, vd, ("{%s}name" % (GFC_NS), "{%s}scope" % (GFC_NS), "{%s}versionNumber" % (GFC_NS)))
        
        fcDate = self.etDoc.find("./{%s}versionDate" % (GFC_NS))
        fcDateCss = fcDate.findall("./{%s}Date" % (GCO_NS))
        if len(fcDateCss) > 1:
            removeSubElements(fcDate, "{%s}Date" % (GCO_NS), 1)
        if len(fcDateCss) == 0:
            etree.SubElement(fcDate, "{%s}Date" % (GCO_NS))


    def getFtName(self):
        ftName = self.etDoc.findall("./{%s}featureType/{%s}FC_FeatureType/{%s}typeName/{%s}LocalName" % (GFC_NS, GFC_NS, GFC_NS, GCO_NS))[0].text
        return ftName

    def setFtName(self, newName):
        ftNames = self.etDoc.findall("./{%s}featureType/{%s}FC_FeatureType/{%s}typeName/{%s}LocalName" % (GFC_NS, GFC_NS, GFC_NS, GCO_NS))
        if len(ftNames) != 1:
            self.cleanFtName()
            
        ftName = self.etDoc.find("./{%s}featureType/{%s}FC_FeatureType/{%s}typeName/{%s}LocalName" % (GFC_NS, GFC_NS, GFC_NS, GCO_NS))
        if isinstance(newName, QtCore.QString):
            ftName.text = unicode(newName)
        else:
            ftName.text = newName

    def cleanFtName(self):
        ftft = self.etDoc.find("./{%s}featureType/{%s}FC_FeatureType" % (GFC_NS, GFC_NS))
        ftfttns = ftft.findall("./{%s}typeName" % (GFC_NS))
        if len(ftfttns) > 1:
            removeSubElements(ftft, "{%s}typeName" % (GFC_NS), 1)
        if len(ftfttns) == 0:
            ftfttn = etree.Element("{%s}typeName" % (GFC_NS))
            ftfttnln = etree.SubElement(ftfttn, "{%s}LocalName" % (GCO_NS))
            ftft.insert(0, ftfttn)
        
        ftfttn = ftft.find("./{%s}typeName" % (GFC_NS))
        ftfttnlns = ftfttn.findall("./{%s}LocalName" % (GCO_NS))
        if len(ftfttnlns) > 1:
            removeSubElements(ftfttn, "{%s}LocalName" % (GCO_NS), 1)
        if len(ftfttnlns) == 0:
            etree.SubElement(ftfttn, "{%s}LocalName" % (GCO_NS))

   
    def getFtDefinition(self):
        ftDefinition = self.etDoc.findall("./{%s}featureType/{%s}FC_FeatureType/{%s}definition/{%s}CharacterString" % (GFC_NS, GFC_NS, GFC_NS, GCO_NS))[0].text
        return ftDefinition

    def setFtDefinition(self, newDefinition):
        ftDefinitions = self.etDoc.findall("./{%s}featureType/{%s}FC_FeatureType/{%s}definition/{%s}CharacterString" % (GFC_NS, GFC_NS, GFC_NS, GCO_NS))
        if len(ftDefinitions) != 1:
            self.cleanFtDefinition()
            
        ftDefinition = self.etDoc.find("./{%s}featureType/{%s}FC_FeatureType/{%s}definition/{%s}CharacterString" % (GFC_NS, GFC_NS, GFC_NS, GCO_NS))
        if isinstance(newDefinition, QtCore.QString):
            ftDefinition.text = unicode(newDefinition)
        else:
            ftDefinition.text = newDefinition

    def cleanFtDefinition(self):
        ftft = self.etDoc.find("./{%s}featureType/{%s}FC_FeatureType" % (GFC_NS, GFC_NS))
        ftftdfs = ftft.findall("./{%s}definition" % (GFC_NS))
        if len(ftftdfs) > 1:
            removeSubElements(ftft, "{%s}definition" % (GFC_NS), 1)
        if len(ftftdfs) == 0:
            ftftdf = etree.Element("{%s}definition" % (GFC_NS))
            ftftdfcs = etree.SubElement(ftftdf, "{%s}CharacterString" % (GCO_NS))
            insertSubElementAfter(ftft, ftftdf, ("{%s}typeName" % (GFC_NS)))
        
        ftftdf = ftft.find("./{%s}definition" % (GFC_NS))
        ftftdfcss = ftftdf.findall("./{%s}CharacterString" % (GCO_NS))
        if len(ftftdfcss) > 1:
            removeSubElements(ftftdf, "{%s}CharacterString" % (GCO_NS), 1)
        if len(ftftdfcss) == 0:
            etree.SubElement(ftftdf, "{%s}CharacterString" % (GCO_NS))

    def cleanFtIsAbstract(self):
        ftft = self.etDoc.find("./{%s}featureType/{%s}FC_FeatureType" % (GFC_NS, GFC_NS))
        ftftias = ftft.findall("./{%s}isAbstract" % (GFC_NS))
        if len(ftftias) > 1:
            removeSubElements(ftft, "{%s}isAbstract" % (GFC_NS), 1)
        if len(ftftias) == 0:
            ftftia = etree.Element("{%s}isAbstract" % (GFC_NS))
            ftftiabo = etree.SubElement(ftftia, "{%s}Boolean" % (GCO_NS))
            insertSubElementAfter(ftft, ftftia, ("{%s}typeName" % (GFC_NS), "{%s}definition" % (GFC_NS)))
        
        ftftia = ftft.find("./{%s}isAbstract" % (GFC_NS))
        ftftiabos = ftftia.findall("./{%s}Boolean" % (GCO_NS))
        if len(ftftiabos) > 1:
            removeSubElements(ftftia, "{%s}Boolean" % (GCO_NS), 1)
        if len(ftftiabos) == 0:
            ftftiabo = etree.SubElement(ftftia, "{%s}Boolean" % (GCO_NS))
            ftftiabo.text = "false"

    def cleanFtFc(self):
        ftft = self.etDoc.find("./{%s}featureType/{%s}FC_FeatureType" % (GFC_NS, GFC_NS))
        ftftfcs = ftft.findall("./{%s}featureCatalogue" % (GFC_NS))
        if len(ftftfcs) > 1:
            removeSubElements(ftft, "{%s}featureCatalogue" % (GFC_NS), 1)
        if len(ftftfcs) == 0:
            ftftfc = etree.Element("{%s}featureCatalogue" % (GFC_NS))
            insertSubElementAfter(ftft, ftftfc, ("{%s}typeName" % (GFC_NS), "{%s}definition" % (GFC_NS), "{%s}isAbstract" % (GFC_NS)))

    def cleanFt(self):
        fts = self.etDoc.findall("./{%s}featureType" % (GFC_NS))
        if len(fts) > 1:
            removeSubElements(self.etDoc, "{%s}featureType" % (GFC_NS), 1)
        if len(fts) == 0:
            ft = etree.Element("{%s}featureType" % (GFC_NS))
            self.etDoc.insert(len(self.etDoc.getchildren()), ft)
        
        ft = self.etDoc.find("./{%s}featureType" % (GFC_NS))
        ftfts = ft.findall("./{%s}FC_FeatureType" % (GFC_NS))
        if len(ftfts) > 1:
            removeSubElements(ft, "{%s}FC_FeatureType" % (GFC_NS), 1)
        if len(ftfts) == 0:
            etree.SubElement(ft, "{%s}FC_FeatureType" % (GFC_NS))
        
        # Clean typeName, definition and isAbstract
        self.cleanFtName()
        self.cleanFtDefinition()
        self.cleanFtIsAbstract()
        self.cleanFtFc()

        # For each carrierOfCharacteristics remove extra FC_FeatureAttribute
        cocs = ft.findall("./{%s}FC_FeatureType/{%s}carrierOfCharacteristics" % (GFC_NS, GFC_NS))
        for coc in cocs:
            removeSubElements(coc, "{%s}FC_FeatureAttribute" % (GFC_NS), 1)
            
        # For each FC_FeatureAttribute remove extra elements
        fas = ft.findall("./{%s}FC_FeatureType/{%s}carrierOfCharacteristics/{%s}FC_FeatureAttribute" % (GFC_NS, GFC_NS, GFC_NS))
        for fa in fas:
            removeSubElements(fa, "{%s}memberName" % (GFC_NS), 1)
            removeSubElements(fa, "{%s}definition" % (GFC_NS), 1)
            removeSubElements(fa, "{%s}cardinality" % (GFC_NS), 1)
            removeSubElements(fa, "{%s}valueMeasurementUnit" % (GFC_NS), 1)
            removeSubElements(fa, "{%s}valueType" % (GFC_NS), 1)

    def removeExtraFields(self, paramFields):
        # List of the field names in the paramField parameter
        fieldNamesInParams = [unicode(f["name"]) for f in paramFields]
        
        # Get the feature type element
        etreeFeatureType = self.etDoc.find("./{%s}featureType/{%s}FC_FeatureType" % (GFC_NS, GFC_NS))
        if etreeFeatureType != None:
            # Loop over the carrierOfCharacteristics elements
            etreeCarrierOfCharacteristics = etreeFeatureType.findall("./{%s}carrierOfCharacteristics" % (GFC_NS))
            for etreeCoC in etreeCarrierOfCharacteristics:
                
                # Get the field name
                fieldNamesElements = etreeCoC.findall("./{%s}FC_FeatureAttribute/{%s}memberName/{%s}LocalName" % (GFC_NS, GFC_NS, GCO_NS))

                # Removal of the carrierOfCharacteristics element if its name is not in the names of the paramFields parameter
                if len(fieldNamesElements) == 0 or fieldNamesElements[0].text not in fieldNamesInParams:
                    etreeFeatureType.remove(etreeCoC)


    def updateField(self, paramField):
        
        # Does the field exist?
        # if not create a new one
        fieldName = unicode(paramField["name"])
        fieldElement = self.getFieldElement(fieldName, True)

        # Update definition
        element = fieldElement.find("./{%s}definition/{%s}CharacterString" % (GFC_NS, GCO_NS))
        if element != None: element.text = unicode(paramField["definition"])

        # Update cardinality
        # default values
        lower = "0"
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
        lowerElement = fieldElement.find("./{%s}cardinality/{%s}Multiplicity/{%s}range/{%s}MultiplicityRange/{%s}lower/{%s}Integer" % (GFC_NS, GCO_NS, GCO_NS, GCO_NS, GCO_NS, GCO_NS))
        if lowerElement != None:
            lowerElement.text = lower

        # upper
        upperElement = fieldElement.find("./{%s}cardinality/{%s}Multiplicity/{%s}range/{%s}MultiplicityRange/{%s}upper/{%s}UnlimitedInteger" % (GFC_NS, GCO_NS, GCO_NS, GCO_NS, GCO_NS, GCO_NS))
        if upperElement != None:
            if upper == "1":
                upperElement.text = "1"
                upperElement.attrib["isInfinite"] = "false"
                upperElement.attrib["{%s}nil" % XSI_NS] = "false"
            else:
                upperElement.text = ""
                upperElement.attrib["isInfinite"] = "true"
                upperElement.attrib["{%s}nil" % XSI_NS] = "true"

        # Update listed values
        # Remove all listed values
        listedValuesElements = fieldElement.findall("./{%s}listedValue" % (GFC_NS))
        for listedValue in listedValuesElements:
            fieldElement.remove(listedValue)
        
        # Insert the new values
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
            fieldElement.insert(len(fieldElement.getchildren()), lv)
        
        # Update value type
        element = fieldElement.find("./{%s}FC_FeatureAttribute/{%s}valueType/{%s}TypeName/{%s}aName/{%s}CharacterString" % (GFC_NS, GFC_NS, GCO_NS, GCO_NS, GCO_NS))
        if element!= None: element.text = unicode(paramField["type"])


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
        cocfaunun.attrib["{%s}id" % GML_NS] = "unknown-%s" % uuid.uuid1()
        cocfaunundes = etree.SubElement(cocfaunun, "{%s}description" % (GML_NS))
        cocfaununid = etree.SubElement(cocfaunun, "{%s}identifier" % (GML_NS))
        cocfaununid.attrib["codeSpace"] = "unknown"
        cocfavt = etree.SubElement(cocfa, "{%s}valueType" % (GFC_NS))
        cocfavttn = etree.SubElement(cocfavt, "{%s}TypeName" % (GCO_NS))
        cocfavttnan = etree.SubElement(cocfavttn, "{%s}aName" % (GCO_NS))
        cocfavttnancs = etree.SubElement(cocfavttnan, "{%s}CharacterString" % (GCO_NS))
    
        return coc
