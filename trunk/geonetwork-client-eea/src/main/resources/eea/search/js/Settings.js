GeoNetwork.Settings = {};
EEA = {};
EEA.MAPVIEWER_URL = 'http://swordfish/paul/databrowser/map_default.phtml?resetsession=ALL&uuid=';
EEA.WEBDAV_URL = 'https://gisdata.eea.europa.eu/data/gis_sdi';
EEA.CIFS_URL = 'file:////sandfish/gis_sdi';

// Turn off rating
Ext.ux.RatingItem = undefined;

// Default to absolute path without apps/search
// GeoNetwork.URL = '../..';

//OpenLayers.ProxyHostURL = '/cgi-bin/proxy.cgi?url=';
// GeoNetwork proxy is much more permissive than OL one
OpenLayers.ProxyHostURL = '../../proxy?url=';

OpenLayers.ProxyHost = function(url){
    /**
     * Do not use proxy for local domain.
     * This is required to keep the session activated.
     */
    if (url && url.indexOf(window.location.host) != -1) {
        return url;
    } else {
        return OpenLayers.ProxyHostURL + encodeURIComponent(url);
    }
};


GeoNetwork.Util.defaultLocale = 'en';
// Restrict locales to a subset of languages
//GeoNetwork.Util.locales = [
//            ['fr', 'Français']
//    ];
GeoNetwork.searchDefault = {
    activeMapControlExtent: false
};
GeoNetwork.advancedFormButton = true;

GeoNetwork.Settings.editor = {
    defaultViewMode : 'metadata'
//    defaultViewMode : 'inspire'
};

// Define which type of search to use
// Default mode
//GeoNetwork.Settings.mdStore = GeoNetwork.data.MetadataResultsStore;
//GeoNetwork.Settings.searchService='xml.search';
// IndexOnly mode 
GeoNetwork.Settings.mdStore = GeoNetwork.data.MetadataResultsFastStore;
GeoNetwork.Settings.searchService='q';


GeoNetwork.MapModule = true;
GeoNetwork.ProjectionList = [['EPSG:4326', 'WGS84 (lat/lon)']];
GeoNetwork.WMSList = [['Geoserver', 'http://localhost/geoserver/wms?']];

GeoNetwork.defaultViewMode = 'view-simple';

Ext.BLANK_IMAGE_URL = '../../apps/js/ext/resources/images/default/s.gif';
