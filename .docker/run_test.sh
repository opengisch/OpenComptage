#!/usr/bin/env bash
Xvfb :1 -screen 0 1024x768x16 &
DISPLAY=:1.0
export DISPLAY

echo "Launching QGIS with startup script"
qgis --version-migration --nologo --code /tests/functional.py --profiles-path /tests/ &

echo "Taking screenshot in 10s to let QGIS do his stuff"
sleep 10
import -display :1 -window root /tests/screenshot.png
