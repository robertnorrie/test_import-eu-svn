CREATE TABLE spatialIndex
  (
		fid int,
    id  varchar(250),

		primary key(fid)

	);

CREATE INDEX spatialIndexNDX1 ON spatialIndex(id);
SELECT AddGeometryColumn('spatialindex', 'the_geom', 4326, 'MULTIPOLYGON', 2 );
CREATE INDEX spatialIndexNDX2 on spatialIndex USING GIST(the_geom);
