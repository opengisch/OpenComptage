#!/usr/bin/env bash

# Copy plugin folder into shared volume profiles dir
sudo rm -rf .docker/tests/profiles/default/python/plugins/comptages
mkdir -p .docker/tests/profiles/default/python/plugins && cp -r comptages "$_"

# Copy the functional test module into shared volume
cp comptages/test/functional.py .docker/tests/

# Run script into docker to install plugin and run the test
docker-compose -f .docker/docker-compose.yml run qgis_tester /run_test.sh
