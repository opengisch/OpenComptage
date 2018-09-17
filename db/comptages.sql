-- Database generated with pgModeler (PostgreSQL Database Modeler).
-- pgModeler  version: 0.9.1-beta1
-- PostgreSQL version: 10.0
-- Project Site: pgmodeler.io
-- Model Author: ---


-- Database creation must be done outside an multicommand file.
-- These commands were put in this file only for convenience.
-- -- object: comptages | type: DATABASE --
-- -- DROP DATABASE IF EXISTS comptages;
-- CREATE DATABASE comptages;
-- -- ddl-end --
-- 

-- object: comptages | type: SCHEMA --
-- DROP SCHEMA IF EXISTS comptages CASCADE;
CREATE SCHEMA comptages;
-- ddl-end --
ALTER SCHEMA comptages OWNER TO postgres;
-- ddl-end --

SET search_path TO pg_catalog,public,comptages;
-- ddl-end --

-- object: comptages.journal_panne | type: TABLE --
-- DROP TABLE IF EXISTS comptages.journal_panne CASCADE;
CREATE TABLE comptages.journal_panne(
	id serial NOT NULL,
	date_debut date NOT NULL,
	date_fin date NOT NULL,
	description text NOT NULL,
	id_automate integer NOT NULL,
	CONSTRAINT journal_panne_pk PRIMARY KEY (id)

);
-- ddl-end --
ALTER TABLE comptages.journal_panne OWNER TO postgres;
-- ddl-end --

-- object: comptages.automate | type: TABLE --
-- DROP TABLE IF EXISTS comptages.automate CASCADE;
CREATE TABLE comptages.automate(
	id serial NOT NULL,
	numero_automate integer NOT NULL,
	serial text,
	date_achat date,
	nom_automate text,
	id_model integer NOT NULL,
	CONSTRAINT automate_pk PRIMARY KEY (id)

);
-- ddl-end --
ALTER TABLE comptages.automate OWNER TO postgres;
-- ddl-end --

-- object: comptages.model | type: TABLE --
-- DROP TABLE IF EXISTS comptages.model CASCADE;
CREATE TABLE comptages.model(
	id serial NOT NULL,
	nom_model text NOT NULL,
	nom_formatter text,
	nom_carte text,
	id_marque integer NOT NULL,
	CONSTRAINT model_pk PRIMARY KEY (id)

);
-- ddl-end --
ALTER TABLE comptages.model OWNER TO postgres;
-- ddl-end --

-- object: comptages.marque | type: TABLE --
-- DROP TABLE IF EXISTS comptages.marque CASCADE;
CREATE TABLE comptages.marque(
	id serial NOT NULL,
	nom_marque text NOT NULL,
	CONSTRAINT marque_pk PRIMARY KEY (id)

);
-- ddl-end --
ALTER TABLE comptages.marque OWNER TO postgres;
-- ddl-end --

-- object: comptages.classification | type: TABLE --
-- DROP TABLE IF EXISTS comptages.classification CASCADE;
CREATE TABLE comptages.classification(
	id serial NOT NULL,
	classe text NOT NULL,
	description text NOT NULL,
	CONSTRAINT classification_pk PRIMARY KEY (id)

);
-- ddl-end --
ALTER TABLE comptages.classification OWNER TO postgres;
-- ddl-end --

-- object: comptages.categorie | type: TABLE --
-- DROP TABLE IF EXISTS comptages.categorie CASCADE;
CREATE TABLE comptages.categorie(
	id serial NOT NULL,
	nom_classe text NOT NULL,
	numero_classe text,
	CONSTRAINT categorie_pk PRIMARY KEY (id)

);
-- ddl-end --
ALTER TABLE comptages.categorie OWNER TO postgres;
-- ddl-end --

-- object: comptages.type_capteur | type: TABLE --
-- DROP TABLE IF EXISTS comptages.type_capteur CASCADE;
CREATE TABLE comptages.type_capteur(
	id serial NOT NULL,
	nom_capteur text NOT NULL,
	fixe boolean,
	CONSTRAINT type_capteur_pk PRIMARY KEY (id)

);
-- ddl-end --
ALTER TABLE comptages.type_capteur OWNER TO postgres;
-- ddl-end --

