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
    python manage.py migrate

    # Import domain defined data (e.g. classes and categories)
    psql "service=comptages_dev" --single-transaction --echo-errors -f ../db/domain_data.sql

    # Import all sections
    python manage.py importsections

    # Set the log properties
    psql "service=comptages_dev" --echo-errors -f ../db/audit.sql
fi
