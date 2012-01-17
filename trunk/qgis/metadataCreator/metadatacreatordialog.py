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

from PyQt4 import QtCore, QtGui
from ui_metadatacreator import Ui_metadataCreator
# create the dialog for zoom to point
class metadataCreatorDialog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_metadataCreator()
        self.ui.setupUi(self)
