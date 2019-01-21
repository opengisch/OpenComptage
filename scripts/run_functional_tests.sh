#!/usr/bin/env bash

set -e

docker run -d --name qgis -v /tmp/.X11-unix:/tmp/.X11-unix \
 -v `pwd`/../.:/tests_directory \
 -e DISPLAY=:99 \
 qgis/qgis:latest

docker exec -it qgis sh -c "apt install -y python3-plotly"

docker exec -it qgis sh -c "qgis_setup.sh comptages"

docker exec -it qgis sh -c "cd /tests_directory && qgis_testrunner.sh comptages.test.functional.run_all"
