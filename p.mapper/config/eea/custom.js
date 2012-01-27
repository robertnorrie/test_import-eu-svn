
// 
// Some sample functions for customization
//

$.extend(PM.Custom,
{
    // Sample Hyperlink function for result window
    openHyperlink: function(layer, fldName, fldValue) {
        switch(layer) {
            case 'cities10000eu':
                //if (fldName == 'CITY_NAME') {
                    window.open('http:/' + '/en.wikipedia.org/wiki/' + fldValue, 'wikiquery');
                //}
                break;
                
            default:
                alert ('See function openHyperlink in custom.js: ' + layer + ' - ' + fldName + ' - ' + fldValue);
        }
    },

    showCategoryInfo: function(catId) {
        var catName = catId.replace(/licat_/, '');
        alert('Info about category: ' + catName);
    },

    showGroupInfo: function(groupId) {
        var groupName = groupId.replace(/ligrp_/, '');
        alert('Info about layer/group: ' + groupName);
    }

});
$(document).ready(function () {
    var showcoords = $("<div>").id("showcoords").addClass("showcoords");
    showcoords.append($("<div>").id("laeaContainer"))
              .append($("<div>").id("latlonContainer"));
    $("#uiLayoutSouth").prepend(showcoords);
 });


 $.extend(PM.ZoomBox,
 {
    laeaContainer: null,
    latlonContainer: null,

    displayCoordinates: function() {
        if (! this.laeaContainer) {
            this.laeaContainer = $("#laeaContainer");
            this.latlonContainer = $("#latlonContainer");
        }
        var mpoint = this.getGeoCoords(this.moveX, this.moveY);

        // reproject coords
        mpoint_latlon = this.transformCoordinates("EPSG:3035", "EPSG:4326", mpoint);


        // Round values (function 'roundN()' in 'measure.js')
        var px_laea_x = isNaN(mpoint.x) ? '' : mpoint.x.roundTo(0);
        var px_laea_y = isNaN(mpoint.y) ? '' : mpoint.y.roundTo(0);

        var px_latlon_x = isNaN(mpoint.x) ? '' : mpoint_latlon.x.roundTo(4);
        var px_latlon_y = isNaN(mpoint.y) ? '' : mpoint_latlon.y.roundTo(4);


        // Display in DIV
        this.laeaContainer.html('ETRS-LAEA  X: ' + px_laea_x + '  Y: ' + px_laea_x );
        this.latlonContainer.html('LonLat WGS84  lon: ' + px_latlon_x + '&deg;  lat: ' + px_latlon_y + '&deg;' );

    }
 });
