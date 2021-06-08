#!/usr/bin/env bash
# TODO : convert to django management command
set -e

read -p "This will delete the comptages database all the data. Are you sure? " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then

    # Cleaning before starting
    psql "service=comptages_dev" --echo-errors -c 'DROP SCHEMA IF EXISTS comptages CASCADE;'
    psql "service=comptages_dev" --echo-errors -c 'DROP SCHEMA IF EXISTS transfer CASCADE;'

    # Import the data model into the database
    psql "service=comptages_dev" --single-transaction --echo-errors -f ../db/generated_model_script.sql

    # Import domain defined data (e.g. classes and categories)
    psql "service=comptages_dev" --single-transaction --echo-errors -f ../db/domain_data.sql
    echo "before ogr2ogr"
    # Import the base_tjm_ok MapInfo dump into the transfer schema
    psql "service=comptages_dev" --echo-errors -c 'CREATE SCHEMA IF NOT EXISTS transfer;'
    ogr2ogr -f "PostgreSQL" PG:"service=comptages_dev schemas=transfer" -t_srs EPSG:2056 -overwrite ../db/legacy/base_tjm_ok_20180227/BASE_TJM_OK.TAB
    echo "ogr2ogr finished"
    python --version
    # Import data from base_tjm to the correct tables
    ./transfer_base_tjm_ok.py

    # Set the log properties
    psql "service=comptages_dev" --echo-errors -f ../db/audit.sql
fi
