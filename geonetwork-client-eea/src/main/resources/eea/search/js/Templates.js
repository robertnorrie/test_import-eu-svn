/*
 * Copyright (C) 2001-2011 Food and Agriculture Organization of the
 * United Nations (FAO-UN), United Nations World Food Programme (WFP)
 * and United Nations Environment Programme (UNEP)
 * 
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or (at
 * your option) any later version.
 * 
 * This program is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
 * General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301, USA
 * 
 * Contact: Jeroen Ticheler - FAO - Viale delle Terme di Caracalla 2,
 * Rome - Italy. email: geonetwork@osgeo.org
 */
Ext.namespace('GeoNetwork');


GeoNetwork.lang.en["webdavLink"] = "WebDAV (Web-based Distributed Authoring and Versioning) link";
GeoNetwork.lang.en["cifsLink"] = "CIFS (Common Internet File System) link";
GeoNetwork.lang.en["ftpsLink"] = "FTPS link";

/** api: (define)
 *  module = GeoNetwork
 *  class = Templates
 *  base_link = `Ext.XTemplate <http://extjs.com/deploy/dev/docs/?class=Ext.XTemplate>`_
 */
EEA.Templates = Ext.extend(Ext.XTemplate, {
    compiled: false,
    disableFormats: false,
    catalogue : null,
    sortOrder: 0,
    abstractMaxSize : 50,
    xmlTplMarkup : [
                    '<?xml version="1.0" encoding="UTF-8"?>',
                    '<node id="{id}" type="{type}">',
                        '<site>',
                            '<name>{site_name}</name>',
                            '<tpl if="values.site_ogctype">',
                                '<ogctype>{site_ogctype}</ogctype>',
                            '</tpl>',
                            '<tpl if="values.site_url">',
                                  '<url>{site_url}</url>',
                            '</tpl>',
                            '<tpl if="values.site_icon">',
                                  '<icon>{site_icon}</icon>',
                            '</tpl>',
                            '<tpl if="values.site_account_use">',
                                '<account>',
                                  '<use>{site_account_use}</use>',
                                  '<username>{site_account_username}</username>',
                                  '<password>{site_account_password}</password>',
                                  '</account>',
                            '</tpl>',
                        '</site>',
                        '<options>',
                              '<tpl if="values.options_every">',
                                  '<every>{options_every}</every>',
                              '</tpl>',
                              '<tpl if="values.options_onerunonly">',
                                  '<oneRunOnly>{options_onerunonly}</oneRunOnly>',
                              '</tpl>',
                              '<tpl if="values.options_lang">',
                                  '<lang>{options_lang}</lang>',
                              '</tpl>',
                              '<tpl if="values.options_topic">',
                                  '<topic>{options_topic}</topic>',
                              '</tpl>',
                              '<tpl if="values.options_createthumbnails">',
                                  '<createThumbnails>{options_createthumbnails}</createThumbnails>',
                              '</tpl>',
                              '<tpl if="values.options_uselayer">',
                                  '<useLayer>{options_uselayer}</useLayer>',
                              '</tpl>',
                              '<tpl if="values.options_uselayermd">',
                                  '<useLayerMd>{options_uselayermd}</useLayerMd>',
                              '</tpl>',
                              '<tpl if="values.options_datasetcategory">',
                                  '<datasetcategory>{options_datasetcategory}</datasetcategory>',
                              '</tpl>',
                        '</options>',
                        '<content>',
                        '</content>',
                        '<privileges>',
                        '</privileges>',
                            '<group id="1">',
                                '<operation name="view" />',
                                '<operation name="dynamic" />',
                            '</group>',
                        '<categories>',
                        '</categories>',
                        '<tpl if="values.info_result_total">',
                        '</tpl>',
                    '</node>'
                    // TODO : other properties - display if available depends on harvester
                ],
    initComponent: function() {
        GeoNetwork.Templates.superclass.initComponent.call(this);
    },
    /** api: method[getHarvesterTemplate]
     *
     *  :return: A template for harvester configuration
     */    
    getHarvesterTemplate: function() {
        return new Ext.XTemplate(this.xmlTplMarkup);
    }
});


