# Generated by Django 3.2.5 on 2022-02-04 12:54

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("comptages", "0025_auto_20220204_1353"),
    ]

    operations = [
        migrations.AlterField(
            model_name="modelclass",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4, editable=False, primary_key=True, serialize=False
            ),
        ),
    ]