-- object: comptages.comptage | type: TABLE --
-- DROP TABLE IF EXISTS comptages.comptage CASCADE;
CREATE TABLE comptages.comptage(
	id serial NOT NULL,
	date_service_debut date,
	date_service_fin date,
	date_pose date,
	date_depose date,
	date_traitement_debut date,
	date_traitement_fin date,
	valide boolean,
	dysfonctionnement boolean,
	remarques text,
	id_model integer NOT NULL,
	id_automate integer,
	id_type_capteur integer,
	id_classification integer,
	id_installation integer,
	CONSTRAINT comptage_pk PRIMARY KEY (id)

);
-- ddl-end --
ALTER TABLE comptages.comptage OWNER TO postgres;
-- ddl-end --

-- object: comptages.installation | type: TABLE --
-- DROP TABLE IF EXISTS comptages.installation CASCADE;
CREATE TABLE comptages.installation(
	id serial NOT NULL,
	permanent boolean,
	nom text,
	foto text,
	geometrie geometry(POINT, 21781),
	actif boolean,
	CONSTRAINT installation_pk PRIMARY KEY (id)

);
-- ddl-end --
ALTER TABLE comptages.installation OWNER TO postgres;
-- ddl-end --

-- object: comptages.voie | type: TABLE --
-- DROP TABLE IF EXISTS comptages.voie CASCADE;
CREATE TABLE comptages.voie(
	id serial NOT NULL,
	numero smallint NOT NULL,
	direction smallint NOT NULL,
	id_installation integer,
	id_troncon integer NOT NULL,
	CONSTRAINT voie_pk PRIMARY KEY (id)

);
-- ddl-end --
ALTER TABLE comptages.voie OWNER TO postgres;
-- ddl-end --

-- object: comptages.troncon | type: TABLE --
-- DROP TABLE IF EXISTS comptages.troncon CASCADE;
CREATE TABLE comptages.troncon(
	id integer NOT NULL,
	nom text NOT NULL,
	proprietaire text,
	axe text,
	sens smallint,
	pr_debut date,
	pr_fin date,
	dist_debut date,
	dist_fin date,
	nom_lieu text,
	geometrie geometry(LINESTRING, 21781) NOT NULL,
	CONSTRAINT troncon_pk PRIMARY KEY (id)

);
-- ddl-end --
ALTER TABLE comptages.troncon OWNER TO postgres;
-- ddl-end --

-- object: comptages.periode_special | type: TABLE --
-- DROP TABLE IF EXISTS comptages.periode_special CASCADE;
CREATE TABLE comptages.periode_special(
	id serial NOT NULL,
	date_debut date NOT NULL,
	date_fin date NOT NULL,
	description text NOT NULL,
	entite text,
	influence text,
	CONSTRAINT periode_special_pk PRIMARY KEY (id)

);
-- ddl-end --
ALTER TABLE comptages.periode_special OWNER TO postgres;
-- ddl-end --

-- object: comptages.comptage_detail | type: TABLE --
-- DROP TABLE IF EXISTS comptages.comptage_detail CASCADE;
CREATE TABLE comptages.comptage_detail(
	id serial NOT NULL,
	numerotation integer NOT NULL,
	"timestamp" timestamp NOT NULL,
	distance_front_front numeric(3,1),
	distance_front_arriere numeric(3,1),
	vitesse smallint,
	longueur smallint,
	class text,
	hauteur smallint,
	corrige boolean,
	contresens boolean,
	filename text,
	id_voie integer NOT NULL,
	id_comptage integer NOT NULL,
	id_categorie integer NOT NULL,
	CONSTRAINT comptage_detail_pk PRIMARY KEY (id)

);
-- ddl-end --
ALTER TABLE comptages.comptage_detail OWNER TO postgres;
-- ddl-end --