EEA.Templates.TITLE = '<h1><input type="checkbox" <tpl if="selected==\'true\'">checked="true"</tpl> class="selector" onclick="javascript:app.getCatalogue().metadataSelect((this.checked?\'add\':\'remove\'), [\'{uuid}\']);"/><a href="#" onclick="javascript:app.getCatalogue().metadataShow(\'{uuid}\');return false;">{title}</a>' + 
                                '<span class="md-action-menu"> - <a rel="mdMenu">' + OpenLayers.i18n('mdMenu') + '</a></span></h1>';
EEA.Templates.RATING_TPL = '<tpl if="isharvested==\'n\' || harvestertype==\'geonetwork\'"><div class="rating">' +
                                           '<input type="radio" name="rating{[xindex]}" <tpl if="rating==\'1\'">checked="true"</tpl> value="1"/>' + 
                                           '<input type="radio" name="rating{[xindex]}" <tpl if="rating==\'2\'">checked="true"</tpl> value="2"/>' + 
                                           '<input type="radio" name="rating{[xindex]}" <tpl if="rating==\'3\'">checked="true"</tpl> value="3"/>' +
                                           '<input type="radio" name="rating{[xindex]}" <tpl if="rating==\'4\'">checked="true"</tpl> value="4"/>' +
                                           '<input type="radio" name="rating{[xindex]}" <tpl if="rating==\'5\'">checked="true"</tpl> value="5"/>' + 
                                       '</div></tpl>'; 
EEA.Templates.LOGO = '<div class="md-logo"><img src="{[app.getCatalogue().URL]}/images/logos/{source}.gif"/></div>';
/** api: constructor 
 *  .. class:: GeoNetwork.Templates.SIMPLE()
 * 
 *   An instance of a pre-configured GeoNetwork.Templates with title and 
 *   keywords with abstract in tooltip.
 */
EEA.Templates.SIMPLE = new Ext.XTemplate(
    '<ul>',
        '<tpl for=".">',
            '<li class="md md-simple" id="md{uuid}" title="{abstract}">',
                '<table><tr><td style="width:30px;">',  // FIXME
                GeoNetwork.Templates.LOGO,
                '</td><td id="{uuid}">',
                GeoNetwork.Templates.TITLE,
                '<tpl if="subject">',
                    '<span class="subject"><tpl for="subject">',
                        '{value}{[xindex==xcount?"":", "]}',
                    '</tpl></span>',
                '</tpl>',
                '</td></tr></table>',
            '</li>',
        '</tpl>',
    '</ul>'
);



/** api: constructor 
 *  .. class:: GeoNetwork.Templates.THUMBNAIL()
 * 
 *   An instance of a pre-configured GeoNetwork.Templates with thumbnail view
 */
EEA.Templates.THUMBNAIL = new Ext.XTemplate(
        '<ul>',
            '<tpl for=".">',
                '<li class="md md-thumbnail" id="md{uuid}">',
                '<div class="md-wrap" id="{uuid}" title="{abstract}">',
                    GeoNetwork.Templates.TITLE,
                    '<div class="thumbnail">',
                        '<tpl if="thumbnail">',
                            '<a rel="lightbox" href="{thumbnail}"><img src="{thumbnail}" alt="Thumbnail"/></a>', 
                        '</tpl>',
                        '<tpl if="thumbnail==\'\'"></tpl>',
                    '</div>',
                    '<tpl for="links">',
                    '<tpl if="values.type == \'application/vnd.ogc.wms_xml\'">',
                    // FIXME : ref to app
                        '<a href="#" class="md-mn addLayer" title="{title}" alt="{title}" onclick="app.switchMode(\'1\', true);app.getIMap().addWMSLayer([[\'{title}\', \'{href}\', \'{name}\', \'{id}\']]);">&nbsp;</a>',
                    '</tpl>',
                    '</tpl>',
                '</div>',
                '</li>',
            '</tpl>',
        '</ul>'
    );


/** api: constructor 
 *  .. class:: GeoNetwork.Templates.FULL()
 * 
 *  FIXME : catalogue.URL suppose that a global var named catalogue is available.
 * 
 *   An instance of a pre-configured GeoNetwork.Templates with full view
 */
