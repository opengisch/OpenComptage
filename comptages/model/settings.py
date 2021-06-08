import os
import tempfile

DATABASES = {
    'default': {
         'ENGINE': 'django.contrib.gis.db.backends.postgis',
         'NAME': 'comptages',
         'USER': 'postgres',
         'PASSWORD': 'postgres',
        'OPTIONS': {
                'options': '-c search_path=comptages,transfer,public'
            },
    },
}

INSTALLED_APPS = [
    "comptages.model.core",
]

GDAL_LIBRARY_PATH = r"C:\OSGeo4W\bin\gdal302.dll"
GEOS_LIBRARY_PATH = r"C:\OSGeo4W\bin\geos_c.dll"
SPATIALITE_LIBRARY_PATH = r"C:\OSGeo4W\bin\mod_spatialite.dll"
