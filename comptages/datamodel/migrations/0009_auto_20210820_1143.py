# Generated by Django 3.2.4 on 2021-08-20 11:43

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('comptages', '0008_auto_20210820_1143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensortypeclass',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='sensortypeinstallation',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='sensortypemodel',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]