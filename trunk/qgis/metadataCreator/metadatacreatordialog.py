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

        # connect browse button to file search dialog
        self.connect(self.ui.browseTemplateButton, SIGNAL('clicked()'), self.updateTemplateFile)
        # change current layer
        self.connect(self.ui.dataSourceBox, SIGNAL('currentIndexChanged(int)'), self.changeCurrentLayer)

        # when tab change to attribute tab, reset field list
        self.connect(self.ui.tabWidget, SIGNAL('currentChanged(int)'), self.tabChanged)
        # when refresh button is clicked, reload field list
        self.connect(self.ui.refreshButton, SIGNAL('clicked()'), self.updateFieldList)
    
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
        columns = self.currentLayer.dataProvider().fields()
        for index, column in columns.items():
            # populate internal representation
            field = {
                    'index': index,
                    'name': column.name(),
                    'type': column.typeName(),
                    'description': "",
                    'cardinality': "",
                    'values' : []
                    }
            self.currentFields.append(field)
        # sort by index key
        self.currentFields.sort(key = lambda k:k['index'])
        # populate combo box with fields in same order
        for field in self.currentFields:
            self.ui.currentFieldBox.addItem(field['name'], field['index'])

    def updateFieldForm(self):
        pass

    def saveFieldComponent(self):
        pass

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


        


