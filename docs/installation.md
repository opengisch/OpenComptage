# Installation and maintenance

## Development version

Clone this repository with the submodules

    git clone --recurse-submodules git@github.com:opengisch/OpenComptage.git

Start dev postgres for development, using docker

    docker run -d --rm -p 5432:5432 -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=comptages --name=comptagesdb postgis/postgis:12-2.5

Install python requirements

    pip install -r requirements.txt

Initialize the datamodel from the QGIS's Python Console (use "--fake" flag if the database already exists)

    from django.core.management import call_command
    call_command('migrate', '--fake', 'comptages', '0001_initial')

Upgrade the datamodel

    from django.core.management import call_command
    call_command('migrate', 'comptages')

Import initial data (use "--clear" flag to delete data before import)

    from django.core.management import call_command
    call_command('importdata')

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

1. Look into `requirements.txt` file and install dependencies by opening QGIS > Python Console:

```python
subprocess.check_call(['python', '-m', 'pip', 'install', '<package_1>', '<package_n*>'])
```

2. Deploy to your custom qgis plugin repository:

```powershell
cd .\scripts\windows
.\deploy.ps1
```

3. Install plugin from your custom repository.

4. Make sure the user in the plugin settings is owner of the database otherwise migrations will not work.

5. Run migrations. Open Python console in QGIS:

```python
from django.core.management import call_command
call_command('migrate', 'comptages')
```

6. Revert ownership of database if required

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
