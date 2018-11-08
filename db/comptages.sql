-- Database generated with pgModeler (PostgreSQL Database Modeler).
-- pgModeler  version: 0.9.2-alpha
-- PostgreSQL version: 10.0
-- Project Site: pgmodeler.io
-- Model Author: ---


-- Database creation must be done outside a multicommand file.
-- These commands were put in this file only as a convenience.
-- -- object: comptages | type: DATABASE --
-- -- DROP DATABASE IF EXISTS comptages;
-- CREATE DATABASE comptages;
-- -- ddl-end --
-- 

-- object: comptages | type: SCHEMA --
DROP SCHEMA IF EXISTS comptages CASCADE;
CREATE SCHEMA comptages;
-- ddl-end --
ALTER SCHEMA comptages OWNER TO postgres;
-- ddl-end --

SET search_path TO pg_catalog,public,comptages;
-- ddl-end --

-- object: comptages.damage_log | type: TABLE --
-- DROP TABLE IF EXISTS comptages.damage_log CASCADE;
CREATE TABLE comptages.damage_log(
	id serial NOT NULL,
	start_date date NOT NULL,
	end_date date NOT NULL,
	description text NOT NULL,
	id_device integer NOT NULL,
	CONSTRAINT damage_log_pk PRIMARY KEY (id)

);
-- ddl-end --
ALTER TABLE comptages.damage_log OWNER TO postgres;
-- ddl-end --

-- object: comptages.device | type: TABLE --
-- DROP TABLE IF EXISTS comptages.device CASCADE;
CREATE TABLE comptages.device(
	id serial NOT NULL,
	number integer NOT NULL,
	serial text,
	purchase_date date,
	name text,
	id_model integer NOT NULL,
	CONSTRAINT automate_pk PRIMARY KEY (id)

);
-- ddl-end --
ALTER TABLE comptages.device OWNER TO postgres;
-- ddl-end --

-- object: comptages.model | type: TABLE --
-- DROP TABLE IF EXISTS comptages.model CASCADE;
CREATE TABLE comptages.model(
	id serial NOT NULL,
	name text NOT NULL,
	formatter_name text,
	card_name text,
	id_brand integer NOT NULL,
	CONSTRAINT model_pk PRIMARY KEY (id)

);
-- ddl-end --
ALTER TABLE comptages.model OWNER TO postgres;
-- ddl-end --

-- object: comptages.brand | type: TABLE --
-- DROP TABLE IF EXISTS comptages.brand CASCADE;
CREATE TABLE comptages.brand(
	id serial NOT NULL,
	name text NOT NULL,
	CONSTRAINT brand_pk PRIMARY KEY (id)

);
-- ddl-end --
ALTER TABLE comptages.brand OWNER TO postgres;
-- ddl-end --

-- object: comptages.class | type: TABLE --
-- DROP TABLE IF EXISTS comptages.class CASCADE;
CREATE TABLE comptages.class(
	id serial NOT NULL,
	name text NOT NULL,
	description text NOT NULL,
	CONSTRAINT class_pk PRIMARY KEY (id)

);
-- ddl-end --
ALTER TABLE comptages.class OWNER TO postgres;
-- ddl-end --

-- object: comptages.category | type: TABLE --
-- DROP TABLE IF EXISTS comptages.category CASCADE;
CREATE TABLE comptages.category(
	id serial NOT NULL,
	name text NOT NULL,
	code text,
	id_category integer NOT NULL,
	CONSTRAINT category_pk PRIMARY KEY (id)

);
-- ddl-end --
ALTER TABLE comptages.category OWNER TO postgres;
-- ddl-end --

-- object: comptages.sensor_type | type: TABLE --
-- DROP TABLE IF EXISTS comptages.sensor_type CASCADE;
CREATE TABLE comptages.sensor_type(
	id serial NOT NULL,
	name text NOT NULL,
	permanent boolean,
	CONSTRAINT sensor_type_pk PRIMARY KEY (id)

);
-- ddl-end --
ALTER TABLE comptages.sensor_type OWNER TO postgres;
-- ddl-end --

