<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0">

  <!-- XSLT Parameters
  path: file path to load document with extra information provided by Word document
  -->
  <xsl:variable name="path" select="'/tmp/urbanatlas'"/>
  
  <!-- Load extra info -->
  <xsl:variable name="images" select="document(concat($path, '/doc/urban_atlas_images.xml'))"/>
  <xsl:variable name="pi" select="document(concat($path, '/doc/urban_atlas_pi.xml'))"/>
  <xsl:variable name="ancData" select="document(concat($path, '/doc/urban_atlas_ancillary_data.xml'))"/>
  
  
  <xsl:template match="/">
    <xsl:variable name="cityId" select="normalize-space(/root/city/f_table_name)"/>
    
    <!-- Compute temporal extent base on image data used -->
    <xsl:variable name="startDate">
      <xsl:choose>
        <xsl:when test="$images//FILENAME[@FILENAME=$cityId]">
          <xsl:for-each select="$images//FILENAME[@FILENAME=$cityId]/DATE">
            <xsl:sort data-type="text" order="ascending"/>
            <xsl:if test="position()=1"><xsl:value-of select="replace(., '/', '-')"/></xsl:if>
          </xsl:for-each>
        </xsl:when>
        <xsl:otherwise>2005-01-01</xsl:otherwise>
      </xsl:choose>
    </xsl:variable>

    <xsl:variable name="endDate">
      <xsl:choose>
        <xsl:when test="$images//FILENAME[@FILENAME=$cityId]">
          <xsl:for-each select="$images//FILENAME[@FILENAME=$cityId]/DATE">
            <xsl:sort data-type="text" order="descending"/>
            <xsl:if test="position()=1"><xsl:value-of select="replace(., '/', '-')"/></xsl:if>
          </xsl:for-each>
        </xsl:when>
        <xsl:otherwise>2010-12-31</xsl:otherwise>
      </xsl:choose>
    </xsl:variable>
    
    
    <gmd:MD_Metadata xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xmlns:gmd="http://www.isotc211.org/2005/gmd" xmlns:gco="http://www.isotc211.org/2005/gco"
      xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:gml="http://www.opengis.net/gml"
      xsi:schemaLocation="http://www.isotc211.org/2005/gmd http://www.isotc211.org/2005/gmd/gmd.xsd">
      <gmd:fileIdentifier>
        <gco:CharacterString><xsl:value-of select="/root/city/uuid"/></gco:CharacterString>
      </gmd:fileIdentifier>
      <gmd:language>
        <gmd:LanguageCode codeList="http://www.loc.gov/standards/iso639-2/" codeListValue="eng"/>
      </gmd:language>
      <gmd:characterSet>
        <gmd:MD_CharacterSetCode
          codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#MD_CharacterSetCode"
          codeListValue="utf8"/>
      </gmd:characterSet>
      <gmd:parentIdentifier>
        <gco:CharacterString><xsl:value-of select="/root/city/seriesuuid"/></gco:CharacterString>
      </gmd:parentIdentifier>
      <gmd:hierarchyLevel>
        <gmd:MD_ScopeCode
          codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#MD_ScopeCode"
          codeListValue="dataset"/>
      </gmd:hierarchyLevel>
      <gmd:contact>
        <gmd:CI_ResponsibleParty>
          <gmd:organisationName>
            <gco:CharacterString>European Environment Agency</gco:CharacterString>
          </gmd:organisationName>
          <gmd:contactInfo>
            <gmd:CI_Contact>
              <gmd:address>
                <gmd:CI_Address>
                  <gmd:deliveryPoint>
                    <gco:CharacterString>Kongens Nytorv 6</gco:CharacterString>
                  </gmd:deliveryPoint>
                  <gmd:city>
                    <gco:CharacterString>Copenhagen</gco:CharacterString>
                  </gmd:city>
                  <gmd:administrativeArea>
                    <gco:CharacterString>K</gco:CharacterString>
                  </gmd:administrativeArea>
                  <gmd:postalCode>
                    <gco:CharacterString>1050</gco:CharacterString>
                  </gmd:postalCode>
                  <gmd:country>
                    <gco:CharacterString>Denmark</gco:CharacterString>
                  </gmd:country>
                  <gmd:electronicMailAddress>
                    <gco:CharacterString>eea.enquiries@eea.europa.eu</gco:CharacterString>
                  </gmd:electronicMailAddress>
                </gmd:CI_Address>
              </gmd:address>
            </gmd:CI_Contact>
          </gmd:contactInfo>
          <gmd:role>
            <gmd:CI_RoleCode
              codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#CI_RoleCode"
              codeListValue="pointOfContact"/>
          </gmd:role>
        </gmd:CI_ResponsibleParty>
      </gmd:contact>
      <gmd:dateStamp>
        <gco:DateTime>2012-01-23T13:27:13</gco:DateTime>
      </gmd:dateStamp>
      <gmd:metadataStandardName>
        <gco:CharacterString xmlns:gmx="http://www.isotc211.org/2005/gmx"
          xmlns:srv="http://www.isotc211.org/2005/srv">ISO 19115:2003/19139</gco:CharacterString>
      </gmd:metadataStandardName>
      <gmd:metadataStandardVersion>
        <gco:CharacterString xmlns:gmx="http://www.isotc211.org/2005/gmx"
          xmlns:srv="http://www.isotc211.org/2005/srv">1.0</gco:CharacterString>
      </gmd:metadataStandardVersion>
      <gmd:referenceSystemInfo>
        <gmd:MD_ReferenceSystem>
          <gmd:referenceSystemIdentifier>
            <gmd:RS_Identifier>
              <gmd:code>
                <gco:CharacterString>urn:ogc:def:crs:EPSG:7.1:<xsl:value-of select="/root/city/srid"/></gco:CharacterString>
              </gmd:code>
              <gmd:codeSpace>
                <gco:CharacterString>OGP Surveying &amp; Positioning Committee</gco:CharacterString>
              </gmd:codeSpace>
            </gmd:RS_Identifier>
          </gmd:referenceSystemIdentifier>
        </gmd:MD_ReferenceSystem>
      </gmd:referenceSystemInfo>
      <gmd:identificationInfo>
        <gmd:MD_DataIdentification>
          <gmd:citation>
            <gmd:CI_Citation>
              <gmd:title>
                <gco:CharacterString>Urban Atlas - <xsl:value-of select="/root/city/countryname"/> - <xsl:value-of select="/root/city/cityname"/></gco:CharacterString>
              </gmd:title>
              <gmd:date>
                <gmd:CI_Date>
                  <gmd:date>
                    <gco:Date>2010-05-28</gco:Date>
                  </gmd:date>
                  <gmd:dateType>
                    <gmd:CI_DateTypeCode
                      codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#CI_DateTypeCode"
                      codeListValue="publication"/>
                  </gmd:dateType>
                </gmd:CI_Date>
              </gmd:date>
              <gmd:date>
                <gmd:CI_Date>
                  <gmd:date>
                    <gco:Date>2010-05-28</gco:Date>
                  </gmd:date>
                  <gmd:dateType>
                    <gmd:CI_DateTypeCode
                      codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#CI_DateTypeCode"
                      codeListValue="creation"/>
                  </gmd:dateType>
                </gmd:CI_Date>
              </gmd:date>
              <gmd:identifier>
                <gmd:RS_Identifier>
                  <gmd:code>
                    <gco:CharacterString><xsl:value-of select="/root/city/id"/></gco:CharacterString>
                  </gmd:code>
                </gmd:RS_Identifier>
              </gmd:identifier>
            </gmd:CI_Citation>
          </gmd:citation>
          <gmd:abstract>
            <gco:CharacterString>Urban Atlas&apos; mission is to provide high-resolution hotspot mapping of changes in urban spaces and indicators for users such as city governments, the European Environment Agency (EEA) and European Commission departments.</gco:CharacterString>
          </gmd:abstract>
          <gmd:pointOfContact>
            <gmd:CI_ResponsibleParty>
              <gmd:organisationName>
                <gco:CharacterString>European Environment Agency</gco:CharacterString>
              </gmd:organisationName>
              <gmd:contactInfo>
                <gmd:CI_Contact>
                  <gmd:address>
                    <gmd:CI_Address>
                      <gmd:deliveryPoint>
                        <gco:CharacterString>Kongens Nytorv 6</gco:CharacterString>
                      </gmd:deliveryPoint>
                      <gmd:city>
                        <gco:CharacterString>Copenhagen</gco:CharacterString>
                      </gmd:city>
                      <gmd:administrativeArea>
                        <gco:CharacterString>K</gco:CharacterString>
                      </gmd:administrativeArea>
                      <gmd:postalCode>
                        <gco:CharacterString>1050</gco:CharacterString>
                      </gmd:postalCode>
                      <gmd:country>
                        <gco:CharacterString>Denmark</gco:CharacterString>
                      </gmd:country>
                      <gmd:electronicMailAddress>
                        <gco:CharacterString>eea.enquiries@eea.europa.eu</gco:CharacterString>
                      </gmd:electronicMailAddress>
                    </gmd:CI_Address>
                  </gmd:address>
                  <gmd:onlineResource>
                    <gmd:CI_OnlineResource>
                      <gmd:linkage>
                        <gmd:URL>http://www.eea.europa.eu</gmd:URL>
                      </gmd:linkage>
                      <gmd:protocol>
                        <gco:CharacterString>WWW:LINK-1.0-http--link</gco:CharacterString>
                      </gmd:protocol>
                      <gmd:name>
                        <gco:CharacterString>Europen Environment Agency public
                          website</gco:CharacterString>
                      </gmd:name>
                      <gmd:function>
                        <gmd:CI_OnLineFunctionCode
                          codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#CI_OnLineFunctionCode"
                          codeListValue="information"/>
                      </gmd:function>
                    </gmd:CI_OnlineResource>
                  </gmd:onlineResource>
                </gmd:CI_Contact>
              </gmd:contactInfo>
              <gmd:role>
                <gmd:CI_RoleCode
                  codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#CI_RoleCode"
                  codeListValue="pointOfContact"/>
              </gmd:role>
            </gmd:CI_ResponsibleParty>
          </gmd:pointOfContact>
          <gmd:graphicOverview>
            <gmd:MD_BrowseGraphic>
              <gmd:fileName>
                <gco:CharacterString>http://sdi.eea.europa.eu/public/catalogue-graphic-overview/<xsl:value-of select="/root/city/uuid"/>.png</gco:CharacterString>
              </gmd:fileName>
            </gmd:MD_BrowseGraphic>
          </gmd:graphicOverview>
          <gmd:descriptiveKeywords>
            <gmd:MD_Keywords>
              <gmd:keyword>
                <gco:CharacterString>Land cover</gco:CharacterString>
              </gmd:keyword>
              <gmd:thesaurusName>
                <gmd:CI_Citation>
                  <gmd:title>
                    <gco:CharacterString>GEMET - INSPIRE themes, version 1.0</gco:CharacterString>
                  </gmd:title>
                  <gmd:date>
                    <gmd:CI_Date>
                      <gmd:date>
                        <gco:Date>2008-06-01</gco:Date>
                      </gmd:date>
                      <gmd:dateType>
                        <gmd:CI_DateTypeCode
                          codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#CI_DateTypeCode"
                          codeListValue="publication"/>
                      </gmd:dateType>
                    </gmd:CI_Date>
                  </gmd:date>
                </gmd:CI_Citation>
              </gmd:thesaurusName>
            </gmd:MD_Keywords>
          </gmd:descriptiveKeywords>
          <gmd:descriptiveKeywords>
            <gmd:MD_Keywords>
              <gmd:keyword>
                <gco:CharacterString>EEA owned data sets</gco:CharacterString>
              </gmd:keyword>
              <gmd:keyword>
                <gco:CharacterString>vector data</gco:CharacterString>
              </gmd:keyword>
              <gmd:thesaurusName>
                <gmd:CI_Citation>
                  <gmd:title>
                    <gco:CharacterString>EEA keyword list</gco:CharacterString>
                  </gmd:title>
                  <gmd:date>
                    <gmd:CI_Date>
                      <gmd:date>
                        <gco:Date>2002-03-01</gco:Date>
                      </gmd:date>
                      <gmd:dateType>
                        <gmd:CI_DateTypeCode
                          codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#CI_DateTypeCode"
                          codeListValue="creation"/>
                      </gmd:dateType>
                    </gmd:CI_Date>
                  </gmd:date>
                </gmd:CI_Citation>
              </gmd:thesaurusName>
            </gmd:MD_Keywords>
          </gmd:descriptiveKeywords>
          <gmd:descriptiveKeywords>
            <gmd:MD_Keywords>
              <gmd:keyword>
                <gco:CharacterString>geospatial data</gco:CharacterString>
              </gmd:keyword>
              <gmd:thesaurusName>
                <gmd:CI_Citation>
                  <gmd:title>
                    <gco:CharacterString>EEA categories</gco:CharacterString>
                  </gmd:title>
                  <gmd:date>
                    <gmd:CI_Date>
                      <gmd:date>
                        <gco:Date>2010-07-06</gco:Date>
                      </gmd:date>
                      <gmd:dateType>
                        <gmd:CI_DateTypeCode
                          codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#CI_DateTypeCode"
                          codeListValue="creation"/>
                      </gmd:dateType>
                    </gmd:CI_Date>
                  </gmd:date>
                </gmd:CI_Citation>
              </gmd:thesaurusName>
            </gmd:MD_Keywords>
          </gmd:descriptiveKeywords>
          <gmd:descriptiveKeywords>
            <gmd:MD_Keywords>
              <gmd:keyword>
                <gco:CharacterString><xsl:value-of select="/root/city/countryname"/></gco:CharacterString>
              </gmd:keyword>
              <gmd:type>
                <gmd:MD_KeywordTypeCode
                  codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#MD_KeywordTypeCode"
                  codeListValue="place"/>
              </gmd:type>
            </gmd:MD_Keywords>
          </gmd:descriptiveKeywords>
          <gmd:resourceConstraints>
            <gmd:MD_Constraints>
              <gmd:useLimitation>
                <gco:CharacterString>Unless otherwise indicated, re-use of content on the EEA website for commercial or non-commercial purposes is permitted free of charge, provided that the source is acknowledged. The EEA re-use policy follows Directive 2003/98/EC of the European Parliament and the Council on the re-use of public sector information throughout the European Union and Commission Decision 2006/291/EC, Euratom on the re-use of Commission information. The EEA accepts no responsibility or liability whatsoever for the re-use of content accessible on its website. Any inquiries about re-use of content on the EEA website should be addressed to 
                  Ove Caspersen, EEA, 
                  Kongens Nytorv 6, 
                  DK-1050 Copenhagen K, 
                  Tel +45 33 36 71 00, Fax +45 33 36 71 99, 
                  e-mail copyrights at eea.europa.eu</gco:CharacterString>
              </gmd:useLimitation>
            </gmd:MD_Constraints>
          </gmd:resourceConstraints>
          <gmd:resourceConstraints>
            <gmd:MD_LegalConstraints>
              <gmd:accessConstraints>
                <gmd:MD_RestrictionCode
                  codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#MD_RestrictionCode"
                  codeListValue="otherRestrictions"/>
              </gmd:accessConstraints>
              <gmd:otherConstraints>
                <gco:CharacterString>no limitations</gco:CharacterString>
              </gmd:otherConstraints>
            </gmd:MD_LegalConstraints>
          </gmd:resourceConstraints>
          <gmd:spatialRepresentationType>
            <gmd:MD_SpatialRepresentationTypeCode
              codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#MD_SpatialRepresentationTypeCode"
              codeListValue="vector"/>
          </gmd:spatialRepresentationType>
          <gmd:spatialResolution>
            <gmd:MD_Resolution>
              <gmd:equivalentScale>
                <gmd:MD_RepresentativeFraction>
                  <gmd:denominator>
                    <gco:Integer>10000</gco:Integer>
                  </gmd:denominator>
                </gmd:MD_RepresentativeFraction>
              </gmd:equivalentScale>
            </gmd:MD_Resolution>
          </gmd:spatialResolution>
          <gmd:language>
            <gmd:LanguageCode codeList="http://www.loc.gov/standards/iso639-2/" codeListValue="eng"
            />
          </gmd:language>
          <gmd:topicCategory>
            <gmd:MD_TopicCategoryCode>location</gmd:MD_TopicCategoryCode>
          </gmd:topicCategory>
          <gmd:topicCategory>
            <gmd:MD_TopicCategoryCode>geoscientificInformation</gmd:MD_TopicCategoryCode>
          </gmd:topicCategory>
          <gmd:extent>
            <gmd:EX_Extent>
              <gmd:geographicElement>
                <gmd:EX_GeographicBoundingBox>
                  <gmd:westBoundLongitude>
                    <gco:Decimal><xsl:value-of select="/root/city/west"/></gco:Decimal>
                  </gmd:westBoundLongitude>
                  <gmd:eastBoundLongitude>
                    <gco:Decimal><xsl:value-of select="/root/city/east"/></gco:Decimal>
                  </gmd:eastBoundLongitude>
                  <gmd:southBoundLatitude>
                    <gco:Decimal><xsl:value-of select="/root/city/south"/></gco:Decimal>
                  </gmd:southBoundLatitude>
                  <gmd:northBoundLatitude>
                    <gco:Decimal><xsl:value-of select="/root/city/north"/></gco:Decimal>
                  </gmd:northBoundLatitude>
                </gmd:EX_GeographicBoundingBox>
              </gmd:geographicElement>
            </gmd:EX_Extent>
          </gmd:extent>
          <gmd:extent>
            <gmd:EX_Extent>
              <gmd:temporalElement>
                <gmd:EX_TemporalExtent>
                  <gmd:extent>
                    <gml:TimePeriod gml:id="d28e322a1049886">
                      <gml:beginPosition><xsl:value-of select="$startDate"/></gml:beginPosition>
                      <gml:endPosition><xsl:value-of select="$endDate"/></gml:endPosition>
                    </gml:TimePeriod>
                  </gmd:extent>
                </gmd:EX_TemporalExtent>
              </gmd:temporalElement>
            </gmd:EX_Extent>
          </gmd:extent>
        </gmd:MD_DataIdentification>
      </gmd:identificationInfo>
      <gmd:distributionInfo>
        <gmd:MD_Distribution>
          <gmd:distributionFormat>
            <gmd:MD_Format>
              <gmd:name>
                <gco:CharacterString>SHP</gco:CharacterString>
              </gmd:name>
              <gmd:version gco:nilReason="inapplicable">
                <gco:CharacterString/>
              </gmd:version>
            </gmd:MD_Format>
          </gmd:distributionFormat>
          <gmd:transferOptions>
            <gmd:MD_DigitalTransferOptions>
              <gmd:onLine>
                <gmd:CI_OnlineResource>
                  <gmd:linkage>
                    <gmd:URL>http://www.eea.europa.eu/data-and-maps/data/urban-atlas</gmd:URL>
                  </gmd:linkage>
                  <gmd:protocol>
                    <gco:CharacterString>WWW:LINK-1.0-http--link</gco:CharacterString>
                  </gmd:protocol>
                  <gmd:description>
                    <gco:CharacterString>GMES Urban Atlas web page</gco:CharacterString>
                  </gmd:description>
                  <gmd:function>
                    <gmd:CI_OnLineFunctionCode
                      codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#CI_OnLineFunctionCode"
                      codeListValue="download"/>
                  </gmd:function>
                </gmd:CI_OnlineResource>
              </gmd:onLine>
              <gmd:onLine>
                <gmd:CI_OnlineResource>
                  <gmd:linkage>
                    <gmd:URL>pg:gis_sdi/<xsl:value-of select="/root/city/f_table_schema"/>.<xsl:value-of select="/root/city/f_table_name"/></gmd:URL>
                  </gmd:linkage>
                  <gmd:protocol>
                    <gco:CharacterString>EEA:DBPG</gco:CharacterString>
                  </gmd:protocol>
                </gmd:CI_OnlineResource>
              </gmd:onLine>
                <gmd:onLine>
                  <gmd:CI_OnlineResource>
                    <gmd:linkage>
                      <gmd:URL><xsl:value-of select="/root/city/docPath"/></gmd:URL>
                    </gmd:linkage>
                    <gmd:protocol>
                      <gco:CharacterString>EEA:FOLDERPATH</gco:CharacterString>
                    </gmd:protocol>
                  </gmd:CI_OnlineResource>
                </gmd:onLine>
            </gmd:MD_DigitalTransferOptions>
          </gmd:transferOptions>
        </gmd:MD_Distribution>
      </gmd:distributionInfo>
      <gmd:dataQualityInfo>
        <gmd:DQ_DataQuality>
          <gmd:scope>
            <gmd:DQ_Scope>
              <gmd:level>
                <gmd:MD_ScopeCode codeListValue="dataset"
                  codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#MD_ScopeCode"
                />
              </gmd:level>
            </gmd:DQ_Scope>
          </gmd:scope>
          <gmd:lineage>
            <gmd:LI_Lineage>
              <gmd:statement>
                <gco:CharacterString>
                  
                  <xsl:if test="$images//FILENAME[@FILENAME=$cityId]">
                    Earth Observation (EO) Data used:<xsl:for-each select="$images//FILENAME[@FILENAME=$cityId]">
                      * <xsl:value-of select="concat(SATELLITE, ' - ', IMAGE, ' (Date: ', DATE, ')')"/><xsl:text> </xsl:text><xsl:value-of select="if (normalize-space(COMMENT)!='') then COMMENT else ''"/>
                    </xsl:for-each>
                  </xsl:if>
                  
                  <xsl:if test="$ancData//FILENAME[@FILENAME=$cityId]">
                    Ancillary data used:<xsl:for-each select="$ancData//FILENAME[@FILENAME=$cityId]">
                      * <xsl:value-of select="ID"/><xsl:value-of select="if (TYPE!='' and TITLE!='') then concat(TYPE, ' - ', TITLE) else ''"/>
                      <xsl:value-of select="if (DATE!='') then concat(' (Date: ', DATE, ')') else ''"/>
                      <xsl:value-of select="if (SCALE!='') then concat(' (Scale: ', SCALE, ')') else ''"/>
                        <xsl:text> </xsl:text><xsl:value-of select="if (normalize-space(COMMENT)!='') then COMMENT else ''"/>
                    </xsl:for-each>
                  </xsl:if>
                  </gco:CharacterString>
              </gmd:statement>
            </gmd:LI_Lineage>
          </gmd:lineage>
        </gmd:DQ_DataQuality>
      </gmd:dataQualityInfo>
    </gmd:MD_Metadata>

  </xsl:template>

</xsl:stylesheet>
