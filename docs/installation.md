# Installation

## Development version

Clone this repository with the submodules

    git clone --recurse-submodules git@github.com:opengisch/OpenComptage.git

Start dev postgres for development, using docker

    docker run -d --rm -p 5432:5432 -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=comptages --name=comptagesdb postgis/postgis:12-2.5

Install python requirements

    pip install -r requirements.txt

Initialize the datamodel (use "--fake" flag if the database already exists)

    python manage.py migrate --fake comptages 0001_initial

Upgrade the datamodel

    python manage.py migrate

Import initial data

    python manage.py importsections


## Windows deployment

Requirements: PostgreSQL, ogr2ogr, psycopg2, GDAL_DATA on path (the one provided with mapserver is fine).
Clone this repository with the submodules, fetch all tags and checkout to a <TAG_NAME> of your choice

    git clone --recurse-submodules https://github.com/opengisch/OpenComptage.git
    cd OpenComptage
    git fetch --all --tags --prune
    git checkout tags/<TAG_NAME> -b <TAG_NAME>

If starting from zero, create a database and a user with CREATE rights on it. Create a pg_service.conf file in your %USERPROFILE% directory.
Go into the `scripts\windows` directory of the repository

    cd .\scripts\windows

Adapt `create_db.ps1` with the name of your pg_service.
Create the database structure (need to be done when model is modified, data will be reset):

    .\create_db.ps1

**If updating an existing project**, make sure to check the diff on the SQL files located in the `db` folder between the version you're deploying and the previous deployed version.

Deploy to your custom repository

    .\deploy.ps1

On the client machine, make sure you have a QGIS installed with its own pip (use OSGEO4W installer).
Then, use the QGIS pip to install the additional python packages (replace OSGEO4W install directory if necessary):

    $env:PATH = "C:\OSGeo4W64\apps\Python37;C:\OSGeo4W64\apps\Python37\Scripts"
    python -m pip install setuptools icalendar openpyxl