-- object: comptages.count | type: TABLE --
-- DROP TABLE IF EXISTS comptages.count CASCADE;
CREATE TABLE comptages.count(
	id serial NOT NULL,
	start_service_date date,
	end_service_date date,
	start_put_date date,
	end_put_date date,
	start_process_date date,
	end_process_date date,
	valid boolean,
	dysfunction boolean,
	remarks text,
	id_model integer NOT NULL,
	id_device integer,
	id_sensor_type integer,
	id_class integer,
	id_installation integer,
	CONSTRAINT count_pk PRIMARY KEY (id)

);
-- ddl-end --
ALTER TABLE comptages.count OWNER TO postgres;
-- ddl-end --

-- object: postgis | type: EXTENSION --
-- DROP EXTENSION IF EXISTS postgis CASCADE;
-- CREATE EXTENSION postgis
-- ;
-- ddl-end --

-- object: comptages.lane | type: TABLE --
-- DROP TABLE IF EXISTS comptages.lane CASCADE;
CREATE TABLE comptages.lane(
	id serial NOT NULL,
	number smallint NOT NULL,
	direction smallint NOT NULL,
	id_installation integer,
	id_section char(20) NOT NULL,
	CONSTRAINT lane_pk PRIMARY KEY (id)

);
-- ddl-end --
ALTER TABLE comptages.lane OWNER TO postgres;
-- ddl-end --

-- object: comptages.section | type: TABLE --
-- DROP TABLE IF EXISTS comptages.section CASCADE;
CREATE TABLE comptages.section(
	id char(20) NOT NULL,
	name text NOT NULL,
	owner text,
	road text,
	way char(1),
	start_pr integer,
	end_pr integer,
	start_dist integer,
	end_dist integer,
	place_name text,
	geometry geometry(LINESTRING, 2056) NOT NULL,
	CONSTRAINT section_pk PRIMARY KEY (id)

);
-- ddl-end --
ALTER TABLE comptages.section OWNER TO postgres;
-- ddl-end --

-- object: comptages.special_period | type: TABLE --
-- DROP TABLE IF EXISTS comptages.special_period CASCADE;
CREATE TABLE comptages.special_period(
	id serial NOT NULL,
	start_date date NOT NULL,
	end_date date NOT NULL,
	description text NOT NULL,
	entity text,
	influence text,
	CONSTRAINT special_period_pk PRIMARY KEY (id)

);
-- ddl-end --
ALTER TABLE comptages.special_period OWNER TO postgres;
-- ddl-end --

-- object: comptages.count_detail | type: TABLE --
-- DROP TABLE IF EXISTS comptages.count_detail CASCADE;
CREATE TABLE comptages.count_detail(
	id serial NOT NULL,
	numbering integer NOT NULL,
	"timestamp" timestamp NOT NULL,
	distance_front_front numeric(3,1),
	distance_front_back numeric(3,1),
	speed smallint,
	length smallint,
	height char(2),
	fixed boolean,
	wrong_way boolean,
	file_name text,
	id_lane integer NOT NULL,
	id_count integer NOT NULL,
	id_category integer NOT NULL,
	CONSTRAINT count_detail_pk PRIMARY KEY (id)

);
-- ddl-end --
ALTER TABLE comptages.count_detail OWNER TO postgres;
-- ddl-end --

