# -*- coding: utf-8 -*-
"""
/***************************************************************************
 featureCatCreator
                                 A QGIS plugin
    Generates, for a selected datasource, a feature catalogue metadata record in XML format compliant with ISO19110 standard.
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

from ui_featurecatcreator import Ui_featureCatCreator
import iso19110

# create the dialog for zoom to point
class featureCatCreatorDialog(QDialog):
    def __init__(self, iface):
        QDialog.__init__(self)
        # keep qgis interface reference
        self.iface = iface
        self.currentLayer = None
        self.currentFields = []

        # Set up the user interface from Designer.
        self.ui = Ui_featureCatCreator()
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
        # attribute field form are active. connect them
        self.activeFieldForm(True)
        # values elements
        self.connect(self.ui.newValueButton, SIGNAL('clicked()'), self.newValueRow)
        self.connect(self.ui.deleteValueButton, SIGNAL('clicked()'), self.deleteValueRow)

    def activeFieldForm(self, connect = True):
        if connect:
            # when one of the field form element is finished editing, 
            # then save to internal field struct
            self.connect(self.ui.f_typeText, SIGNAL('editingFinished()'), self.saveFieldComponent)
            self.connect(self.ui.f_definitionText, SIGNAL('textChanged()'), self.saveFieldComponent)
            self.connect(self.ui.f_cardinalityText, SIGNAL('editingFinished()'), self.saveFieldComponent)
            self.connect(self.ui.valuesTable, SIGNAL('cellChanged(int, int)'), self.saveFieldComponent)
        else:
            self.disconnect(self.ui.f_typeText, SIGNAL('editingFinished()'), self.saveFieldComponent)
            self.disconnect(self.ui.f_definitionText, SIGNAL('textChanged()'), self.saveFieldComponent)
            self.disconnect(self.ui.f_cardinalityText, SIGNAL('editingFinished()'), self.saveFieldComponent)
            self.disconnect(self.ui.valuesTable, SIGNAL('cellChanged(int, int)'), self.saveFieldComponent)

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
        self.updateFieldList()

    def tabChanged(self, tabIndex):
        # do we focus on Fields tab ?
        if tabIndex == 2:
            pass
            #self.updateFieldList()
        elif tabIndex == 3:
            try:
                self.ui.xmlEditor.setText(self.generateXML())
            # FIXME : raise and catch only relevant exceptions
            except Exception, e:
                self.ui.xmlEditor.setText("Error generating XML : %s" % e.message)


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
                        'definition': column.comment(),
                        'cardinality': "",
                        'values' : []
                        }
                self.analyzeValues(field)
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
            #self.updateFieldForm()    

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
            self.ui.f_typeText.setText(self.currentFields[fieldIndex]['type'])
            self.ui.f_cardinalityText.setText(self.currentFields[fieldIndex]['cardinality'])
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
            currentField['type'] = self.ui.f_typeText.text()
            currentField['definition'] = self.ui.f_definitionText.toPlainText()
            currentField['cardinality'] = self.ui.f_cardinalityText.text()
            # save values from table to internal storage
            currentField['values'] = []
            for rownb in range(self.ui.valuesTable.rowCount()):
                currentField['values'].append(\
                        {'label':self.ui.valuesTable.item(rownb, 0).text(),
                            'code':self.ui.valuesTable.item(rownb, 1).text(),
                            'definition':self.ui.valuesTable.item(rownb, 2).text()})

    def analyzeValues(self, field):
        # TODO implement real function
        field['values'] = [{'label':"test1", 'code':"code1", 'definition':"def1"},
                {'label':"test2", 'code':"code2", 'definition':"def2"},
                {'label':"test3", 'code':"code3", 'definition':"def3"}]

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

    def generateXML(self):
        params = {}
        params['fc_name'] = self.ui.fc_nameText.text()
        params['fc_scope'] = self.ui.fc_scopeText.toPlainText()
        params['fc_versionNumber'] = self.ui.fc_versionNbText.text()
        params['ft_name'] = self.ui.ft_nameText.text()
        params['ft_definition'] = self.ui.ft_definitionText.toPlainText()
        params['fields'] = self.currentFields 
        return iso19110.generateXML(self.ui.templateText.text(), params)

    def saveXML(self):
        pass


        


