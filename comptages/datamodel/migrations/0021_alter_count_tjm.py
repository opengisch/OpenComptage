# Generated by Django 3.2.5 on 2021-12-16 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comptages', '0020_delete_tjm'),
    ]

    operations = [
        migrations.AlterField(
            model_name='count',
            name='tjm',
            field=models.IntegerField(null=True),
        ),
    ]
