GRANT USAGE ON SCHEMA comptages TO spch_comptages_rw;
GRANT SELECT ON ALL SEQUENCES IN SCHEMA comptages TO spch_comptages_rw;
GRANT SELECT ON ALL TABLES IN SCHEMA comptages TO spch_comptages_rw;
GRANT ALL ON comptages.brand, comptages.model, comptages.device, comptages.damage_log, comptages.special_period, comptages.installation, comptages.count, comptages.sensor_type TO spch_comptages_rw;
ALTER DEFAULT PRIVILEGES IN SCHEMA comptages GRANT SELECT ON TABLES TO spch_comptages_rw;
ALTER DEFAULT PRIVILEGES IN SCHEMA comptages GRANT SELECT ON SEQUENCES TO spch_comptages_rw;

GRANT USAGE ON SCHEMA comptages TO spch_comptages_ro;
GRANT SELECT ON ALL TABLES IN SCHEMA comptages TO spch_comptages_ro;
GRANT SELECT ON ALL SEQUENCES IN SCHEMA comptages TO spch_comptages_ro;
ALTER DEFAULT PRIVILEGES IN SCHEMA comptages GRANT SELECT ON TABLES TO spch_comptages_ro;
ALTER DEFAULT PRIVILEGES IN SCHEMA comptages GRANT SELECT ON SEQUENCES TO spch_comptages_ro;
