#/***************************************************************************
# featureCatCreator
#                                 A QGIS plugin
#    Generates, for a selected datasource, a feature catalogue metadata
#    record in XML format compliant with ISO19110 standard.
#    This project has been funded by the EEA (European Environment Agency) :
#    http://www.eea.europa.eu
#    The project has been developped by Neogeo and Oslandia :
#    http://www.neogeo-online.net/
#    http://www.oslandia.com
#                             -------------------
#        begin                : 2012-01-17
#        copyright            : (C) 2012 Neogeo & Oslandia, funded by EEA
#        email                : vincent.picavet@oslandia.com
# ***************************************************************************/
#
#/***************************************************************************
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU General Public License as published by  *
# *   the Free Software Foundation; either version 2 of the License, or     *
# *   (at your option) any later version.                                   *
# *                                                                         *
# ***************************************************************************/

# Makefile for a PyQGIS plugin 

PLUGINNAME = featurecatcreator

PY_FILES = featurecatcreator.py featurecatcreatordialog.py __init__.py iso19110.py

EXTRAS = icon.png mActionOpenTable.png

UI_FILES = ui_featurecatcreator.py

RESOURCE_FILES = resources_rc.py

HELP_FILES = help

default: compile

compile: $(UI_FILES) $(RESOURCE_FILES)

%_rc.py : %.qrc
	pyrcc4 -o $@  $<

%.py : %.ui
	pyuic4 -o $@ $<

# The deploy  target only works on unix like operating system where
# the Python plugin directory is located at:
# $HOME/.qgis/python/plugins
deploy: compile
	mkdir -p $(HOME)/.qgis/python/plugins/$(PLUGINNAME)
	cp -vf $(PY_FILES) $(HOME)/.qgis/python/plugins/$(PLUGINNAME)
	cp -vf $(UI_FILES) $(HOME)/.qgis/python/plugins/$(PLUGINNAME)
	cp -vf $(RESOURCE_FILES) $(HOME)/.qgis/python/plugins/$(PLUGINNAME)
	cp -vf $(EXTRAS) $(HOME)/.qgis/python/plugins/$(PLUGINNAME)
	cp -vfr $(HELP_FILES) $(HOME)/.qgis/python/plugins/$(PLUGINNAME)
	find $(HOME)/.qgis/python/plugins/$(PLUGINNAME) -type d -iname ".svn" -prune -exec rm -fr {} \;

# Create a zip package of the plugin named $(PLUGINNAME).zip. 
# This requires use of git (your plugin development directory must be a 
# git repository).
# To use, pass a valid commit or tag as follows:
#   make package VERSION=Version_0.3.2
package: compile
		rm -f $(PLUGINNAME).zip
		git archive --prefix=$(PLUGINNAME)/ -o $(PLUGINNAME).zip $(VERSION)
		echo "Created package: $(PLUGINNAME).zip"
