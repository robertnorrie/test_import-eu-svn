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
def name():
    return "ISO19110 feature catalogue metadata creator"
def description():
    return "Generates, for a selected datasource, a feature catalogue metadata record in XML format compliant with ISO19110 standard."
def version():
    return "Version 0.1"
def icon():
    return "icon.png"
def qgisMinimumVersion():
    return "1.0"
def classFactory(iface):
    # load featureCatCreator class from file featureCatCreator
    from featurecatcreator import featureCatCreator 
    return featureCatCreator(iface)
