# -*- coding: utf-8 -*-
"""
/***************************************************************************
 metadataCreatorDialog
                                 A QGIS plugin
 Select a datasource and generates a metadata record for the feature catalogue using the ISO19110 standard in XML format.
                             -------------------
        begin                : 2012-01-17
        copyright            : (C) 2012 by Vincent Picavet (Oslandia) for EEA
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

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

from ui_metadatacreator import Ui_metadataCreator
import iso19110

# create the dialog for zoom to point
class metadataCreatorDialog(QDialog):
    def __init__(self, iface):
        QDialog.__init__(self)
        # keep qgis interface reference
        self.iface = iface
        self.currentLayer = None
        self.currentFields = []

        # Set up the user interface from Designer.
        self.ui = Ui_metadataCreator()
        self.ui.setupUi(self)

        # update data source combobox content
        self.updateDatasourceBox()

        # update initial field list
        self.updateFieldList()

        # connect browse button to file search dialog
        self.connect(self.ui.browseTemplateButton, SIGNAL('clicked()'), self.updateTemplateFile)
        # change current layer
        self.connect(self.ui.dataSourceBox, SIGNAL('currentIndexChanged(int)'), self.changeCurrentLayer)

        # when tab change to attribute tab, reset field list
        self.connect(self.ui.tabWidget, SIGNAL('currentChanged(int)'), self.tabChanged)
        # when refresh button is clicked, reload field list
        self.connect(self.ui.refreshButton, SIGNAL('clicked()'), self.updateFieldList)
        # when current field changes, fill form
        self.connect(self.ui.currentFieldBox, SIGNAL('currentIndexChanged(int)'), self.updateFieldForm)
        # when one of the field form element is finished editing, 
        # then save to internal field struct
        self.connect(self.ui.f_typeText, SIGNAL('editingFinished()'), self.saveFieldComponent)
        self.connect(self.ui.f_definitionText, SIGNAL('textChanged()'), self.saveFieldComponent)
        self.connect(self.ui.f_cardinalityText, SIGNAL('editingFinished()'), self.saveFieldComponent)

    
    def updateTemplateFile(self):
        filename = QFileDialog.getOpenFileName(self, \
                "Open XML template file", "", "Template file (*.xml)")
        if filename:
            self.ui.templateText.setText(filename)

    def updateDatasourceBox(self):
        self.ui.dataSourceBox.clear()
        for layer in self.iface.mapCanvas().layers():
            self.ui.dataSourceBox.addItem(layer.name(), QVariant(layer))
        if self.ui.dataSourceBox.count():     
            self.changeCurrentLayer(0)

    def changeCurrentLayer(self, index = None):
        if index is not None:
            self.currentLayer = self.ui.dataSourceBox.itemData(index).toPyObject()
        else:
            self.currentLayer = None

    def tabChanged(self, tabIndex):
        # do we focus on Fields tab ?
        if tabIndex == 2:
            self.updateFieldList()

    def updateFieldList(self):
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
                        'definition': "",
                        'cardinality': "",
                        'values' : []
                        }
                self.currentFields.append(field)
            # sort list by index key
            self.currentFields.sort(key = lambda k:k['index'])
            # populate combo box with fields in same order
            # call to addItem when box is empty emits currentIndexChanged
            for field in self.currentFields:
                self.ui.currentFieldBox.addItem(field['name'])
            # next instruction will call updateFieldForm slot
            self.ui.currentFieldBox.setCurrentIndex(0)
            # update field form
            self.updateFieldForm()    

    def updateFieldForm(self):
        # get selected field if any
        fieldIndex = self.ui.currentFieldBox.currentIndex()
        # nothing in combo box
        if fieldIndex != -1:
            # fill form elements
            self.ui.f_nameText.setText(self.currentFields[fieldIndex]['name'])
            self.ui.f_definitionText.setPlainText(self.currentFields[fieldIndex]['definition'])
            self.ui.f_typeText.setText(self.currentFields[fieldIndex]['type'])
            self.ui.f_cardinalityText.setText(self.currentFields[fieldIndex]['cardinality'])
            # TODO : check value model
            # reset values
            # self.ui.valuesTable.clear()
            # self.ui.valuesTable.addItems(self.currentFields[fieldIndex]['values'])

    def saveFieldComponent(self):
        fieldIndex = self.ui.currentFieldBox.currentIndex()
        if fieldIndex != -1:
            self.currentFields[fieldIndex]['type'] = self.ui.f_typeText.text()
            self.currentFields[fieldIndex]['definition'] = self.ui.f_definitionText.toPlainText()
            self.currentFields[fieldIndex]['cardinality'] = self.ui.f_cardinalityText.text()
            # TODO : save values

    def analyzeValues(self, field):
        pass

    def updateValueList(self, values):
        pass

    def delCurrentValue(self):
        pass

    def addNewValue(self):
        pass

    def generateXML(self):
        params = {}
        params['fc_name'] = ui.fc_nameText.text()
        params['fc_scope'] = ui.fc_scopeText.text()
        params['fc_versionNumber'] = ui.fc_versionNbText.text()
        params['ft_name'] = ui.ft_nameText.text()
        params['ft_definition'] = ui.ft_definitionText.text()
        params['fields'] = self.fields 
        return iso19110.generateXML(self.ui.templateText.text(), params)

    def saveXML(self):
        pass


        


