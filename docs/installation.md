# Installation and maintenance

## Development version

The repository contains a docker-compose configuration to run the
database and a QGIS container with the plugin code mounted as volume.

### Steps
Clone this repository with the submodules

    git clone --recurse-submodules git@github.com:opengisch/OpenComptage.git

Grant access to the X server

    xhost +

Run the containers

    cd OpenComptage
    docker-compose up -d

QGIS should start. Open the plugin manager and enable the plugin `comptages` and configure the host in the QGIS plugin settings to `127.0.0.1`.
Restart QGIS after changing the settings.

Initialize the datamodel from the QGIS's Python Console

    from django.core.management import call_command
    call_command('migrate', 'comptages')


!!! Note
    Run first the command with the "--fake" flag if the database already exists to fake the initial migration
    <code>call_command('migrate', '--fake', 'comptages', '0001_initial')</code>

Restart QGIS and import initial data (use "--clear" flag to delete data before import)

    from django.core.management import call_command
    call_command('importdata')

OpenComptage is now ready to be used! You can find some demo data into
the mounted `/test_data/` directory of the QGIS container. E.g. in the
`SWISS10_vbv` subdirectory there is the complete year 2021 set of
measures for the `00107695` section in the SWISS10 class.

## Windows deployment

Requirements:
 - PostgreSQL,
 - ogr2ogr, psycopg2,
 - QGIS installed with OSGEO4W with pip and a GDAL version matching requirements for django

Clone this repository with the submodules, fetch all tags and checkout to a <TAG_NAME> of your choice

    git clone --recurse-submodules https://github.com/opengisch/OpenComptage.git
    cd OpenComptage
    git fetch --all --tags --prune
    git checkout tags/<TAG_NAME> -b <TAG_NAME>
    
If updating an existing application, go directly to the [Deploying plugin](#deploying-plugin) section.

If starting from zero, restore a backup of opencomptages database or follow [Development version](#development-version)

### Deploying plugin

1. Make sure Django will be aware of GDAL by setting `GDAL_LIBRARY_PATH` environment variable in QGIS settings.
You'll have to find the GDAL dll path in the `bin` folder of your QGIS installation.
For instance `C:/Program Files/QGIS 3.36.3/bin/gdal309.dll`.

2. Look into `requirements.txt` file and install dependencies by opening QGIS > Python Console:

```python
subprocess.check_call(['python', '-m', 'pip', 'install', '<package_1>', '<package_n*>'])
```

3. Deploy to your custom qgis plugin repository:

```powershell
cd .\scripts\windows
.\deploy.ps1
```

4. Install plugin from your custom repository.

5. Make sure the user in the plugin settings is owner of the database otherwise migrations will not work.

6. Run migrations. Open Python console in QGIS:

```python
from django.core.management import call_command
call_command('migrate', 'comptages')
```

7. Revert ownership of database if required

## Recalculate TJM of the counts

Tjm field of `count` model is calculated automatically every time new data of the comptage are accepted from the chart dialog. There is also a command to force the plugin to recalculate the Tjm of the counts.

Open Python console in QGIS:

```python
from django.core.management import call_command
call_command('tjmreset')
```

It is possible to recalculate only a subset of the counts using the options `--min_id` and `--max_id`. For example this command will recalculate only the Tjm of the counts with `5 <= id <= 10`. Both options are inclusive and can be used alone or together.

```python
from django.core.management import call_command
call_command('tjmreset', '--min_id', '5', '--max_id', '10')
```

## Constraint option

When an object referenced by a ForeignKey is deleted, Django will emulate the behavior of the SQL constraint specified by the `on_delete` argument. Django `on_delete` doesn’t create an actual SQL constraint in the database. Support for database-level cascade options may be implemented later (see https://code.djangoproject.com/ticket/21961 ).

That means setting the `on_delete` constraint on the actual database should be done manually.

To get the name of the constraint:

```SQL
select constraint_name from information_schema.key_column_usage where position_in_unique_constraint is not null and table_name = 'count_detail' and column_name = 'id_count'
```

To replace the constraint and set `on_delete` option (replace `<CONSTRAINT_NAME>` with the actual name received from the previous query):

```SQL
alter table comptages.count_detail
drop constraint <CONSTRAINT_NAME>,
add constraint <CONSTRAINT_NAME>
   foreign key ("id_count")
   references "count"(id)
   on delete cascade;
```
