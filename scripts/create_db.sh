#!/usr/bin/env bash

psql "service=comptages_dev" --single-transaction -f ../db/comptages.sql
