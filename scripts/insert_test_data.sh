#!/usr/bin/env bash

psql "service=comptages_dev" --single-transaction --echo-errors -f ../db/test_data.sql 