-- object: automate_fk | type: CONSTRAINT --
-- ALTER TABLE comptages.journal_panne DROP CONSTRAINT IF EXISTS automate_fk CASCADE;
ALTER TABLE comptages.journal_panne ADD CONSTRAINT automate_fk FOREIGN KEY (id_automate)
REFERENCES comptages.automate (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: model_fk | type: CONSTRAINT --
-- ALTER TABLE comptages.automate DROP CONSTRAINT IF EXISTS model_fk CASCADE;
ALTER TABLE comptages.automate ADD CONSTRAINT model_fk FOREIGN KEY (id_model)
REFERENCES comptages.model (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: marque_fk | type: CONSTRAINT --
-- ALTER TABLE comptages.model DROP CONSTRAINT IF EXISTS marque_fk CASCADE;
ALTER TABLE comptages.model ADD CONSTRAINT marque_fk FOREIGN KEY (id_marque)
REFERENCES comptages.marque (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: comptages.many_type_capteur_has_many_model | type: TABLE --
-- DROP TABLE IF EXISTS comptages.many_type_capteur_has_many_model CASCADE;
CREATE TABLE comptages.many_type_capteur_has_many_model(
	id_type_capteur integer NOT NULL,
	id_model integer NOT NULL,
	CONSTRAINT many_type_capteur_has_many_model_pk PRIMARY KEY (id_type_capteur,id_model)

);
-- ddl-end --

-- object: type_capteur_fk | type: CONSTRAINT --
-- ALTER TABLE comptages.many_type_capteur_has_many_model DROP CONSTRAINT IF EXISTS type_capteur_fk CASCADE;
ALTER TABLE comptages.many_type_capteur_has_many_model ADD CONSTRAINT type_capteur_fk FOREIGN KEY (id_type_capteur)
REFERENCES comptages.type_capteur (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: model_fk | type: CONSTRAINT --
-- ALTER TABLE comptages.many_type_capteur_has_many_model DROP CONSTRAINT IF EXISTS model_fk CASCADE;
ALTER TABLE comptages.many_type_capteur_has_many_model ADD CONSTRAINT model_fk FOREIGN KEY (id_model)
REFERENCES comptages.model (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: installation_fk | type: CONSTRAINT --
-- ALTER TABLE comptages.voie DROP CONSTRAINT IF EXISTS installation_fk CASCADE;
ALTER TABLE comptages.voie ADD CONSTRAINT installation_fk FOREIGN KEY (id_installation)
REFERENCES comptages.installation (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: troncon_fk | type: CONSTRAINT --
-- ALTER TABLE comptages.voie DROP CONSTRAINT IF EXISTS troncon_fk CASCADE;
ALTER TABLE comptages.voie ADD CONSTRAINT troncon_fk FOREIGN KEY (id_troncon)
REFERENCES comptages.troncon (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: comptages.many_classification_has_many_categorie | type: TABLE --
-- DROP TABLE IF EXISTS comptages.many_classification_has_many_categorie CASCADE;
CREATE TABLE comptages.many_classification_has_many_categorie(
	id_classification integer NOT NULL,
	id_categorie integer NOT NULL,
	CONSTRAINT many_classification_has_many_categorie_pk PRIMARY KEY (id_classification,id_categorie)

);
-- ddl-end --

-- object: classification_fk | type: CONSTRAINT --
-- ALTER TABLE comptages.many_classification_has_many_categorie DROP CONSTRAINT IF EXISTS classification_fk CASCADE;
ALTER TABLE comptages.many_classification_has_many_categorie ADD CONSTRAINT classification_fk FOREIGN KEY (id_classification)
REFERENCES comptages.classification (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: categorie_fk | type: CONSTRAINT --
-- ALTER TABLE comptages.many_classification_has_many_categorie DROP CONSTRAINT IF EXISTS categorie_fk CASCADE;
ALTER TABLE comptages.many_classification_has_many_categorie ADD CONSTRAINT categorie_fk FOREIGN KEY (id_categorie)
REFERENCES comptages.categorie (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: voie_fk | type: CONSTRAINT --
-- ALTER TABLE comptages.comptage_detail DROP CONSTRAINT IF EXISTS voie_fk CASCADE;
ALTER TABLE comptages.comptage_detail ADD CONSTRAINT voie_fk FOREIGN KEY (id_voie)
REFERENCES comptages.voie (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: comptage_fk | type: CONSTRAINT --
-- ALTER TABLE comptages.comptage_detail DROP CONSTRAINT IF EXISTS comptage_fk CASCADE;
ALTER TABLE comptages.comptage_detail ADD CONSTRAINT comptage_fk FOREIGN KEY (id_comptage)
REFERENCES comptages.comptage (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: model_fk | type: CONSTRAINT --
-- ALTER TABLE comptages.comptage DROP CONSTRAINT IF EXISTS model_fk CASCADE;
ALTER TABLE comptages.comptage ADD CONSTRAINT model_fk FOREIGN KEY (id_model)
REFERENCES comptages.model (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: automate_fk | type: CONSTRAINT --
-- ALTER TABLE comptages.comptage DROP CONSTRAINT IF EXISTS automate_fk CASCADE;
ALTER TABLE comptages.comptage ADD CONSTRAINT automate_fk FOREIGN KEY (id_automate)
REFERENCES comptages.automate (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: categorie_fk | type: CONSTRAINT --
-- ALTER TABLE comptages.comptage_detail DROP CONSTRAINT IF EXISTS categorie_fk CASCADE;
ALTER TABLE comptages.comptage_detail ADD CONSTRAINT categorie_fk FOREIGN KEY (id_categorie)
REFERENCES comptages.categorie (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: type_capteur_fk | type: CONSTRAINT --
-- ALTER TABLE comptages.comptage DROP CONSTRAINT IF EXISTS type_capteur_fk CASCADE;
ALTER TABLE comptages.comptage ADD CONSTRAINT type_capteur_fk FOREIGN KEY (id_type_capteur)
REFERENCES comptages.type_capteur (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: classification_fk | type: CONSTRAINT --
-- ALTER TABLE comptages.comptage DROP CONSTRAINT IF EXISTS classification_fk CASCADE;
ALTER TABLE comptages.comptage ADD CONSTRAINT classification_fk FOREIGN KEY (id_classification)
REFERENCES comptages.classification (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: comptages.many_type_capteur_has_many_installation | type: TABLE --
-- DROP TABLE IF EXISTS comptages.many_type_capteur_has_many_installation CASCADE;
CREATE TABLE comptages.many_type_capteur_has_many_installation(
	id_type_capteur integer NOT NULL,
	id_installation integer NOT NULL,
	CONSTRAINT many_type_capteur_has_many_installation_pk PRIMARY KEY (id_type_capteur,id_installation)

);
-- ddl-end --

-- object: type_capteur_fk | type: CONSTRAINT --
-- ALTER TABLE comptages.many_type_capteur_has_many_installation DROP CONSTRAINT IF EXISTS type_capteur_fk CASCADE;
ALTER TABLE comptages.many_type_capteur_has_many_installation ADD CONSTRAINT type_capteur_fk FOREIGN KEY (id_type_capteur)
REFERENCES comptages.type_capteur (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: installation_fk | type: CONSTRAINT --
-- ALTER TABLE comptages.many_type_capteur_has_many_installation DROP CONSTRAINT IF EXISTS installation_fk CASCADE;
ALTER TABLE comptages.many_type_capteur_has_many_installation ADD CONSTRAINT installation_fk FOREIGN KEY (id_installation)
REFERENCES comptages.installation (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: installation_fk | type: CONSTRAINT --
-- ALTER TABLE comptages.comptage DROP CONSTRAINT IF EXISTS installation_fk CASCADE;
ALTER TABLE comptages.comptage ADD CONSTRAINT installation_fk FOREIGN KEY (id_installation)
REFERENCES comptages.installation (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: comptages.many_type_capteur_has_many_classification | type: TABLE --
-- DROP TABLE IF EXISTS comptages.many_type_capteur_has_many_classification CASCADE;
CREATE TABLE comptages.many_type_capteur_has_many_classification(
	id_type_capteur integer NOT NULL,
	id_classification integer NOT NULL,
	CONSTRAINT many_type_capteur_has_many_classification_pk PRIMARY KEY (id_type_capteur,id_classification)

);
-- ddl-end --

-- object: type_capteur_fk | type: CONSTRAINT --
-- ALTER TABLE comptages.many_type_capteur_has_many_classification DROP CONSTRAINT IF EXISTS type_capteur_fk CASCADE;
ALTER TABLE comptages.many_type_capteur_has_many_classification ADD CONSTRAINT type_capteur_fk FOREIGN KEY (id_type_capteur)
REFERENCES comptages.type_capteur (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: classification_fk | type: CONSTRAINT --
-- ALTER TABLE comptages.many_type_capteur_has_many_classification DROP CONSTRAINT IF EXISTS classification_fk CASCADE;
ALTER TABLE comptages.many_type_capteur_has_many_classification ADD CONSTRAINT classification_fk FOREIGN KEY (id_classification)
REFERENCES comptages.classification (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: comptages.many_model_has_many_classification | type: TABLE --
-- DROP TABLE IF EXISTS comptages.many_model_has_many_classification CASCADE;
CREATE TABLE comptages.many_model_has_many_classification(
	id_model integer NOT NULL,
	id_classification integer NOT NULL,
	CONSTRAINT many_model_has_many_classification_pk PRIMARY KEY (id_model,id_classification)

);
-- ddl-end --

-- object: model_fk | type: CONSTRAINT --
-- ALTER TABLE comptages.many_model_has_many_classification DROP CONSTRAINT IF EXISTS model_fk CASCADE;
ALTER TABLE comptages.many_model_has_many_classification ADD CONSTRAINT model_fk FOREIGN KEY (id_model)
REFERENCES comptages.model (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: classification_fk | type: CONSTRAINT --
-- ALTER TABLE comptages.many_model_has_many_classification DROP CONSTRAINT IF EXISTS classification_fk CASCADE;
ALTER TABLE comptages.many_model_has_many_classification ADD CONSTRAINT classification_fk FOREIGN KEY (id_classification)
REFERENCES comptages.classification (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --


