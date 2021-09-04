from django.apps import AppConfig
from django.db.models.signals import post_migrate

from django.db import connection

def move_tables_to_schemas(sender, **kwargs):
    """
    This moves all tables of this model to the app's schema
    """
    app = sender
    with connection.cursor() as cursor:
        cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {app.label};")
        for model in app.get_models():
            query = f'ALTER TABLE IF EXISTS {model._meta.db_table} SET SCHEMA {app.label};'
            cursor.execute(query)


class ComptagesConfig(AppConfig):
    name = 'comptages.datamodel'
    label = 'comptages'

    def ready(self):
        post_migrate.connect(move_tables_to_schemas)
