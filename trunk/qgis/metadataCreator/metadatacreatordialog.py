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
        # Set up the user interface from Designer.
        self.ui = Ui_metadataCreator()
        self.ui.setupUi(self)

        # update data source combobox content
        self.updateDatasourceBox()
    
    def updateDatasourceBox(self):
        pass

    def updateFieldList(self):
        pass

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


        


