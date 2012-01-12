GeoNetwork.Settings = {};
EEA = {};
EEA.MAPVIEWER_URL = 'https://sdi.eea.europa.eu/eea/databrowser/?uuid=';
EEA.WEBDAV_URL = 'https://sdi.eea.europa.eu/data';
EEA.CIFS_URL = '\\sdi.eea.europa.eu\data';
EEA.FTPS_URL = 'ftps://sdi.eea.europa.eu/data';

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

//Latest update info query
GeoNetwork.Settings.latestQuery = "from=1&to=6&sortBy=changeDate&fast=index";
//GeoNetwork.Settings.latestTpl = EEA.Templates.THUMBNAIL;

GeoNetwork.MapModule = true;
GeoNetwork.ProjectionList = [['EPSG:4326', 'WGS84 (lat/lon)']];
GeoNetwork.WMSList = [['Geoserver', 'http://localhost/geoserver/wms?']];

GeoNetwork.defaultViewMode = 'view-simple';

Ext.BLANK_IMAGE_URL = '../../apps/js/ext/resources/images/default/s.gif';
