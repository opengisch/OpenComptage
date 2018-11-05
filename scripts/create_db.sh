#!/usr/bin/env bash

read -p "This will delete the schemas comptages and base_tjm_ok with all the data. Are you sure? " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then

    psql "service=comptages_dev" --single-transaction --echo-errors -f ../db/comptages.sql
    psql "service=comptages_dev" --single-transaction --echo-errors -f ../db/class_category.sql

    psql "service=comptages_dev" --single-transaction --echo-errors -f ../db/base_tjm_ok.sql 
    psql "service=comptages_dev" --single-transaction --echo-errors -f ../db/base_tjm_ok_data.sql
    psql "service=comptages_dev" --single-transaction --echo-errors -f ../db/base_tjm_ok_data_transfer.sql

    psql "service=comptages_dev" --single-transaction --echo-errors -f ../db/test_data.sql 

fi