EEA.Templates.FULL = new Ext.XTemplate(
        '<ul>',
          '<tpl for=".">',
            '<li class="md md-full">',
                '<table><tr>',
                '<td class="left">',
                    EEA.Templates.LOGO,
                '</td>',
                '<td id="{uuid}">',
                    EEA.Templates.TITLE,
                    '<p class="abstract">{[values.abstract.substring(0, 350)]} ...</p>',    // FIXME : 250 as parameters
                    '<tpl if="subject">',
                        '<p class="subject"><tpl for="subject">',
                            '{value}{[xindex==xcount?"":", "]}',
                        '</tpl></p>',
                    '</tpl>',
                    '<div class="md-links">',
                    // FIXME : this call require the catalogue to be named catalogue, static call ?
                    // FIXME : ref to app
                        '<a href="?uuid={uuid}" class="md-mn mdLinkIcon" title="' + OpenLayers.i18n('permalink') + ' {title}" alt="Metadata permalink" target="_blank">&nbsp;</a>',
                        '<tpl for="links">',
                            '<tpl if="values.type == \'application/vnd.ogc.wms_xml\' || values.type == \'OGC:WMS\'">',
                                '<a href="#" class="md-mn addLayer" title="' + OpenLayers.i18n('addToMap') + ' {title}" alt="Add layer to map" onclick="app.switchMode(\'1\', true);app.getIMap().addWMSLayer([[\'{[escape(values.title)]}\', \'{href}\', \'{name}\', \'{id}\']]);">&nbsp;</a>',
                            '</tpl>',
                            '<tpl if="values.type == \'application/vnd.google-earth.kml+xml\'">',
                                '<a href="{href}" class="md-mn md-mn-kml" title="' + OpenLayers.i18n('viewKml') + ' {title}" alt="Open kml">&nbsp;</a>',
                            '</tpl>',
                            '<tpl if="values.type == \'application/zip\' || values.type == \'application/x-compressed\'">',
                                '<a href="{href}" class="md-mn md-mn-zip" title="' + OpenLayers.i18n('downloadLink') + ' {title}" alt="Download">&nbsp;</a>',
                            '</tpl>',
                            '<tpl if="values.type == \'text/html\'">',
                                '<a href="{href}" class="md-mn md-mn-www" title="' + OpenLayers.i18n('webLink') + ' {title}" alt="Web link" target="_blank">&nbsp;</a>',
                            '</tpl>',
//                            '<tpl if="values.type == \'EEA:FILEPATH\'">',
//                                '<a href="' + EEA.MAPVIEWER_URL + '{uuid}" class="md-mn addLayer" title="' + OpenLayers.i18n('addToMap') + ' {title}" alt="EEA link" target="_blank">&nbsp;</a>',
//                            '</tpl>',
                            '<tpl if="values.type == \'EEA:FILEPATH\' || values.type == \'EEA:FOLDERPATH\'">',
                            	'<a href="' + EEA.WEBDAV_URL + '{href}" class="md-mn md-mn-webdav with-tooltip" target="_blank" title="' + OpenLayers.i18n('webdavLink') + ' {title}" alt="EEA webdav link" target="_blank">&nbsp;</a>',
	                        '</tpl>',
	                        '<tpl if="values.type == \'EEA:FILEPATH\' || values.type == \'EEA:FOLDERPATH\'">',
		                    // replace / by \ TODO
	                        '<a href="' + EEA.CIFS_URL + '{href}" class="md-mn md-mn-cifs with-tooltip" target="_blank" title="' + OpenLayers.i18n('cifsLink') + ' {title}" alt="EEA cifs link" target="_blank">&nbsp;</a>',
		                    '</tpl>',
		                    '<tpl if="values.type == \'EEA:FILEPATH\' || values.type == \'EEA:FOLDERPATH\'">',
                                '<a href="' + EEA.FTPS_URL + '{href}" class="md-mn md-mn-ftps with-tooltip" target="_blank" title="' + OpenLayers.i18n('ftpsLink') + ' {title}" alt="EEA ftps link" target="_blank">&nbsp;</a>',
                            '</tpl>',
                            // FIXME : no else ops, how to display other links ?
                        //'|<a href="#" onclick="app.getIMap().addWMSLayer([[\'{title}\', \'{href}\', \'{name}\', \'{id}\']]);">{type}</a>',
                        '</tpl>',
                        '<tpl if="this.hasDownloadLinks(values.links)">',//type == \'application/vnd.ogc.wms_xml\'">',
                            '<a href="#" onclick="app.getCatalogue().metadataPrepareDownload({id});" class="md-mn downloadAllIcon" title="' + OpenLayers.i18n('prepareDownload') + '" alt="download">&nbsp;</a>',
                        '</tpl>',
                        '<tpl if="this.hasEEALinks(values.links)">',//type == \'application/vnd.ogc.wms_xml\'">',
                            '<a href="' + EEA.MAPVIEWER_URL + '{uuid}" class="md-mn addLayer" target="_blank" title="' + OpenLayers.i18n('addToMap') + ' {title}" alt="EEA link" target="_blank">&nbsp;</a>',                        
                        '</tpl>',
                        //'<div id="md-link-info{id}"><input type="text" value=""/></div>',
                    '</div>',
                '</td><td class="thumb">',
//                        GeoNetwork.Templates.RATING_TPL,
                        '<div class="thumbnail">',
                            '<tpl if="thumbnail">',
                                '<a rel="lightbox" href="{thumbnail}"><img src="{thumbnail}" alt="Thumbnail"/></a>', 
                            '</tpl>',
                            '<tpl if="thumbnail==\'\'"></tpl>',
                        '</div>',
                '</td><td class="icon">',
                // Validity and category information
                '<div class="md-mn valid-{valid}" title="' + OpenLayers.i18n('validityInfo'),
                    '<tpl for="valid_details">',
                      '{values.type}: ',
                        '<tpl if="values.valid == \'1\'">' + OpenLayers.i18n('valid')  + '</tpl>',
                        '<tpl if="values.valid == \'0\'">' + OpenLayers.i18n('notValid')  + '</tpl>',
                        '<tpl if="values.valid == \'-1\'">' + OpenLayers.i18n('notDetermined')  + '</tpl>',
                        '<tpl if="values.ratio != \'\'"> ({values.ratio}) </tpl> - ',
                    '</tpl>',
                '">&nbsp;</div>',
                '</td><td class="icon" title="' + OpenLayers.i18n('metadataCategories') + '">',
                '<tpl for="category">',
                  '<div class="md-mn cat-{value}" title="{value}">&nbsp;</div>',
                '</tpl>',
                '</td></tr></table>',
                '<div class="relation" title="' + OpenLayers.i18n('relateddatasets') + '"><span></span><ul id="md-relation-{id}"></ul></div>',
                '<div class="md-contact">',
                  '<tpl for="contact">',
                      // metadata contact are not displayed.
                      '<tpl if="applies==\'resource\'">',
                          '<span title="{role} - {applies}"><tpl if="values.logo !== undefined && values.logo !== \'\'">',
                              '<img src="{logo}" class="orgLogo"/>',
                          '</tpl>',
                          '{name}&nbsp;&nbsp;</span>',
                      '</tpl>',
                  '</tpl>',
                  '<tpl if="edit==\'true\' && isharvested!=\'y\'">',
                      '<br/><span class="md-mn md-mn-user" title="' + OpenLayers.i18n('ownerName') + '">{ownername} (' + OpenLayers.i18n('lastUpdate') + '{[values.changedate.split(\'T\')[0]]})</span>',
                  '</tpl>',
                '</div>',
            '</li>',
        '</tpl>',
    '</ul>',
    {
        hasDownloadLinks: function(values) {
            var i;
            for (i = 0; i < values.length; i ++) {
                if (values[i].type === 'application/x-compressed') {
                    return true;
                }
            }
            return false;
        },
        hasEEALinks: function(values) {
            var i;
            for (i = 0; i < values.length; i ++) {
                if (values[i].type === 'EEA:DBPG') {
                    return true;
                } else if (values[i].type === 'EEA:FILEPATH' && 
                        (values[i].href.indexOf('.mdb') == -1 && values[i].href.indexOf('.gdb') == -1)) {
                    return true;
                }
            }
            return false;
        }
    }
);