-- object: device_fk | type: CONSTRAINT --
-- ALTER TABLE comptages.damage_log DROP CONSTRAINT IF EXISTS device_fk CASCADE;
ALTER TABLE comptages.damage_log ADD CONSTRAINT device_fk FOREIGN KEY (id_device)
REFERENCES comptages.device (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: model_fk | type: CONSTRAINT --
-- ALTER TABLE comptages.device DROP CONSTRAINT IF EXISTS model_fk CASCADE;
ALTER TABLE comptages.device ADD CONSTRAINT model_fk FOREIGN KEY (id_model)
REFERENCES comptages.model (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: brand_fk | type: CONSTRAINT --
-- ALTER TABLE comptages.model DROP CONSTRAINT IF EXISTS brand_fk CASCADE;
ALTER TABLE comptages.model ADD CONSTRAINT brand_fk FOREIGN KEY (id_brand)
REFERENCES comptages.brand (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: comptages.sensor_type_model | type: TABLE --
-- DROP TABLE IF EXISTS comptages.sensor_type_model CASCADE;
CREATE TABLE comptages.sensor_type_model(
	id_sensor_type integer NOT NULL,
	id_model integer NOT NULL,
	CONSTRAINT sensor_type_model_pk PRIMARY KEY (id_sensor_type,id_model)

);
-- ddl-end --

-- object: sensor_type_fk | type: CONSTRAINT --
-- ALTER TABLE comptages.sensor_type_model DROP CONSTRAINT IF EXISTS sensor_type_fk CASCADE;
ALTER TABLE comptages.sensor_type_model ADD CONSTRAINT sensor_type_fk FOREIGN KEY (id_sensor_type)
REFERENCES comptages.sensor_type (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: model_fk | type: CONSTRAINT --
-- ALTER TABLE comptages.sensor_type_model DROP CONSTRAINT IF EXISTS model_fk CASCADE;
ALTER TABLE comptages.sensor_type_model ADD CONSTRAINT model_fk FOREIGN KEY (id_model)
REFERENCES comptages.model (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: comptages.installation | type: TABLE --
-- DROP TABLE IF EXISTS comptages.installation CASCADE;
CREATE TABLE comptages.installation(
	id serial NOT NULL,
	permanent boolean,
	name text,
	picture text,
	geometry geometry(POINT, 2056),
	active boolean,
	CONSTRAINT installation_pk PRIMARY KEY (id)

);
-- ddl-end --
ALTER TABLE comptages.installation OWNER TO postgres;
-- ddl-end --

-- object: section_fk | type: CONSTRAINT --
-- ALTER TABLE comptages.lane DROP CONSTRAINT IF EXISTS section_fk CASCADE;
ALTER TABLE comptages.lane ADD CONSTRAINT section_fk FOREIGN KEY (id_section)
REFERENCES comptages.section (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: comptages.class_category | type: TABLE --
-- DROP TABLE IF EXISTS comptages.class_category CASCADE;
CREATE TABLE comptages.class_category(
	id_class integer NOT NULL,
	id_category integer NOT NULL,
	CONSTRAINT class_category_pk PRIMARY KEY (id_class,id_category)

);
-- ddl-end --

-- object: class_fk | type: CONSTRAINT --
-- ALTER TABLE comptages.class_category DROP CONSTRAINT IF EXISTS class_fk CASCADE;
ALTER TABLE comptages.class_category ADD CONSTRAINT class_fk FOREIGN KEY (id_class)
REFERENCES comptages.class (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: category_fk | type: CONSTRAINT --
-- ALTER TABLE comptages.class_category DROP CONSTRAINT IF EXISTS category_fk CASCADE;
ALTER TABLE comptages.class_category ADD CONSTRAINT category_fk FOREIGN KEY (id_category)
REFERENCES comptages.category (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: lane_fk | type: CONSTRAINT --
-- ALTER TABLE comptages.count_detail DROP CONSTRAINT IF EXISTS lane_fk CASCADE;
ALTER TABLE comptages.count_detail ADD CONSTRAINT lane_fk FOREIGN KEY (id_lane)
REFERENCES comptages.lane (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: count_fk | type: CONSTRAINT --
-- ALTER TABLE comptages.count_detail DROP CONSTRAINT IF EXISTS count_fk CASCADE;
ALTER TABLE comptages.count_detail ADD CONSTRAINT count_fk FOREIGN KEY (id_count)
REFERENCES comptages.count (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: model_fk | type: CONSTRAINT --
-- ALTER TABLE comptages.count DROP CONSTRAINT IF EXISTS model_fk CASCADE;
ALTER TABLE comptages.count ADD CONSTRAINT model_fk FOREIGN KEY (id_model)
REFERENCES comptages.model (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: device_fk | type: CONSTRAINT --
-- ALTER TABLE comptages.count DROP CONSTRAINT IF EXISTS device_fk CASCADE;
ALTER TABLE comptages.count ADD CONSTRAINT device_fk FOREIGN KEY (id_device)
REFERENCES comptages.device (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: category_fk | type: CONSTRAINT --
-- ALTER TABLE comptages.count_detail DROP CONSTRAINT IF EXISTS category_fk CASCADE;
ALTER TABLE comptages.count_detail ADD CONSTRAINT category_fk FOREIGN KEY (id_category)
REFERENCES comptages.category (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: sensor_type_fk | type: CONSTRAINT --
-- ALTER TABLE comptages.count DROP CONSTRAINT IF EXISTS sensor_type_fk CASCADE;
ALTER TABLE comptages.count ADD CONSTRAINT sensor_type_fk FOREIGN KEY (id_sensor_type)
REFERENCES comptages.sensor_type (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: class_fk | type: CONSTRAINT --
-- ALTER TABLE comptages.count DROP CONSTRAINT IF EXISTS class_fk CASCADE;
ALTER TABLE comptages.count ADD CONSTRAINT class_fk FOREIGN KEY (id_class)
REFERENCES comptages.class (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: comptages.sensor_type_installation | type: TABLE --
-- DROP TABLE IF EXISTS comptages.sensor_type_installation CASCADE;
CREATE TABLE comptages.sensor_type_installation(
	id_sensor_type integer NOT NULL,
	id_installation integer NOT NULL,
	CONSTRAINT sensor_type_installation_pk PRIMARY KEY (id_sensor_type,id_installation)

);
-- ddl-end --

-- object: sensor_type_fk | type: CONSTRAINT --
-- ALTER TABLE comptages.sensor_type_installation DROP CONSTRAINT IF EXISTS sensor_type_fk CASCADE;
ALTER TABLE comptages.sensor_type_installation ADD CONSTRAINT sensor_type_fk FOREIGN KEY (id_sensor_type)
REFERENCES comptages.sensor_type (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: installation_fk | type: CONSTRAINT --
-- ALTER TABLE comptages.sensor_type_installation DROP CONSTRAINT IF EXISTS installation_fk CASCADE;
ALTER TABLE comptages.sensor_type_installation ADD CONSTRAINT installation_fk FOREIGN KEY (id_installation)
REFERENCES comptages.installation (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: installation_fk | type: CONSTRAINT --
-- ALTER TABLE comptages.count DROP CONSTRAINT IF EXISTS installation_fk CASCADE;
ALTER TABLE comptages.count ADD CONSTRAINT installation_fk FOREIGN KEY (id_installation)
REFERENCES comptages.installation (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: comptages.sensor_type_class | type: TABLE --
-- DROP TABLE IF EXISTS comptages.sensor_type_class CASCADE;
CREATE TABLE comptages.sensor_type_class(
	id_sensor_type integer NOT NULL,
	id_class integer NOT NULL,
	CONSTRAINT sensor_type_class_pk PRIMARY KEY (id_sensor_type,id_class)

);
-- ddl-end --

-- object: sensor_type_fk | type: CONSTRAINT --
-- ALTER TABLE comptages.sensor_type_class DROP CONSTRAINT IF EXISTS sensor_type_fk CASCADE;
ALTER TABLE comptages.sensor_type_class ADD CONSTRAINT sensor_type_fk FOREIGN KEY (id_sensor_type)
REFERENCES comptages.sensor_type (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: class_fk | type: CONSTRAINT --
-- ALTER TABLE comptages.sensor_type_class DROP CONSTRAINT IF EXISTS class_fk CASCADE;
ALTER TABLE comptages.sensor_type_class ADD CONSTRAINT class_fk FOREIGN KEY (id_class)
REFERENCES comptages.class (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: comptages.model_class | type: TABLE --
-- DROP TABLE IF EXISTS comptages.model_class CASCADE;
CREATE TABLE comptages.model_class(
	id_model integer NOT NULL,
	id_class integer NOT NULL,
	CONSTRAINT model_class_pk PRIMARY KEY (id_model,id_class)

);
-- ddl-end --

-- object: model_fk | type: CONSTRAINT --
-- ALTER TABLE comptages.model_class DROP CONSTRAINT IF EXISTS model_fk CASCADE;
ALTER TABLE comptages.model_class ADD CONSTRAINT model_fk FOREIGN KEY (id_model)
REFERENCES comptages.model (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: class_fk | type: CONSTRAINT --
-- ALTER TABLE comptages.model_class DROP CONSTRAINT IF EXISTS class_fk CASCADE;
ALTER TABLE comptages.model_class ADD CONSTRAINT class_fk FOREIGN KEY (id_class)
REFERENCES comptages.class (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: category_fk | type: CONSTRAINT --
-- ALTER TABLE comptages.category DROP CONSTRAINT IF EXISTS category_fk CASCADE;
ALTER TABLE comptages.category ADD CONSTRAINT category_fk FOREIGN KEY (id_category)
REFERENCES comptages.category (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: comptages.count_aggregate | type: TABLE --
-- DROP TABLE IF EXISTS comptages.count_aggregate CASCADE;
CREATE TABLE comptages.count_aggregate(
	id serial NOT NULL,
	type text,
	start timestamp,
	"end" timestamp,
	file_name text,
	id_count integer,
	id_lane integer,
	CONSTRAINT count_aggregate_pk PRIMARY KEY (id)

);
-- ddl-end --
ALTER TABLE comptages.count_aggregate OWNER TO postgres;
-- ddl-end --

-- object: count_fk | type: CONSTRAINT --
-- ALTER TABLE comptages.count_aggregate DROP CONSTRAINT IF EXISTS count_fk CASCADE;
ALTER TABLE comptages.count_aggregate ADD CONSTRAINT count_fk FOREIGN KEY (id_count)
REFERENCES comptages.count (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: lane_fk | type: CONSTRAINT --
-- ALTER TABLE comptages.count_aggregate DROP CONSTRAINT IF EXISTS lane_fk CASCADE;
ALTER TABLE comptages.count_aggregate ADD CONSTRAINT lane_fk FOREIGN KEY (id_lane)
REFERENCES comptages.lane (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: comptages.count_aggregate_value | type: TABLE --
-- DROP TABLE IF EXISTS comptages.count_aggregate_value CASCADE;
CREATE TABLE comptages.count_aggregate_value(
	id serial NOT NULL,
	total integer,
	speed_low smallint,
	speed_high smallint,
	length_low smallint,
	length_high smallint,
	id_count_aggregate integer,
	id_category integer,
	CONSTRAINT count_aggregate_value_pk PRIMARY KEY (id)

);
-- ddl-end --
ALTER TABLE comptages.count_aggregate_value OWNER TO postgres;
-- ddl-end --

-- object: count_aggregate_fk | type: CONSTRAINT --
-- ALTER TABLE comptages.count_aggregate_value DROP CONSTRAINT IF EXISTS count_aggregate_fk CASCADE;
ALTER TABLE comptages.count_aggregate_value ADD CONSTRAINT count_aggregate_fk FOREIGN KEY (id_count_aggregate)
REFERENCES comptages.count_aggregate (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: category_fk | type: CONSTRAINT --
-- ALTER TABLE comptages.count_aggregate_value DROP CONSTRAINT IF EXISTS category_fk CASCADE;
ALTER TABLE comptages.count_aggregate_value ADD CONSTRAINT category_fk FOREIGN KEY (id_category)
REFERENCES comptages.category (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: installation_fk | type: CONSTRAINT --
-- ALTER TABLE comptages.lane DROP CONSTRAINT IF EXISTS installation_fk CASCADE;
ALTER TABLE comptages.lane ADD CONSTRAINT installation_fk FOREIGN KEY (id_installation)
REFERENCES comptages.installation (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --


