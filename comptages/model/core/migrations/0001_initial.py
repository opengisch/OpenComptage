# Generated by Django 3.2.4 on 2021-06-08 14:14

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BaseTjmOk',
            fields=[
                ('ogc_fid', models.AutoField(primary_key=True, serialize=False)),
                ('fsection', models.CharField(blank=True, max_length=20, null=True)),
                ('fonctionel', models.CharField(blank=True, max_length=4, null=True)),
                ('f_prop', models.CharField(blank=True, max_length=12, null=True)),
                ('f_axe', models.CharField(blank=True, max_length=64, null=True)),
                ('f_sens', models.CharField(blank=True, max_length=1, null=True)),
                ('f_pr_d', models.CharField(blank=True, max_length=64, null=True)),
                ('f_dist_d', models.CharField(blank=True, max_length=19, null=True)),
                ('ecartd', models.CharField(blank=True, max_length=10, null=True)),
                ('f_pr_f', models.CharField(blank=True, max_length=64, null=True)),
                ('f_dist_f', models.CharField(blank=True, max_length=19, null=True)),
                ('ecartf', models.CharField(blank=True, max_length=10, null=True)),
                ('usaneg', models.CharField(blank=True, max_length=2, null=True)),
                ('poste', models.CharField(blank=True, max_length=4, null=True)),
                ('troncon', models.CharField(blank=True, max_length=4, null=True)),
                ('lieu_rue', models.CharField(blank=True, max_length=45, null=True)),
                ('type_tra', models.CharField(blank=True, max_length=11, null=True)),
                ('sensor', models.CharField(blank=True, max_length=7, null=True)),
                ('classif', models.CharField(blank=True, max_length=3, null=True)),
                ('lpseps', models.CharField(blank=True, max_length=11, null=True)),
                ('permanent', models.CharField(blank=True, max_length=3, null=True)),
                ('c_ehbdo', models.CharField(blank=True, max_length=6, null=True)),
                ('boucon', models.CharField(blank=True, max_length=6, null=True)),
                ('ccd', models.CharField(blank=True, max_length=1, null=True)),
                ('ccf', models.CharField(blank=True, max_length=1, null=True)),
                ('f_long', models.CharField(blank=True, max_length=20, null=True)),
                ('f_surf', models.CharField(blank=True, max_length=20, null=True)),
                ('nom_rue', models.CharField(blank=True, max_length=45, null=True)),
                ('dir1', models.CharField(blank=True, max_length=75, null=True)),
                ('dir2', models.CharField(blank=True, max_length=75, null=True)),
                ('wkb_geometry', django.contrib.gis.db.models.fields.GeometryField(blank=True, null=True, srid=2056)),
            ],
            options={
                'db_table': 'base_tjm_ok',
            },
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('formatter_name', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'brand',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('code', models.SmallIntegerField()),
                ('light', models.BooleanField()),
                ('id_category', models.ForeignKey(db_column='id_category', on_delete=django.db.models.deletion.DO_NOTHING, to='core.category')),
            ],
            options={
                'db_table': 'category',
            },
        ),
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('description', models.TextField()),
            ],
            options={
                'db_table': 'class',
            },
        ),
        migrations.CreateModel(
            name='CoreStructure',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('geom', django.contrib.gis.db.models.fields.GeometryField(srid=2056)),
                ('name', models.CharField(max_length=255)),
                ('label', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'core_structure',
            },
        ),
        migrations.CreateModel(
            name='Count',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('start_service_date', models.DateField()),
                ('end_service_date', models.DateField()),
                ('start_put_date', models.DateField(blank=True, null=True)),
                ('end_put_date', models.DateField(blank=True, null=True)),
                ('start_process_date', models.DateField()),
                ('end_process_date', models.DateField()),
                ('valid', models.BooleanField(blank=True, null=True)),
                ('dysfunction', models.BooleanField(blank=True, null=True)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('id_class', models.ForeignKey(blank=True, db_column='id_class', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.class')),
            ],
            options={
                'db_table': 'count',
            },
        ),
        migrations.CreateModel(
            name='CountAggregate',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('type', models.TextField()),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('file_name', models.TextField()),
                ('import_status', models.SmallIntegerField()),
                ('id_count', models.ForeignKey(db_column='id_count', on_delete=django.db.models.deletion.DO_NOTHING, to='core.count')),
            ],
            options={
                'db_table': 'count_aggregate',
            },
        ),
        migrations.CreateModel(
            name='Installation',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('permanent', models.BooleanField()),
                ('name', models.TextField()),
                ('picture', models.TextField(blank=True, null=True)),
                ('geometry', django.contrib.gis.db.models.fields.GeometryField(blank=True, null=True, srid=2056)),
                ('active', models.BooleanField()),
            ],
            options={
                'db_table': 'installation',
            },
        ),
        migrations.CreateModel(
            name='Lane',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('number', models.SmallIntegerField()),
                ('direction', models.SmallIntegerField()),
                ('direction_desc', models.TextField(blank=True, null=True)),
                ('id_installation', models.ForeignKey(blank=True, db_column='id_installation', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.installation')),
            ],
            options={
                'db_table': 'lane',
            },
        ),
        migrations.CreateModel(
            name='Model',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('card_name', models.TextField(blank=True, null=True)),
                ('configuration', models.TextField(blank=True, null=True)),
                ('id_brand', models.ForeignKey(db_column='id_brand', on_delete=django.db.models.deletion.DO_NOTHING, to='core.brand')),
            ],
            options={
                'db_table': 'model',
            },
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('owner', models.TextField(blank=True, null=True)),
                ('road', models.TextField(blank=True, null=True)),
                ('way', models.CharField(blank=True, max_length=1, null=True)),
                ('start_pr', models.TextField(blank=True, null=True)),
                ('end_pr', models.TextField(blank=True, null=True)),
                ('start_dist', models.DecimalField(blank=True, decimal_places=65535, max_digits=65535, null=True)),
                ('end_dist', models.DecimalField(blank=True, decimal_places=65535, max_digits=65535, null=True)),
                ('place_name', models.TextField(blank=True, null=True)),
                ('geometry', django.contrib.gis.db.models.fields.LineStringField(srid=2056)),
                ('start_validity', models.DateField(blank=True, null=True)),
                ('end_validity', models.DateField(blank=True, null=True)),
            ],
            options={
                'db_table': 'section',
            },
        ),
        migrations.CreateModel(
            name='SensorType',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('permanent', models.BooleanField(blank=True, null=True)),
            ],
            options={
                'db_table': 'sensor_type',
            },
        ),
        migrations.CreateModel(
            name='SpecialPeriod',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('description', models.TextField()),
                ('entity', models.TextField(blank=True, null=True)),
                ('influence', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'special_period',
            },
        ),
        migrations.CreateModel(
            name='CoreBuilding',
            fields=[
                ('structure_ptr', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='core.corestructure')),
                ('stories_count', models.IntegerField()),
            ],
            options={
                'db_table': 'core_building',
            },
        ),
        migrations.CreateModel(
            name='SensorTypeSection',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('geometry', django.contrib.gis.db.models.fields.GeometryField(blank=True, null=True, srid=2056)),
                ('id_section', models.ForeignKey(blank=True, db_column='id_section', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.section')),
                ('id_sensor_type', models.ForeignKey(blank=True, db_column='id_sensor_type', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.sensortype')),
            ],
            options={
                'db_table': 'sensor_type_section',
            },
        ),
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('start_pr', models.TextField(blank=True, null=True)),
                ('end_pr', models.TextField(blank=True, null=True)),
                ('start_dist', models.DecimalField(blank=True, decimal_places=65535, max_digits=65535, null=True)),
                ('end_dist', models.DecimalField(blank=True, decimal_places=65535, max_digits=65535, null=True)),
                ('start_service_date', models.DateField(blank=True, null=True)),
                ('end_service_date', models.DateField(blank=True, null=True)),
                ('geometry', django.contrib.gis.db.models.fields.GeometryField(blank=True, null=True, srid=2056)),
                ('id_lane', models.ForeignKey(blank=True, db_column='id_lane', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.lane')),
                ('id_sensor_type', models.ForeignKey(blank=True, db_column='id_sensor_type', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.sensortype')),
            ],
            options={
                'db_table': 'sensor',
            },
        ),
        migrations.AddField(
            model_name='lane',
            name='id_section',
            field=models.ForeignKey(db_column='id_section', on_delete=django.db.models.deletion.DO_NOTHING, to='core.section'),
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('serial', models.TextField(blank=True, null=True)),
                ('purchase_date', models.DateField(blank=True, null=True)),
                ('name', models.TextField()),
                ('id_model', models.ForeignKey(db_column='id_model', on_delete=django.db.models.deletion.DO_NOTHING, to='core.model')),
            ],
            options={
                'db_table': 'device',
            },
        ),
        migrations.CreateModel(
            name='DamageLog',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('description', models.TextField()),
                ('id_device', models.ForeignKey(db_column='id_device', on_delete=django.db.models.deletion.DO_NOTHING, to='core.device')),
            ],
            options={
                'db_table': 'damage_log',
            },
        ),
        migrations.CreateModel(
            name='CountDetail',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('numbering', models.IntegerField()),
                ('timestamp', models.DateTimeField()),
                ('distance_front_front', models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True)),
                ('distance_front_back', models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True)),
                ('speed', models.SmallIntegerField(blank=True, null=True)),
                ('length', models.SmallIntegerField(blank=True, null=True)),
                ('height', models.CharField(blank=True, max_length=2, null=True)),
                ('fixed', models.BooleanField(blank=True, null=True)),
                ('wrong_way', models.BooleanField(blank=True, null=True)),
                ('file_name', models.TextField()),
                ('import_status', models.SmallIntegerField()),
                ('id_category', models.ForeignKey(db_column='id_category', on_delete=django.db.models.deletion.DO_NOTHING, to='core.category')),
                ('id_count', models.ForeignKey(db_column='id_count', on_delete=django.db.models.deletion.DO_NOTHING, to='core.count')),
                ('id_lane', models.ForeignKey(db_column='id_lane', on_delete=django.db.models.deletion.DO_NOTHING, to='core.lane')),
            ],
            options={
                'db_table': 'count_detail',
            },
        ),
        migrations.CreateModel(
            name='CountAggregateValueSpd',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('value', models.SmallIntegerField()),
                ('low', models.SmallIntegerField()),
                ('high', models.SmallIntegerField()),
                ('id_count_aggregate', models.ForeignKey(db_column='id_count_aggregate', on_delete=django.db.models.deletion.DO_NOTHING, to='core.countaggregate')),
            ],
            options={
                'db_table': 'count_aggregate_value_spd',
            },
        ),
        migrations.CreateModel(
            name='CountAggregateValueSds',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('mean', models.FloatField()),
                ('deviation', models.FloatField()),
                ('id_count_aggregate', models.ForeignKey(db_column='id_count_aggregate', on_delete=django.db.models.deletion.DO_NOTHING, to='core.countaggregate')),
            ],
            options={
                'db_table': 'count_aggregate_value_sds',
            },
        ),
        migrations.CreateModel(
            name='CountAggregateValueLen',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('value', models.SmallIntegerField()),
                ('low', models.SmallIntegerField()),
                ('high', models.SmallIntegerField()),
                ('id_count_aggregate', models.ForeignKey(db_column='id_count_aggregate', on_delete=django.db.models.deletion.DO_NOTHING, to='core.countaggregate')),
            ],
            options={
                'db_table': 'count_aggregate_value_len',
            },
        ),
        migrations.CreateModel(
            name='CountAggregateValueDrn',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('value', models.SmallIntegerField()),
                ('direction', models.SmallIntegerField()),
                ('id_count_aggregate', models.ForeignKey(db_column='id_count_aggregate', on_delete=django.db.models.deletion.DO_NOTHING, to='core.countaggregate')),
            ],
            options={
                'db_table': 'count_aggregate_value_drn',
            },
        ),
        migrations.CreateModel(
            name='CountAggregateValueCnt',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('value', models.SmallIntegerField()),
                ('interval', models.SmallIntegerField()),
                ('id_count_aggregate', models.ForeignKey(db_column='id_count_aggregate', on_delete=django.db.models.deletion.DO_NOTHING, to='core.countaggregate')),
            ],
            options={
                'db_table': 'count_aggregate_value_cnt',
            },
        ),
        migrations.CreateModel(
            name='CountAggregateValueCls',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('value', models.IntegerField()),
                ('id_category', models.ForeignKey(db_column='id_category', on_delete=django.db.models.deletion.DO_NOTHING, to='core.category')),
                ('id_count_aggregate', models.ForeignKey(db_column='id_count_aggregate', on_delete=django.db.models.deletion.DO_NOTHING, to='core.countaggregate')),
            ],
            options={
                'db_table': 'count_aggregate_value_cls',
            },
        ),
        migrations.AddField(
            model_name='countaggregate',
            name='id_lane',
            field=models.ForeignKey(db_column='id_lane', on_delete=django.db.models.deletion.DO_NOTHING, to='core.lane'),
        ),
        migrations.AddField(
            model_name='count',
            name='id_device',
            field=models.ForeignKey(blank=True, db_column='id_device', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.device'),
        ),
        migrations.AddField(
            model_name='count',
            name='id_installation',
            field=models.ForeignKey(db_column='id_installation', on_delete=django.db.models.deletion.DO_NOTHING, to='core.installation'),
        ),
        migrations.AddField(
            model_name='count',
            name='id_model',
            field=models.ForeignKey(db_column='id_model', on_delete=django.db.models.deletion.DO_NOTHING, to='core.model'),
        ),
        migrations.AddField(
            model_name='count',
            name='id_sensor_type',
            field=models.ForeignKey(db_column='id_sensor_type', on_delete=django.db.models.deletion.DO_NOTHING, to='core.sensortype'),
        ),
        migrations.CreateModel(
            name='SensorTypeModel',
            fields=[
                ('id_sensor_type', models.OneToOneField(db_column='id_sensor_type', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='core.sensortype')),
                ('id_model', models.ForeignKey(db_column='id_model', on_delete=django.db.models.deletion.DO_NOTHING, to='core.model')),
            ],
            options={
                'db_table': 'sensor_type_model',
                'unique_together': {('id_sensor_type', 'id_model')},
            },
        ),
        migrations.CreateModel(
            name='SensorTypeInstallation',
            fields=[
                ('id_sensor_type', models.OneToOneField(db_column='id_sensor_type', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='core.sensortype')),
                ('id_installation', models.ForeignKey(db_column='id_installation', on_delete=django.db.models.deletion.DO_NOTHING, to='core.installation')),
            ],
            options={
                'db_table': 'sensor_type_installation',
                'unique_together': {('id_sensor_type', 'id_installation')},
            },
        ),
        migrations.CreateModel(
            name='SensorTypeClass',
            fields=[
                ('id_sensor_type', models.OneToOneField(db_column='id_sensor_type', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='core.sensortype')),
                ('id_class', models.ForeignKey(db_column='id_class', on_delete=django.db.models.deletion.DO_NOTHING, to='core.class')),
            ],
            options={
                'db_table': 'sensor_type_class',
                'unique_together': {('id_sensor_type', 'id_class')},
            },
        ),
        migrations.CreateModel(
            name='ModelClass',
            fields=[
                ('id_model', models.OneToOneField(db_column='id_model', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='core.model')),
                ('id_class', models.ForeignKey(db_column='id_class', on_delete=django.db.models.deletion.DO_NOTHING, to='core.class')),
            ],
            options={
                'db_table': 'model_class',
                'unique_together': {('id_model', 'id_class')},
            },
        ),
        migrations.CreateModel(
            name='ClassCategory',
            fields=[
                ('id_class', models.OneToOneField(db_column='id_class', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='core.class')),
                ('id_category', models.ForeignKey(db_column='id_category', on_delete=django.db.models.deletion.DO_NOTHING, to='core.category')),
            ],
            options={
                'db_table': 'class_category',
                'unique_together': {('id_class', 'id_category')},
            },
        ),
    ]
