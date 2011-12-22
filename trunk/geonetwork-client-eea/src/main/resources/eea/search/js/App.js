Ext.namespace('GeoNetwork');

var catalogue;
var app;

GeoNetwork.app = function () {
    // private vars:
    var geonetworkUrl;
    var searching = false;
    var editorWindow;
    var editorPanel;
    var cookie;
    
    /**
     * Application parameters are :
     *
     *  * any search form ids (eg. any)
     *  * mode=1 for visualization
     *  * advanced: to open advanced search form by default
     *  * search: to trigger the search
     *  * uuid: to display a metadata record based on its uuid
     *  * extent: to set custom map extent
     */
    var urlParameters = {};
    /**
     * Catalogue manager
     */
    var catalogue;
    /**
     * An interactive map panel for data visualization
     */
    var iMap, searchForm, resultsPanel, metadataResultsView, tBar, bBar,
        mainTagCloudViewPanel, tagCloudViewPanel, infoPanel,
        visualizationModeInitialized = false;
    
    // private function:
    /**
     * Create a radio button switch in order to change perspective from a search
     * mode to a map visualization mode.
     */
    function createModeSwitcher() {
        var ms = {
            xtype: 'radiogroup',
            id: 'ms',
            hidden: !GeoNetwork.MapModule,
            items: [{
                name: 'mode',
                ctCls: 'mn-main',
                boxLabel: OpenLayers.i18n('discovery'),
                id: 'discoveryMode',
                width: 110,
                inputValue: 0,
                checked: true
            }, {
                name: 'mode',
                ctCls: 'mn-main',
                width: 140,
                boxLabel: OpenLayers.i18n('visualization'),
                id: 'visualizationMode',
                inputValue: 1
            }],
            listeners: {
                change: function (rg, checked) {
                    app.switchMode(checked.getGroupValue(), false);
                    /* TODO : update viewport */
                }
            }
        };
        
        return new Ext.form.FormPanel({
            renderTo: 'mode-form',
            border: false,
            layout: 'hbox',
            items: ms
        });
    }
    
    
    function initMap() {
        iMap = new GeoNetwork.mapApp();
        iMap.init(GeoNetwork.map.BACKGROUND_LAYERS, GeoNetwork.map.MAIN_MAP_OPTIONS);
        metadataResultsView.addMap(iMap.getMap());
        visualizationModeInitialized = true;
    }
    
    
    /**
     * Create a language switcher mode
     *
     * @return
     */
    function createLanguageSwitcher(lang) {
        return new Ext.form.FormPanel({
            renderTo: 'lang-form',
            width: 80,
            border: false,
            layout: 'hbox',
            hidden:  GeoNetwork.Util.locales.length === 1 ? true : false,
            items: [new Ext.form.ComboBox({
                mode: 'local',
                triggerAction: 'all',
                width: 80,
                store: new Ext.data.ArrayStore({
                    idIndex: 0,
                    fields: ['id', 'name'],
                    data: GeoNetwork.Util.locales
                }),
                valueField: 'id',
                displayField: 'name',
                value: lang,
                listeners: {
                    select: function (cb, record, idx){
                        window.location.replace('?hl=' + cb.getValue());
                    }
                }
            })]
        });
    }
    
    
    /**
     * Create a default login form and register extra events in case of error.
     *
     * @return
     */
    function createLoginForm() {
        var loginForm = new GeoNetwork.LoginForm({
            renderTo: 'login-form',
            catalogue: catalogue,
            width: 300,
            layout: 'form'
        });
        
        catalogue.on('afterBadLogin', loginAlert, this);
        // Store user info in cookie to be displayed if user reload the page
        // Register events to set cookie values
        catalogue.on('afterLogin', function(){
            var cookie = Ext.state.Manager.getProvider();
            cookie.set('user', catalogue.identifiedUser);
        });
        catalogue.on('afterLogout', function(){
            var cookie = Ext.state.Manager.getProvider();
            cookie.set('user', undefined);
        });
        
        // Refresh login form if needed
        var cookie = Ext.state.Manager.getProvider();
        var user = cookie.get('user');
        if (user) {
            catalogue.identifiedUser = user;
            loginForm.login(catalogue, true);
        }
    }
    /**
     * Create latest metadata panel.
     */
    function createLatestUpdate(){
        var latestView = new GeoNetwork.MetadataResultsView({
            catalogue: catalogue,
            height: 500,
            autoScroll: true,
            tpl: EEA.Templates.THUMBNAIL
        });
        latestView.setStore(GeoNetwork.Settings.mdStore());
        new Ext.Panel({
            border: false,
            bodyCssClass: 'md-view',
            items: latestView,
            renderTo: 'latest'
        });
        catalogue.kvpSearch(GeoNetwork.Settings.latestQuery, null, null, null, true, latestView.getStore());
    }
    /**
     * Error message in case of bad login
     *
     * @param cat
     * @param user
     * @return
     */
    function loginAlert(cat, user) {
        Ext.Msg.show({
            title: 'Login',
            msg: 'Login failed. Check your username and password.',
            /* TODO : Get more info about the error */
            icon: Ext.MessageBox.ERROR,
            buttons: Ext.MessageBox.OK
        });
    }
    
    /**
     * Create a default search form with advanced mode button
     *
     * @return
     */
    function createSearchForm() {
        
                // Add advanced mode criteria to simple form - start
        var advancedCriteria = [];
        var services = catalogue.services;
        var orgNameStore = new GeoNetwork.data.OpenSearchSuggestionStore({
            url: services.opensearchSuggest,
            rootId: 1,
            baseParams: {
                field: 'orgName'
            }
        });
        var orgNameField = new Ext.ux.form.SuperBoxSelect({
            hideLabel: false,
            minChars: 0,
            queryParam: 'q',
            hideTrigger: false,
            id: 'E_orgName',
            name: 'E_orgName',
            store: orgNameStore,
            valueField: 'value',
            displayField: 'value',
            valueDelimiter: ' or ',
//            tpl: tpl,
            fieldLabel: OpenLayers.i18n('org')
        });
        
        
        
        
        // Multi select keyword
        var themekeyStore = new GeoNetwork.data.OpenSearchSuggestionStore({
            url: services.opensearchSuggest,
            rootId: 1,
            baseParams: {
                field: 'keyword'
            }
        });
//        FIXME : could not underline current search criteria in tpl
//        var tpl = '<tpl for="."><div class="x-combo-list-item">' + 
//            '{[values.value.replace(Ext.getDom(\'E_themekey\').value, \'<span>\' + Ext.getDom(\'E_themekey\').value + \'</span>\')]}' + 
//          '</div></tpl>';
        var themekeyField = new Ext.ux.form.SuperBoxSelect({
            hideLabel: false,
            minChars: 0,
            queryParam: 'q',
            hideTrigger: false,
            id: 'E_themekey',
            name: 'E_themekey',
            store: themekeyStore,
            valueField: 'value',
            displayField: 'value',
            valueDelimiter: ' or ',
//            tpl: tpl,
            fieldLabel: OpenLayers.i18n('keyword')
//            FIXME : Allow new data is not that easy
//            allowAddNewData: true,
//            addNewDataOnBlur: true,
//            listeners: {
//                newitem: function (bs,v, f){
//                    var newObj = {
//                            value: v
//                        };
//                    bs.addItem(newObj, true);
//                }
//            }
        });
        
        var when = new Ext.form.FieldSet({
            title: OpenLayers.i18n('when'),
            autoWidth: true,
            //layout: 'row',
            defaultType: 'datefield',
            collapsible: true,
            collapsed: true,
            items: GeoNetwork.util.SearchFormTools.getWhen()
        });
        
        var idField = new GeoNetwork.form.OpenSearchSuggestionTextField({
            hideLabel: false,
            minChars: 1,
            hideTrigger: true,
            url: catalogue.services.opensearchSuggest,
            field: 'identifier', 
            name: 'E_identifier', 
            fieldLabel: OpenLayers.i18n('rsIdentifier')
        });
        
        var catalogueField = GeoNetwork.util.SearchFormTools.getCatalogueField(services.getSources, services.logoUrl, true);
        var groupField = GeoNetwork.util.SearchFormTools.getGroupField(services.getGroups, true);
        var metadataTypeField = GeoNetwork.util.SearchFormTools.getMetadataTypeField(true);
        //var categoryField = GeoNetwork.util.SearchFormTools.getCategoryField(services.getCategories, '../../apps/images/default/category/');
        var validField = GeoNetwork.util.SearchFormTools.getValidField(true);
        var spatialTypes = GeoNetwork.util.SearchFormTools.getSpatialRepresentationTypeField([['grid', OpenLayers.i18n('grid')], 
                                                                                              ['textTabled', OpenLayers.i18n('textTable')], 
                                                                                              ['vector', OpenLayers.i18n('vector')] 
                                                                                              ], true);
        var denominatorField = GeoNetwork.util.SearchFormTools.getScaleDenominatorField(true);
        var typeCodeList = GeoNetwork.util.SearchFormTools.getTypesField(null, true);
        
        advancedCriteria.push(themekeyField, orgNameField, typeCodeList, //categoryField, 
                                when, spatialTypes, denominatorField, idField,
                                catalogueField, groupField, 
                                metadataTypeField, validField);
        var adv = {
            xtype: 'fieldset',
            title: OpenLayers.i18n('advancedSearchOptions'),
            autoHeight: true,
            autoWidth: true,
            collapsible: true,
            collapsed: (urlParameters.advanced ? false : true),
            defaultType: 'checkbox',
            defaults: {
                width: 160
            },
            items: advancedCriteria
        };
        
        var inspire = {
                xtype: 'fieldset',
                title: OpenLayers.i18n('inspireSearchOptions'),
                autoHeight: true,
                autoWidth: true,
                collapsible: true,
                collapsed: (urlParameters.inspire ? false : true),
                defaultType: 'checkbox',
                defaults: {
                    width: 160
                },
                items: GeoNetwork.util.INSPIRESearchFormTools.getINSPIREFields(catalogue.services, true)
            };
            
        
        var formItems = [];
        formItems.push(GeoNetwork.util.SearchFormTools.getSimpleFormFields(catalogue.services, 
                    GeoNetwork.map.BACKGROUND_LAYERS, GeoNetwork.map.MAP_OPTIONS, false, 
                    GeoNetwork.searchDefault.activeMapControlExtent, undefined, {width: 290}), 
                    inspire, adv);
        // Add advanced mode criteria to simple form - end
        
        
        // Hide or show extra fields after login event
        var adminFields = [groupField, metadataTypeField, validField];
        Ext.each(adminFields, function (item) {
            item.setVisible(false);
        });
        
        catalogue.on('afterLogin', function () {
            Ext.each(adminFields, function (item) {
                item.setVisible(true);
            });
        });
        catalogue.on('afterLogout', function () {
            Ext.each(adminFields, function (item) {
                item.setVisible(false);
            });
        });
        
        
        return new Ext.FormPanel({
            id: 'searchForm',
            renderTo: 'search-form',
            border: false,
            //autoShow : true,
            padding: 5,
            //autoHeight : true,
            defaults: {
                width : 180
            },
            listeners: {
                afterrender: function (){
                }
            },
            items: formItems,
            buttons: [{
                tooltip: OpenLayers.i18n('resetSearchForm'),
                // iconCls: 'md-mn-reset',
                id: 'resetBt',
                icon: '../../apps/images/default/cross.png',
                listeners: {
                    click: function (){
                        Ext.getCmp('searchForm').getForm().reset();
                    }
                }
            }, {
                text: OpenLayers.i18n('search'),
                id: 'searchBt',
                icon: '../../apps/js/GeoNetwork/resources/images/default/find.png',
                // FIXME : iconCls : 'md-mn-find',
                iconAlign: 'right',
                listeners: {
                    click: function (){
                    
                        if (Ext.getCmp('geometryMap')) {
                           metadataResultsView.addMap(Ext.getCmp('geometryMap').map, true);
                        }
                        var any = Ext.get('E_any');
                        if (any) {
                            if (any.getValue() === OpenLayers.i18n('fullTextSearch')) {
                                any.setValue('');
                            }
                        }
                        
                        catalogue.startRecord = 1; // Reset start record
                        search();
                    }
                }
            }]
        });
    }
    function loadCallback(el, success, response, options){
        if (success) {
            createLatestUpdate();
        } else {
            Ext.get('infoPanel').getUpdater().update({url:'home_en.html'});
        }
    }
    /** private: methode[createInfoPanel]
     *  Main information panel displayed on load
     *
     *  :return:
     */
    function createInfoPanel(){
        return new Ext.Panel({
            border: true,
            id: 'infoPanel',
            baseCls: 'md-info',
            autoWidth: true,
            renderTo: 'infoContent',
            //contentEl: 'infoContent',
            autoLoad: {
                url: 'home_' + catalogue.LANG + '.html',
                callback: loadCallback,
                scope: this,
                loadScripts: false
            }
        });
    }
    /** private: methode[createHelpPanel]
     *  Help panel displayed on load
     *
     *  :return:
     */
    function createHelpPanel(){
        return new Ext.Panel({
            border: false,
            frame: false,
            baseCls: 'none',
            id: 'helpPanel',
            autoWidth: true,
            renderTo: 'shortcut',
            autoLoad: {
                url: 'help_' + catalogue.LANG + '.html',
                callback: initShortcut,
                scope: this,
                loadScripts: false
            }
        });
    }
    function search(){
        searching = true;
        catalogue.search('searchForm', app.loadResults, null, catalogue.startRecord, true);
        
        var infoPanel = Ext.getCmp('infoPanel'), 
            resultsPanel = Ext.getCmp('resultsPanel'),
            tagCloudPanel = Ext.getCmp('tagCloudPanel');
          if (infoPanel.isVisible()) {
            infoPanel.hide();
          }
          if (!resultsPanel.isVisible()) {
             resultsPanel.show();
          }
          if (!tagCloudPanel.isVisible()) {
             tagCloudPanel.show();
          }
    }
    
    /**
     * Bottom bar
     *
     * @return
     */
    function createBBar(){
    
        var previousAction = new Ext.Action({
            id: 'previousBt',
            text: '&lt;&lt;',
            handler: function(){
            	var from = catalogue.startRecord - parseInt(Ext.getCmp('E_hitsperpage').getValue(), 10);
                if (from > 0) {
                	catalogue.startRecord = from;
	            	search();
                }
            },
            scope: this
        });
        
        var nextAction = new Ext.Action({
            id: 'nextBt',
            text: '&gt;&gt;',
            handler: function (){
                catalogue.startRecord += parseInt(Ext.getCmp('E_hitsperpage').getValue(), 10);
                search();
            },
            scope: this
        });
        
        return new Ext.Toolbar({
            items: [previousAction, '|', nextAction, '|', {
                xtype: 'tbtext',
                text: '',
                id: 'info'
            }]
        });
        
    }
    
    /**
     * Results panel layout with top, bottom bar and DataView
     *
     * @return
     */
    function createResultsPanel(){
        metadataResultsView = new GeoNetwork.MetadataResultsView({
            catalogue: catalogue,
            autoScroll: true,
            autoHeight: true,
            tpl: EEA.Templates.FULL,
            templates: {
                SIMPLE: EEA.Templates.SIMPLE,
                THUMBNAIL: EEA.Templates.THUMBNAIL,
                FULL: EEA.Templates.FULL
            }
        });
        
        catalogue.resultsView = metadataResultsView;
        
        tBar = new GeoNetwork.MetadataResultsToolbar({
            catalogue: catalogue,
            searchBtCmp: Ext.getCmp('searchBt'),
            sortByCmp: Ext.getCmp('E_sortBy'),
            metadataResultsView: metadataResultsView
        });
        
        bBar = createBBar();
        
        resultPanel = new Ext.Panel({
            id: 'resultsPanel',
            renderTo: 'region-content',
            border: false,
            hidden: true,
            autoHeight: true,
            //height: 750,
            bodyCssClass: 'md-view',
            //autoWidth: true,
            layout: 'fit',
            tbar: tBar,
            items: metadataResultsView,
            // paging bar on the bottom
            bbar: bBar
        });
        return resultPanel;
    }
   
    /**
     * Extra tag cloud to displayed current search summary TODO : not really a
     * narrow your search component.
     *
     * @return
     */
    function createTagCloud(){
        var tagCloudView = new GeoNetwork.TagCloudView({
            catalogue: catalogue,
            tpl: new Ext.XTemplate(
                    '<ul>', 
                    '<tpl for=".">', 
                        '<li class="tag-cloud">',
                            // TODO : hitsPerPage should take in account the current search form
                            '<a href="#" onclick="javascript:catalogue.kvpSearch(\'fast=index&summaryOnly=0&from=1&to=20&hitsPerPage=20&themekey={value}\', ' + 
                        'null, null, null);" alt="{value}" title="{count} records">{value} ({count} records)</a>', 
                        '</li>', 
                    '</tpl>', 
                '</ul>')
        });
        
        return new Ext.Panel({
            id: 'tagCloudPanel',
            renderTo: 'tag-cloud',
            layout: 'fit',
            border: false,
            hidden: true,
            autoHeight: true,
            baseCls: 'md-view',
            items: tagCloudView
        });
    }
    
    function edit(metadataId, create, group, child){
        
        if (!this.editorWindow) {
            this.editorPanel = new GeoNetwork.editor.EditorPanel({
                defaultViewMode: GeoNetwork.Settings.editor.defaultViewMode,
                catalogue: catalogue,
                xlinkOptions: {CONTACT: true}
            });
            
            this.editorWindow = new Ext.Window({
                tools: [{
                    id: 'newwindow',
                    qtip: OpenLayers.i18n('newWindow'),
                    handler: function (e, toolEl, panel, tc){
                        window.open(GeoNetwork.Util.getBaseUrl(location.href) + "#edit=" + metadataId);
                        panel.hide();
                    },
                    scope: this
                }],
                title: OpenLayers.i18n('mdEditor'),
                id : 'editorWindow',
                layout: 'fit',
                modal: false,
                items: this.editorPanel,
                closeAction: 'hide',
                collapsible: true,
                collapsed: false,
                maximizable: true,
                maximized: true,
                resizable: true,
//                constrain: true,
                width: 980,
                height: 800
            });
            this.editorPanel.setContainer(this.editorWindow);
            this.editorPanel.on('editorClosed', function (){
                Ext.getCmp('searchBt').fireEvent('click');
            });
        }
        
        if (metadataId) {
            this.editorWindow.show();
            this.editorWindow.maximize();
            this.editorPanel.init(metadataId, create, group, child);
        }
    }
    
    function createHeader(){
        var info = catalogue.getInfo();
        document.title = info.name;
        
        // http://www.eea.europa.eu/en/getHeader
        // Load EEA header inf
//        new Ext.Panel({
//            border: false,
//            frame: false,
//            baseCls: 'none',
//            autoWidth: true,
//            renderTo: 'header',
//            autoLoad: {
//                //url: 'http://webservices.eea.europa.eu/templates/getHeader?tabselected=products',
//                url: 'http://www.eea.europa.eu/' + catalogue.LANG + '/getHeader',
//                loadScripts: false
//            }
//        });
//        return new Ext.Panel({
//            border: false,
//            frame: false,
//            baseCls: 'none',
//            autoWidth: true,
//            renderTo: 'footer',
//            autoLoad: {
//                url: 'http://www.eea.europa.eu/' + catalogue.LANG + '/getFooter',
//                loadScripts: false
//            }
//        });
    }
    
    // public space:
    return {
        init: function (){
            geonetworkUrl = GeoNetwork.URL || window.location.href.match(/(http.*\/.*)\/eea\/search.*/, '')[1];

            urlParameters = GeoNetwork.Util.getParameters(location.href);
            var lang = GeoNetwork.Util.getCatalogueLang(urlParameters.hl || GeoNetwork.defaultLocale);
            if (urlParameters.extent) {
                urlParameters.bounds = new OpenLayers.Bounds(urlParameters.extent[0], urlParameters.extent[1], urlParameters.extent[2], urlParameters.extent[3]);
            }

            // Init cookie
            cookie = new Ext.state.CookieProvider({
                expires: new Date(new Date().getTime()+(1000*60*60*24*365))
            });
            Ext.state.Manager.setProvider(cookie);
            
            Ext.getDom('searchLb').innerHTML = OpenLayers.i18n('search');
            Ext.getDom('loginLb').innerHTML = OpenLayers.i18n('login');
            
            // Create connexion to the catalogue
            catalogue = new GeoNetwork.Catalogue({
                statusBarId: 'info',
                lang: lang,
                hostUrl: geonetworkUrl,
                mdOverlayedCmpId: 'resultsPanel',
                adminAppUrl: geonetworkUrl + '/srv/' + lang + '/admin',
                // Declare default store to be used for records and summary
                metadataStore: GeoNetwork.Settings.mdStore(),
                metadataCSWStore : GeoNetwork.data.MetadataCSWResultsStore(),
                summaryStore: GeoNetwork.data.MetadataSummaryStore(),
                editMode: 2, // TODO : create constant
                metadataEditFn: edit
            });
            
            createHeader();
            
            // Override xml search service value
            catalogue.setServiceUrl('xmlSearch', GeoNetwork.Settings.searchService);

            // Search form
            searchForm = createSearchForm();
            
            // Top navigation widgets
            createLanguageSwitcher(lang);
            createLoginForm();
            createTagCloud();
            edit();
            
            // Search result
            resultsPanel = createResultsPanel();

            createHelpPanel();
            infoPanel = createInfoPanel();
            
            /* Init form field URL according to URL parameters */
            GeoNetwork.util.SearchTools.populateFormFromParams(searchForm, urlParameters);

            /* Trigger search if search is in URL parameters */
            if (urlParameters.search !== undefined) {
                Ext.getCmp('searchBt').fireEvent('click');
            }
            if (urlParameters.edit !== undefined && urlParameters.edit !== '') {
                catalogue.metadataEdit(urlParameters.edit);
            }
            if (urlParameters.create !== undefined) {
                resultPanel.getTopToolbar().createMetadataAction.fireEvent('click');
            }
            if (urlParameters.uuid !== undefined) {
                catalogue.metadataShow(urlParameters.uuid, false);
            } else if (urlParameters.id !== undefined) {
                catalogue.metadataShowById(urlParameters.id, true);
            }
            
            // FIXME : should be in Search field configuration
            Ext.get('E_any').setWidth(285);
            Ext.get('E_any').setHeight(28);
            if (GeoNetwork.searchDefault.activeMapControlExtent) {
                Ext.getCmp('geometryMap').setExtent();
            }
            if (urlParameters.bounds) {
                Ext.getCmp('geometryMap').map.zoomToExtent(urlParameters.bounds);
            }
            
//            resultPanel.setHeight(Ext.getCmp('center').getHeight());
            
            var events = ['afterDelete', 'afterRating', 'afterLogout', 'afterLogin'];
            Ext.each(events, function (e) {
                catalogue.on(e, function (){
                    if (searching === true) {
                        Ext.getCmp('searchBt').fireEvent('click');
                    }
                });
            });
        },
        getCatalogue: function (){
            return catalogue;
        },
        /**
         * Do layout
         *
         * @param response
         * @return
         */
        loadResults: function (response){
            // FIXME : result panel need to update layout in case of slider
            // Ext.getCmp('resultsPanel').syncSize();
            Ext.getCmp('previousBt').setDisabled(catalogue.startRecord === 1);
            Ext.getCmp('nextBt').setDisabled(catalogue.startRecord + 
                    parseInt(Ext.getCmp('E_hitsperpage').getValue(), 10) > catalogue.metadataStore.totalLength);
            if (Ext.getCmp('E_sortBy').getValue()) {
              Ext.getCmp('sortByToolBar').setValue(Ext.getCmp('E_sortBy').getValue()  + "#" + Ext.getCmp('sortOrder').getValue() );

            } else {
              Ext.getCmp('sortByToolBar').setValue(Ext.getCmp('E_sortBy').getValue());

            }
            
//            resultsPanel.syncSize();
//            console.log(Ext.getCmp('tagCloudPanel'));
//            Ext.getCmp('tagCloudPanel').setHeight(200);
            //resultPanel.setHeight(Ext.getCmp('center').getHeight());
            Ext.ux.Lightbox.register('a[rel^=lightbox]');
        }
    };
};

Ext.onReady(function (){
    var lang = /hl=([a-z]{2})/.exec(location.href);
    GeoNetwork.Util.setLang(lang && lang[1], '..');

    Ext.QuickTips.init();
    setTimeout(function () {
      Ext.get('loading').remove();
      Ext.get('loading-mask').fadeOut({remove:true});
    }, 250);

    app = new GeoNetwork.app();
    app.init();
    catalogue = app.getCatalogue();
    
    /* Focus on full text search field */
    Ext.getDom('E_any').focus(true);
    
});
