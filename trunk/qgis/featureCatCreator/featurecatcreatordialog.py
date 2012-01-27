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
import random

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

from ui_featurecatcreator import Ui_featureCatCreator
import iso19110

# create the dialog for zoom to point
class featureCatCreatorDialog(QDialog):
    def __init__(self, iface):
        QDialog.__init__(self)
        # get paths
        self.user_plugin_dir = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/python/plugins"
        self.plugin_dir = self.user_plugin_dir + "/featurecatcreator"
        self.last_used_dir = QDir.homePath()

        # keep qgis interface reference
        self.iface = iface
        self.currentLayer = None
        self.currentFields = []
        self.nodataValues = []
        self.savedState = False
        # reference to the iso19110Doc instance
        self.isoDoc = None

        # Plugin settings
        self.settings = QSettings()

        # Set up the user interface from Designer.
        self.ui = Ui_featureCatCreator()
        self.ui.setupUi(self)

        # Set UI from saved settings
        self.loadSettings()

        # init isoDoc
        self.updateIsoDocFromXml()

        # default is first tab (XML)
        self.ui.tabWidget.setCurrentIndex(0)

        # load documentation
        self.ui.helpContent.setUrl(QUrl(self.plugin_dir + "/help/featurecatcreator_help.html"))

        # update data source combobox content
        self.updateDatasourceBox()

        self.connectSignals()

    def connectSignals(self):
        # connect close button
        self.connect(self.ui.buttonBox, SIGNAL('clicked(QAbstractButton *)'), self.bboxClicked)        
        # connect save button
        self.connect(self.ui.saveButton, SIGNAL('clicked()'), self.saveXML)        
        # connect browse button to file search dialog
        self.connect(self.ui.browseTemplateButton, SIGNAL('clicked()'), self.updateTemplateFile)
        # connect Load XML button to loading the file
        self.connect(self.ui.loadTemplate, SIGNAL('clicked()'), self.loadTemplateFile)
        # current layer change
        self.connect(self.ui.dataSourceBox, SIGNAL('currentIndexChanged(int)'), self.changeCurrentLayer)
        # connect analyze button to the analysis
        self.connect(self.ui.analyzeButton, SIGNAL('clicked()'), self.analyzeButtonClicked)
        # connect nodata button to input values
        self.connect(self.ui.nodataButton, SIGNAL('clicked()'), self.getNodataInput)
        # connect attribute table button to show attribute table
        self.connect(self.ui.attributeTableButton, SIGNAL('clicked()'), self.showAttributeTable)
        # connect load fc and ft from XML
        self.connect(self.ui.loadFcFromXML, SIGNAL('clicked()'), self.fillFcForm)
        self.connect(self.ui.loadFtFromXML, SIGNAL('clicked()'), self.fillFtForm)

        # connect refresh XML button
        self.connect(self.ui.refreshButton, SIGNAL('clicked()'), self.refreshXML)
        # when user go out of XML tab, update internal xml doc
        self.connect(self.ui.tabWidget, SIGNAL('currentChanged(int)'), self.tabChanged)

        # connect load fields from layer button
        self.connect(self.ui.loadFromLayer, SIGNAL('clicked()'), self.updateFieldList)
        # connect load fields from XML button
        self.connect(self.ui.loadFromXML, SIGNAL('clicked()'), self.loadFieldsFromXML)
        # when current field changes, fill form
        self.connect(self.ui.currentFieldBox, SIGNAL('currentIndexChanged(int)'), self.updateFieldForm)
        # attribute field form are active. connect them
        self.activeFieldForm(True)
        # values elements
        self.connect(self.ui.newValueButton, SIGNAL('clicked()'), self.newValueRow)
        self.connect(self.ui.deleteValueButton, SIGNAL('clicked()'), self.deleteValueRow)

    def loadSettings(self):
        self.ui.templateText.setText(self.settings.value("featurecatcreator/template",\
                self.plugin_dir + "/fc_template_01.xml").toString())
        self.last_used_dir = QFileInfo(self.ui.templateText.text()).absolutePath()
        self.loadTemplateFile()
        if self.settings.value("featurecatcreator/classification", False).toBool():
            self.ui.classification.setChecked(True)
        self.ui.rowNb.setValue(self.settings.value("featurecatcreator/rownb", 1000).toInt()[0])
        self.ui.requiredValuesNb.setValue(self.settings.value("featurecatcreator/requiredvaluesnb", 5).toInt()[0])
        self.last_used_dir = self.settings.value("featurecatcreator/lastuseddir", QDir.homePath()).toString()

    def saveSettings(self):
        self.settings.setValue("featurecatcreator/template", self.ui.templateText.text())
        self.settings.setValue("featurecatcreator/classification", self.ui.classification.isChecked())
        self.settings.setValue("featurecatcreator/rownb", self.ui.rowNb.value())
        self.settings.setValue("featurecatcreator/requiredvaluesnb", self.ui.requiredValuesNb.value())
        self.settings.setValue("featurecatcreator/lastuseddir", self.last_used_dir)

    def showAttributeTable(self):
        if self.currentLayer and self.currentLayer.type() == QgsMapLayer.VectorLayer:
            self.iface.showAttributeTable(self.currentLayer)

    def activeFieldForm(self, connect = True):
        if connect:
            # when one of the field form element is finished editing, 
            # then save to internal field struct
            self.connect(self.ui.f_typeText, SIGNAL('editTextChanged ( const QString &)'), self.saveFieldComponent)
            self.connect(self.ui.f_definitionText, SIGNAL('textChanged()'), self.saveFieldComponent)
            self.connect(self.ui.f_cardinalityText, SIGNAL('editTextChanged ( const QString &)'), self.saveFieldComponent)
            self.connect(self.ui.valuesTable, SIGNAL('cellChanged(int, int)'), self.saveFieldComponent)
        else:
            self.disconnect(self.ui.f_typeText, SIGNAL('editTextChanged ( const QString &)'), self.saveFieldComponent)
            self.disconnect(self.ui.f_definitionText, SIGNAL('textChanged()'), self.saveFieldComponent)
            self.disconnect(self.ui.f_cardinalityText, SIGNAL('editTextChanged ( const QString &)'), self.saveFieldComponent)
            self.disconnect(self.ui.valuesTable, SIGNAL('cellChanged(int, int)'), self.saveFieldComponent)

    def resetInternals(self):
        self.currentLayer = None
        self.currentFields = []
        self.nodataValues = []
        self.savedState = False

    def resetGlobal(self):
        self.ui.fc_nameText.clear()
        self.ui.fc_scopeText.clear()
        self.ui.fc_versionNbText.clear()
        self.ui.ft_nameText.clear()
        self.ui.ft_definitionText.clear()

    def resetFields(self):
        self.ui.currentFieldBox.clear()
        self.ui.f_typeText.setCurrentIndex(-1)
        self.ui.f_nameText.clear()
        self.ui.f_definitionText.clear()
        self.ui.f_cardinalityText.setCurrentIndex(-1)
        self.ui.valuesTable.clear()
        self.updateDataSourceBox(self)

    def updateTemplateFile(self):
        filename = QFileDialog.getOpenFileName(self, \
                "Open XML template file", self.last_used_dir, "Template file (*.xml)")
        if filename:
            self.ui.templateText.setText(filename)
            self.last_used_dir = QFileInfo(filename).absolutePath()
            self.loadTemplateFile()

    def loadTemplateFile(self):
        self.isoDoc = iso19110.iso19110Doc(self.ui.templateText.text())
        self.ui.xmlEditor.setPlainText(self.isoDoc.toString())
        self.resetInternals()
        self.resetGlobal()
        self.resetFields()

    def updateDatasourceBox(self):
        self.ui.dataSourceBox.clear()
        for layer in self.iface.mapCanvas().layers():
            if layer.type() in [QgsMapLayer.VectorLayer, QgsMapLayer.RasterLayer]:
                self.ui.dataSourceBox.addItem(layer.name(), QVariant(layer))
        if self.ui.dataSourceBox.count():     
            self.changeCurrentLayer(0)

    def changeCurrentLayer(self, index = None):
        if index is not None:
            self.currentLayer = self.ui.dataSourceBox.itemData(index).toPyObject()
            # activate attribute table button only for vectors
            if self.currentLayer:
                # self.ui.ft_nameText.setText(self.currentLayer.name())
                if self.currentLayer.type() == QgsMapLayer.VectorLayer:
                    self.ui.attributeTableButton.setEnabled(True)
                else:
                    self.ui.attributeTableButton.setEnabled(False)
        else:
            self.currentLayer = None

    def refreshXML(self):
        # when refresh xml button is hit, update content with internal struct
        if self.isoDoc is not None:
            try:
                # FIXME this should already be ok since we do it entering the tab
                self.isoDoc.updateWithParams(self.getParams())
                self.ui.xmlEditor.setPlainText(self.isoDoc.toString())
            except ValueError, e:
                QMessageBox.critical(self, "Error", e.message)

    def updateIsoDocFromXml(self):
        if self.isoDoc:
            try:
                # iso doc is set from xml
                self.isoDoc.updateWithXmlContent(self.ui.xmlEditor.toPlainText())
                params = self.isoDoc.extractParamsFromContent()
                if params['fields']:
                    self.currentFields = params['fields']
                #self.isoDoc.updateWithParams(self.getParams())
                # rewrite editor content to the one from internal struct
                self.ui.xmlEditor.setPlainText(self.isoDoc.toString())
                self.savedState = False
            except IOError, e:
                self.ui.xmlEditor.setText("Error parsing/reading XML: %s" % e.message)
            except ValueError, e:
                self.ui.xmlEditor.setText("Error parsing/reading XML: %s" % e.message)


    def tabChanged(self, tabIndex):
        # when tab changes, we set internal values to the ones from the xml content
        # do we go out of XML tab ?
        # FIXME : we should only do that when going out of xml tab
        # when we go to the XML tab, we update iso doc with current data from other tabs
        if tabIndex == 0:
            try:
                self.isoDoc.updateWithParams(self.getParams())
            except ValueError, e:
                QMessageBox.critical(self, "Error", e.message)
        elif self.isoDoc:
            self.updateIsoDocFromXml()

    def loadFieldsFromXML(self):
        # XML internal is up to date compared to XML in widget
        # as soon as we get out of XML tab
        try:
            params = self.isoDoc.extractParamsFromContent()
            if params['fields']:
                self.currentFields = params['fields']
        except IOError, e:
            QMessageBox.warning(self, "Error parsing/reading XML",\
                    "Error parsing/reading XML: %s" % e.message)
        except ValueError, e:
            QMessageBox.warning(self, "Error parsing/reading XML",\
                    "Error parsing/reading XML: %s" % e.message)
    
    def updateVectorFieldList(self):
        # clear internal representation
        self.currentFields = []
        # clear combo box
        self.ui.currentFieldBox.clear()
        # get field list from data provider
        if self.currentLayer:
            columns = self.currentLayer.dataProvider().fields()
            for index, column in columns.items():
                # populate internal representation
                field = {
                        'index': index,
                        'name': column.name(),
                        'type': column.typeName(),
                        'definition': column.comment(),
                        'cardinality': '0..1',
                        'values' : []
                        }
                self.currentFields.append(field)
            # sort list by index key
            self.currentFields.sort(key = lambda k:k['index'])
            # populate combo box with fields in same order
            # call to addItem when box is empty emits currentIndexChanged
            for field in self.currentFields:
                self.ui.currentFieldBox.addItem(field['name'])
            # analyze values for all field if enabled 
            if self.ui.classification.isChecked():
                self.analyzeVectorValues()
            # next instruction will call updateFieldForm slot
            self.ui.currentFieldBox.setCurrentIndex(0)

    def updateRasterFieldList(self):
        self.currentFields = []
        self.ui.currentFieldBox.clear()
        if self.currentLayer:
            # set nodata value from layer
            value, ok = self.currentLayer.noDataValue()
            if ok:
                self.nodataValues = [str(value)]
            # band indexes are 1-based !
            for index in range(1, self.currentLayer.bandCount() + 1):
                field = {
                        'index': index,
                        'name': "%s" % self.currentLayer.bandName(index),
                        'type': "",
                        'definition': "",
                        'cardinality': '1..1',
                        'values' : []
                        }
                self.currentFields.append(field)
            for field in self.currentFields:
                self.ui.currentFieldBox.addItem(field['name'])
            if self.ui.classification.isChecked():
                self.analyzeRasterValues()
            self.ui.currentFieldBox.setCurrentIndex(0)

    def updateFieldList(self):
        if self.currentLayer:
            if self.currentLayer.type() == QgsMapLayer.VectorLayer:
                self.updateVectorFieldList()
            # current layer can only be raster or vector
            else:
                self.updateRasterFieldList()

    def updateFieldForm(self):
        # deactivate signals, otherwise they are messing with value setting
        self.activeFieldForm(False)
        # get selected field if any
        fieldIndex = self.ui.currentFieldBox.currentIndex()
        # nothing in combo box
        if fieldIndex != -1:
            # fill form elements
            self.ui.f_nameText.setText(self.currentFields[fieldIndex]['name'])
            self.ui.f_definitionText.setPlainText(self.currentFields[fieldIndex]['definition'])
            typeIndex = self.ui.f_typeText.findText(\
                    self.currentFields[fieldIndex]['type'], Qt.MatchFixedString)
            if typeIndex == -1:
                if self.currentFields[fieldIndex]['type'] != '':
                    self.ui.f_typeText.insertItem(0, self.currentFields[fieldIndex]['type'])
                    self.ui.f_typeText.setCurrentIndex(0)
            else:
                self.ui.f_typeText.setCurrentIndex(typeIndex)
                
            cardinalityIndex = self.ui.f_cardinalityText.findText(\
                    self.currentFields[fieldIndex]['cardinality'], Qt.MatchFixedString)
            if cardinalityIndex == -1:
                if self.currentFields[fieldIndex]['cardinality'] != '':
                    self.ui.f_cardinalityText.insertItem(0, self.currentFields[fieldIndex]['cardinality'])
                    self.ui.f_cardinalityText.setCurrentIndex(0)
            else:
                self.ui.f_cardinalityText.setCurrentIndex(cardinalityIndex)
                
            # reset values
            values = self.currentFields[fieldIndex]['values']
            self.ui.valuesTable.clearContents()
            self.ui.valuesTable.setRowCount(len(values))
            # fill values in table
            for rownb, value in enumerate(values):
                self.ui.valuesTable.setItem(rownb, 0, QTableWidgetItem(value['label']))
                self.ui.valuesTable.setItem(rownb, 1, QTableWidgetItem(value['code']))
                self.ui.valuesTable.setItem(rownb, 2, QTableWidgetItem(value['definition']))
        # reactivate signals
        self.activeFieldForm(True)

    def saveFieldComponent(self):
        fieldIndex = self.ui.currentFieldBox.currentIndex()
        if fieldIndex != -1:
            currentField = self.currentFields[fieldIndex]
            currentField['type'] = self.ui.f_typeText.currentText()
            currentField['definition'] = self.ui.f_definitionText.toPlainText()
            currentField['cardinality'] = self.ui.f_cardinalityText.currentText()
            # save values from table to internal storage
            currentField['values'] = []
            for rownb in range(self.ui.valuesTable.rowCount()):
                currentField['values'].append(\
                        {'label':self.ui.valuesTable.item(rownb, 0).text(),
                            'code':self.ui.valuesTable.item(rownb, 1).text(),
                            'definition':self.ui.valuesTable.item(rownb, 2).text()})

    def getNodataInput(self):
        nodata, ok = QInputDialog.getText(self, "NODATA values", "Enter NODATA values separated by ';'",
                QLineEdit.Normal, ';'.join(self.nodataValues))
        if ok:
            self.nodataValues = [it for it in str(nodata).strip().split(';') if it != '']

    def analyzeButtonClicked(self):
        self.analyzeCurrentFieldValues()
        self.updateFieldForm()

    def analyzeCurrentFieldValues(self):
        # set index list only for current field
        index_list = [self.ui.currentFieldBox.currentIndex()]
        if self.currentLayer.type() == QgsMapLayer.VectorLayer:
            self.analyzeVectorValues(index_list)
        else:
            self.analyzeRasterValues(index_list)

    def analyzeRasterValues(self, index_list = None):
        # raster data analysis is based on random points
        # in the canvas area
        if self.currentLayer:
            if index_list is None:
                fieldIndexList = [field['index'] for field in self.currentFields]
            else:
                # raster band index is 1-based, whereas index list is 0-based
                fieldIndexList = [i + 1 for i in index_list]
            fieldsValues = {}
            for i in fieldIndexList:
                fieldsValues[i] = {}
            random.seed()
            extent = self.iface.mapCanvas().extent()
            point = QgsPoint()
            valueNb = 0
            while valueNb < self.ui.rowNb.value():
                x = random.random() * extent.width() + extent.xMinimum()
                y = random.random() * extent.height() + extent.yMinimum()
                point.set(x,y)
                success, data = self.currentLayer.identify(point)
                if success and str(data.values()[0]) != 'out of extent':
                    valueNb += 1
                    for fieldName, fieldValue in data.items():
                        if str(fieldValue) not in self.nodataValues:
                            fieldIndex = self.currentLayer.bandNumber(fieldName)
                            if fieldsValues[fieldIndex].has_key(str(fieldValue)):
                                fieldsValues[fieldIndex][str(fieldValue)] += 1
                            else:
                                fieldsValues[fieldIndex][str(fieldValue)] = 1
            # only keep values with count > specified
            # generate a value structure for each field
            for index in fieldIndexList:
                self.currentFields[index - 1]['values'] = [\
                        {'code':key, 'label':'', 'definition':''}\
                        for key, value in fieldsValues[index].items()\
                        if value >= self.ui.requiredValuesNb.value()]

    def analyzeVectorValues(self, index_list = None):
        # get data provider
        if self.currentLayer:
            provider = self.currentLayer.dataProvider()
            fieldIndexList = index_list 
            # set index list for all fields if not given
            if fieldIndexList is None:
                fieldIndexList = [field['index'] for field in self.currentFields]
            # store values for each field, with occurence nb
            fieldsValues = {}
            for i in fieldIndexList:
                fieldsValues[i] = {}
            # select features without geometry
            provider.select(fieldIndexList, QgsRectangle(), False)
            feat = QgsFeature()
            # iterate over a limited number of features
            for rownb in range(self.ui.rowNb.value()):
                if provider.nextFeature(feat):
                    # for each field set value as dictionnary key and
                    # increment value count if already found
                    for fieldIndex, fieldValue in feat.attributeMap().items():
                        if fieldsValues[fieldIndex].has_key(fieldValue.toString()):
                            fieldsValues[fieldIndex][fieldValue.toString()] += 1
                        else:
                            fieldsValues[fieldIndex][fieldValue.toString()] = 1
                else:
                    # no more feature, go out 
                    break
            # only keep values with count > specified
            # generate a value structure for each field
            for index in fieldIndexList:
                self.currentFields[index]['values'] = [\
                        {'code':key, 'label':'', 'definition':''}\
                        for key, value in fieldsValues[index].items()\
                        if value >= self.ui.requiredValuesNb.value()]

    def deleteValueRow(self):
        self.ui.valuesTable.removeRow(self.ui.valuesTable.currentRow())

    def newValueRow(self):
        # disconnect signals because we change items one by one
        # and don't want to save components every time
        self.activeFieldForm(False)
        rowcount = self.ui.valuesTable.rowCount()
        self.ui.valuesTable.insertRow(rowcount)
        # initialize table widgets to empty string
        self.ui.valuesTable.setItem(rowcount, 0, QTableWidgetItem(''))
        self.ui.valuesTable.setItem(rowcount, 1, QTableWidgetItem(''))
        self.ui.valuesTable.setItem(rowcount, 2, QTableWidgetItem(''))
        self.saveFieldComponent()
        self.activeFieldForm(True)

    def fillFcForm(self):
        if self.isoDoc:
            # feature catalog properties
            self.ui.fc_nameText.setText(self.isoDoc.getFcName())
            self.ui.fc_scopeText.setPlainText(self.isoDoc.getFcScope())
            self.ui.fc_versionNbText.setText(self.isoDoc.getFcVersionNumber())

    def fillFtForm(self):
        if self.isoDoc:
            # Feature type properties
            self.ui.ft_nameText.setText(self.isoDoc.getFtName())
            self.ui.ft_definitionText.setPlainText(self.isoDoc.getFtDefinition())

    def getParams(self):
        params = {}
        params['fc_name'] = self.ui.fc_nameText.text()
        params['fc_scope'] = self.ui.fc_scopeText.toPlainText()
        params['fc_versionNumber'] = self.ui.fc_versionNbText.text()
        params['ft_name'] = self.ui.ft_nameText.text()
        params['ft_definition'] = self.ui.ft_definitionText.toPlainText()
        params['fields'] = self.currentFields
        return params

    def updateFormWithParams(self, params):
        # set values
        self.ui.fc_nameText.setText(params['fc_name'])
        self.ui.fc_scopeText.setPlainText(params['fc_scope'])
        self.ui.fc_versionNbText.setText(params['fc_versionNumber'])
        self.ui.ft_nameText.setText(params['ft_name'])
        self.ui.ft_definitionText.setPlainText(params['ft_definition'])
        self.currentFields = params['fields']
        self.updateFieldForm()

    def saveXML(self):
        xmlViewContent = self.ui.xmlEditor.toPlainText()
        xmlViewContentCanBeSaved = False
        
        if not self.isoDoc:
            QMessageBox.critical(self, "Error", "An iso 191110 template need to be selected first.")
        elif xmlViewContent is None or xmlViewContent.isEmpty():
            QMessageBox.critical(self, "Error", "The content of the XML view is empty. It must contain an XML iso19110 document.")
        else:
            try:
                # If the tab of the XML view is not active refresh the XML view
                if self.ui.tabWidget.currentIndex() != 2:
                    self.isoDoc.updateWithXmlContent(xmlViewContent)
                    self.isoDoc.updateWithParams(self.getParams())
                    self.ui.xmlEditor.setPlainText(self.isoDoc.toString())
                else:
                    self.isoDoc.updateWithXmlContent(xmlViewContent)
                    self.ui.xmlEditor.setPlainText(self.isoDoc.toString())
                    
                xmlViewContentCanBeSaved = True
            except ValueError, e:
                QMessageBox.critical(self, "Error", e.message)
        
        if xmlViewContentCanBeSaved:
            # Initialize the file path with the one used the last time
            filePath = QFileDialog.getSaveFileName(self, \
                    "Save XML feature catalog file", self.last_used_dir, "XML file (*.xml)")
            
            # Save the content of the XML view in a file if the isoDoc exists and if the user
            # selected a valid path
            if filePath:
                self.last_used_dir = QFileInfo(filePath).absolutePath()
                self.isoDoc.save(filePath)
                self.savedState = True


    def bboxClicked(self, button):
        if self.ui.buttonBox.standardButton(button) == QDialogButtonBox.Close:
            if self.savedState is False:
                res = QMessageBox.warning(self, "Feature Catalog Creator",
                        "The document has been modified.\nDo you really want to close ?",
                        QMessageBox.Cancel | QMessageBox.Ok,
                        QMessageBox.Cancel)
                if res == QMessageBox.Ok:
                    self.saveSettings()
                    self.close()
            else:
                self.saveSettings()
                self.close()
