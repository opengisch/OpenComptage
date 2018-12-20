$dbName = "spch95"
$pgConf = "$($env:USERPROFILE)\.pg_service.conf"
$env:PGSERVICEFILE = $pgConf
$env:PGSERVICE = $dbName

if ([bool](Get-ChildItem -Path $pgConf | Select-String -Pattern $dbName)) {
  Write-Host "Service was found for $dbName"
  # Cleaning before starting
  psql --echo-errors -c 'DROP SCHEMA IF EXISTS comptages CASCADE;'
  psql --echo-errors -c 'DROP SCHEMA IF EXISTS transfer CASCADE;'

  # Import the data model into the database
  psql --echo-errors -f "..\..\db\generated_model_script.sql"

  # Import domain defined data (e.g. classes and categories)
  psql --echo-errors -f "..\..\db\domain_data.sql"
  Write-Host "Before ogr2ogr"
  
  # Import the base_tjm_ok MapInfo dump into the transfer schema
  psql --echo-errors -c 'CREATE SCHEMA IF NOT EXISTS transfer;'
  ogr2ogr -f "PostgreSQL" PG:"schemas=transfer" -t_srs EPSG:2056 -overwrite ../../db/legacy/base_tjm_ok_20180227/BASE_TJM_OK.TAB
  Write-Host "ogr2ogr finished"
  python ../transfer_base_tjm_ok.py $env:PGSERVICE
} else {
  Write-Error "You need to define you pg_service conf."
}
