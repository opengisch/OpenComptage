#!/usr/bin/env bash

# Export the sql script file of the pgmodeler's data model
pgmodeler-cli -ef -if ../db/model.dbm -of ../db/generated_model_script.sql
sed -i -- 's/-- DROP SCHEMA IF EXISTS comptages CASCADE;/-- DROP SCHEMA IF EXISTS comptages CASCADE;/g' ../db/generated_model_script.sql
sed -i -- 's/CREATE EXTENSION/CREATE EXTENSION IF NOT EXISTS/g' ../db/generated_model_script.sql
