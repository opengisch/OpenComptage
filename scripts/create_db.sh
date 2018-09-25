#!/usr/bin/env bash

psql "service=comptages_dev" --single-transaction --echo-errors -f ../db/comptages.sql
psql "service=comptages_dev" --single-transaction --echo-errors -f ../db/base_tjm_ok.sql 
psql "service=comptages_dev" --single-transaction --echo-errors -f ../db/base_tjm_ok_data.sql
psql "service=comptages_dev" --single-transaction --echo-errors -f ../db/base_tjm_ok_data_transfer.sql 
