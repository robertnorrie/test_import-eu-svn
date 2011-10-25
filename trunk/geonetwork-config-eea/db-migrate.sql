-- Missing settings from 262 ?

INSERT INTO Settings VALUES (800,1,'indexlanguages',NULL);
INSERT INTO Settings VALUES (801,800,'indexlanguage',NULL);
INSERT INTO Settings VALUES (802,801,'name','danish');
INSERT INTO Settings VALUES (803,801,'selected','false');
INSERT INTO Settings VALUES (804,800,'indexlanguage',NULL);
INSERT INTO Settings VALUES (805,804,'name','dutch');
INSERT INTO Settings VALUES (806,804,'selected','false');
INSERT INTO Settings VALUES (807,800,'indexlanguage',NULL);
INSERT INTO Settings VALUES (808,807,'name','english');
INSERT INTO Settings VALUES (809,807,'selected','true');
INSERT INTO Settings VALUES (810,800,'indexlanguage',NULL);
INSERT INTO Settings VALUES (811,810,'name','finnish');
INSERT INTO Settings VALUES (812,810,'selected','false');
INSERT INTO Settings VALUES (813,800,'indexlanguage',NULL);
INSERT INTO Settings VALUES (814,813,'name','french');
INSERT INTO Settings VALUES (815,813,'selected','false');
INSERT INTO Settings VALUES (816,800,'indexlanguage',NULL);
INSERT INTO Settings VALUES (817,816,'name','german');
INSERT INTO Settings VALUES (818,816,'selected','false');
INSERT INTO Settings VALUES (819,800,'indexlanguage',NULL);
INSERT INTO Settings VALUES (820,819,'name','hungarian');
INSERT INTO Settings VALUES (821,819,'selected','false');
INSERT INTO Settings VALUES (822,800,'indexlanguage',NULL);
INSERT INTO Settings VALUES (823,822,'name','italian');
INSERT INTO Settings VALUES (824,822,'selected','false');
INSERT INTO Settings VALUES (825,800,'indexlanguage',NULL);
INSERT INTO Settings VALUES (826,825,'name','norwegian');
INSERT INTO Settings VALUES (827,825,'selected','false');
INSERT INTO Settings VALUES (828,800,'indexlanguage',NULL);
INSERT INTO Settings VALUES (829,828,'name','portuguese');
INSERT INTO Settings VALUES (830,828,'selected','false');
INSERT INTO Settings VALUES (831,800,'indexlanguage',NULL);
INSERT INTO Settings VALUES (832,831,'name','russian');
INSERT INTO Settings VALUES (833,831,'selected','false');
INSERT INTO Settings VALUES (834,800,'indexlanguage',NULL);
INSERT INTO Settings VALUES (835,834,'name','spanish');
INSERT INTO Settings VALUES (836,834,'selected','false');
INSERT INTO Settings VALUES (837,800,'indexlanguage',NULL);
INSERT INTO Settings VALUES (838,837,'name','swedish');
INSERT INTO Settings VALUES (839,837,'selected','false');



INSERT INTO Settings VALUES (250,1,'searchStats',NULL);
INSERT INTO Settings VALUES (251,250,'enable','false');

INSERT INTO Settings VALUES (722,720,'enableSearchPanel','false');

INSERT INTO Settings VALUES (900,1,'harvester',NULL);
INSERT INTO Settings VALUES (901,900,'enableEditing','false');

-- 2.6.5

INSERT INTO Settings VALUES (23,20,'protocol','http');

INSERT INTO Settings VALUES (88,80,'defaultGroup', NULL);
INSERT INTO Settings VALUES (113,87,'group',NULL);
INSERT INTO Settings VALUES (178,173,'group',NULL);
INSERT INTO Settings VALUES (179,170,'defaultGroup', NULL);

UPDATE Settings SET value='2.6.5' WHERE name='version';
UPDATE Settings SET value='0' WHERE name='subVersion';


-- 2.7.0
CREATE TABLE Validation
  (
    metadataId   int,
    valType      varchar(40),
    status       int,
    tested       int,
    failed       int,
    valDate      varchar(30),
    
    primary key(metadataId, valType),
    foreign key(metadataId) references Metadata(id)
);

CREATE TABLE Thesaurus (
    id   varchar(250) not null,
    activated    varchar(1),
    primary key(id)
  );

CREATE TABLE HarvestHistory
  (
    id             int not null,
    harvestDate    varchar(30),
        harvesterUuid  varchar(250),
        harvesterName  varchar(128),
        harvesterType  varchar(128),
    deleted        char(1) default 'n' not null,
    info           text,
    params         text,

    primary key(id)

  );

CREATE INDEX HarvestHistoryNDX1 ON HarvestHistory(harvestDate);

ALTER TABLE Metadata ALTER COLUMN createDate TYPE varchar(30);
ALTER TABLE Metadata ALTER COLUMN changeDate TYPE varchar(30);
ALTER TABLE Metadata ADD doctype varchar(255);

INSERT INTO Settings VALUES (910,1,'metadata',NULL);
INSERT INTO Settings VALUES (911,910,'enableSimpleView','true');
INSERT INTO Settings VALUES (912,910,'enableIsoView','true');
INSERT INTO Settings VALUES (913,910,'enableInspireView','false');
INSERT INTO Settings VALUES (914,910,'enableXmlView','true');
INSERT INTO Settings VALUES (915,910,'defaultView','simple');

INSERT INTO Settings VALUES (920,1,'threadedindexing',NULL);
INSERT INTO Settings VALUES (921,920,'maxthreads','1');

UPDATE Settings SET value='2.7.0' WHERE name='version';
UPDATE Settings SET value='0' WHERE name='subVersion';


