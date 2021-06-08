# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class BaseTjmOk(models.Model):
    ogc_fid = models.AutoField(primary_key=True)
    fsection = models.CharField(max_length=20, blank=True, null=True)
    fonctionel = models.CharField(max_length=4, blank=True, null=True)
    f_prop = models.CharField(max_length=12, blank=True, null=True)
    f_axe = models.CharField(max_length=64, blank=True, null=True)
    f_sens = models.CharField(max_length=1, blank=True, null=True)
    f_pr_d = models.CharField(max_length=64, blank=True, null=True)
    f_dist_d = models.CharField(max_length=19, blank=True, null=True)
    ecartd = models.CharField(max_length=10, blank=True, null=True)
    f_pr_f = models.CharField(max_length=64, blank=True, null=True)
    f_dist_f = models.CharField(max_length=19, blank=True, null=True)
    ecartf = models.CharField(max_length=10, blank=True, null=True)
    usaneg = models.CharField(max_length=2, blank=True, null=True)
    poste = models.CharField(max_length=4, blank=True, null=True)
    troncon = models.CharField(max_length=4, blank=True, null=True)
    lieu_rue = models.CharField(max_length=45, blank=True, null=True)
    type_tra = models.CharField(max_length=11, blank=True, null=True)
    sensor = models.CharField(max_length=7, blank=True, null=True)
    classif = models.CharField(max_length=3, blank=True, null=True)
    lpseps = models.CharField(max_length=11, blank=True, null=True)
    permanent = models.CharField(max_length=3, blank=True, null=True)
    c_ehbdo = models.CharField(max_length=6, blank=True, null=True)
    boucon = models.CharField(max_length=6, blank=True, null=True)
    ccd = models.CharField(max_length=1, blank=True, null=True)
    ccf = models.CharField(max_length=1, blank=True, null=True)
    f_long = models.CharField(max_length=20, blank=True, null=True)
    f_surf = models.CharField(max_length=20, blank=True, null=True)
    nom_rue = models.CharField(max_length=45, blank=True, null=True)
    dir1 = models.CharField(max_length=75, blank=True, null=True)
    dir2 = models.CharField(max_length=75, blank=True, null=True)
    wkb_geometry = models.GeometryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'base_tjm_ok'


class Brand(models.Model):
    name = models.TextField()
    formatter_name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'brand'


class Category(models.Model):
    name = models.TextField()
    code = models.SmallIntegerField()
    light = models.BooleanField()
    id_category = models.ForeignKey('self', models.DO_NOTHING, db_column='id_category')

    class Meta:
        managed = False
        db_table = 'category'


class Class(models.Model):
    name = models.TextField()
    description = models.TextField()

    class Meta:
        managed = False
        db_table = 'class'


class ClassCategory(models.Model):
    id_class = models.OneToOneField(Class, models.DO_NOTHING, db_column='id_class', primary_key=True)
    id_category = models.ForeignKey(Category, models.DO_NOTHING, db_column='id_category')

    class Meta:
        managed = False
        db_table = 'class_category'
        unique_together = (('id_class', 'id_category'),)


class CoreBuilding(models.Model):
    structure_ptr = models.OneToOneField('CoreStructure', models.DO_NOTHING, primary_key=True)
    stories_count = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'core_building'


class CoreStructure(models.Model):
    id = models.BigAutoField(primary_key=True)
    geom = models.GeometryField()
    name = models.CharField(max_length=255)
    label = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'core_structure'


class Count(models.Model):
    start_service_date = models.DateField()
    end_service_date = models.DateField()
    start_put_date = models.DateField(blank=True, null=True)
    end_put_date = models.DateField(blank=True, null=True)
    start_process_date = models.DateField()
    end_process_date = models.DateField()
    valid = models.BooleanField(blank=True, null=True)
    dysfunction = models.BooleanField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    id_model = models.ForeignKey('Model', models.DO_NOTHING, db_column='id_model')
    id_device = models.ForeignKey('Device', models.DO_NOTHING, db_column='id_device', blank=True, null=True)
    id_sensor_type = models.ForeignKey('SensorType', models.DO_NOTHING, db_column='id_sensor_type')
    id_class = models.ForeignKey(Class, models.DO_NOTHING, db_column='id_class', blank=True, null=True)
    id_installation = models.ForeignKey('Installation', models.DO_NOTHING, db_column='id_installation')

    class Meta:
        managed = False
        db_table = 'count'


class CountAggregate(models.Model):
    type = models.TextField()
    start = models.DateTimeField()
    end = models.DateTimeField()
    file_name = models.TextField()
    import_status = models.SmallIntegerField()
    id_count = models.ForeignKey(Count, models.DO_NOTHING, db_column='id_count')
    id_lane = models.ForeignKey('Lane', models.DO_NOTHING, db_column='id_lane')

    class Meta:
        managed = False
        db_table = 'count_aggregate'


class CountAggregateValueCls(models.Model):
    value = models.IntegerField()
    id_count_aggregate = models.ForeignKey(CountAggregate, models.DO_NOTHING, db_column='id_count_aggregate')
    id_category = models.ForeignKey(Category, models.DO_NOTHING, db_column='id_category')

    class Meta:
        managed = False
        db_table = 'count_aggregate_value_cls'


class CountAggregateValueCnt(models.Model):
    value = models.SmallIntegerField()
    interval = models.SmallIntegerField()
    id_count_aggregate = models.ForeignKey(CountAggregate, models.DO_NOTHING, db_column='id_count_aggregate')

    class Meta:
        managed = False
        db_table = 'count_aggregate_value_cnt'


class CountAggregateValueDrn(models.Model):
    value = models.SmallIntegerField()
    direction = models.SmallIntegerField()
    id_count_aggregate = models.ForeignKey(CountAggregate, models.DO_NOTHING, db_column='id_count_aggregate')

    class Meta:
        managed = False
        db_table = 'count_aggregate_value_drn'


class CountAggregateValueLen(models.Model):
    value = models.SmallIntegerField()
    low = models.SmallIntegerField()
    high = models.SmallIntegerField()
    id_count_aggregate = models.ForeignKey(CountAggregate, models.DO_NOTHING, db_column='id_count_aggregate')

    class Meta:
        managed = False
        db_table = 'count_aggregate_value_len'


class CountAggregateValueSds(models.Model):
    mean = models.FloatField()
    deviation = models.FloatField()
    id_count_aggregate = models.ForeignKey(CountAggregate, models.DO_NOTHING, db_column='id_count_aggregate')

    class Meta:
        managed = False
        db_table = 'count_aggregate_value_sds'


class CountAggregateValueSpd(models.Model):
    value = models.SmallIntegerField()
    low = models.SmallIntegerField()
    high = models.SmallIntegerField()
    id_count_aggregate = models.ForeignKey(CountAggregate, models.DO_NOTHING, db_column='id_count_aggregate')

    class Meta:
        managed = False
        db_table = 'count_aggregate_value_spd'


class CountDetail(models.Model):
    numbering = models.IntegerField()
    timestamp = models.DateTimeField()
    distance_front_front = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    distance_front_back = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    speed = models.SmallIntegerField(blank=True, null=True)
    length = models.SmallIntegerField(blank=True, null=True)
    height = models.CharField(max_length=2, blank=True, null=True)
    fixed = models.BooleanField(blank=True, null=True)
    wrong_way = models.BooleanField(blank=True, null=True)
    file_name = models.TextField()
    import_status = models.SmallIntegerField()
    id_lane = models.ForeignKey('Lane', models.DO_NOTHING, db_column='id_lane')
    id_count = models.ForeignKey(Count, models.DO_NOTHING, db_column='id_count')
    id_category = models.ForeignKey(Category, models.DO_NOTHING, db_column='id_category')

    class Meta:
        managed = False
        db_table = 'count_detail'


class DamageLog(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()
    id_device = models.ForeignKey('Device', models.DO_NOTHING, db_column='id_device')

    class Meta:
        managed = False
        db_table = 'damage_log'


class Device(models.Model):
    serial = models.TextField(blank=True, null=True)
    purchase_date = models.DateField(blank=True, null=True)
    name = models.TextField()
    id_model = models.ForeignKey('Model', models.DO_NOTHING, db_column='id_model')

    class Meta:
        managed = False
        db_table = 'device'


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class Installation(models.Model):
    permanent = models.BooleanField()
    name = models.TextField()
    picture = models.TextField(blank=True, null=True)
    geometry = models.GeometryField(blank=True, null=True)
    active = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'installation'


class Lane(models.Model):
    number = models.SmallIntegerField()
    direction = models.SmallIntegerField()
    direction_desc = models.TextField(blank=True, null=True)
    id_installation = models.ForeignKey(Installation, models.DO_NOTHING, db_column='id_installation', blank=True, null=True)
    id_section = models.ForeignKey('Section', models.DO_NOTHING, db_column='id_section')

    class Meta:
        managed = False
        db_table = 'lane'


class Model(models.Model):
    name = models.TextField()
    card_name = models.TextField(blank=True, null=True)
    configuration = models.TextField(blank=True, null=True)
    id_brand = models.ForeignKey(Brand, models.DO_NOTHING, db_column='id_brand')

    class Meta:
        managed = False
        db_table = 'model'


class ModelClass(models.Model):
    id_model = models.OneToOneField(Model, models.DO_NOTHING, db_column='id_model', primary_key=True)
    id_class = models.ForeignKey(Class, models.DO_NOTHING, db_column='id_class')

    class Meta:
        managed = False
        db_table = 'model_class'
        unique_together = (('id_model', 'id_class'),)


class Section(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    name = models.TextField()
    owner = models.TextField(blank=True, null=True)
    road = models.TextField(blank=True, null=True)
    way = models.CharField(max_length=1, blank=True, null=True)
    start_pr = models.TextField(blank=True, null=True)
    end_pr = models.TextField(blank=True, null=True)
    start_dist = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    end_dist = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    place_name = models.TextField(blank=True, null=True)
    geometry = models.GeometryField()
    start_validity = models.DateField(blank=True, null=True)
    end_validity = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'section'


class Sensor(models.Model):
    id_lane = models.ForeignKey(Lane, models.DO_NOTHING, db_column='id_lane', blank=True, null=True)
    id_sensor_type = models.ForeignKey('SensorType', models.DO_NOTHING, db_column='id_sensor_type', blank=True, null=True)
    start_pr = models.TextField(blank=True, null=True)
    end_pr = models.TextField(blank=True, null=True)
    start_dist = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    end_dist = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    start_service_date = models.DateField(blank=True, null=True)
    end_service_date = models.DateField(blank=True, null=True)
    geometry = models.GeometryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sensor'


class SensorType(models.Model):
    name = models.TextField()
    permanent = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sensor_type'


class SensorTypeClass(models.Model):
    id_sensor_type = models.OneToOneField(SensorType, models.DO_NOTHING, db_column='id_sensor_type', primary_key=True)
    id_class = models.ForeignKey(Class, models.DO_NOTHING, db_column='id_class')

    class Meta:
        managed = False
        db_table = 'sensor_type_class'
        unique_together = (('id_sensor_type', 'id_class'),)


class SensorTypeInstallation(models.Model):
    id_sensor_type = models.OneToOneField(SensorType, models.DO_NOTHING, db_column='id_sensor_type', primary_key=True)
    id_installation = models.ForeignKey(Installation, models.DO_NOTHING, db_column='id_installation')

    class Meta:
        managed = False
        db_table = 'sensor_type_installation'
        unique_together = (('id_sensor_type', 'id_installation'),)


class SensorTypeModel(models.Model):
    id_sensor_type = models.OneToOneField(SensorType, models.DO_NOTHING, db_column='id_sensor_type', primary_key=True)
    id_model = models.ForeignKey(Model, models.DO_NOTHING, db_column='id_model')

    class Meta:
        managed = False
        db_table = 'sensor_type_model'
        unique_together = (('id_sensor_type', 'id_model'),)


class SensorTypeSection(models.Model):
    geometry = models.GeometryField(blank=True, null=True)
    id_sensor_type = models.ForeignKey(SensorType, models.DO_NOTHING, db_column='id_sensor_type', blank=True, null=True)
    id_section = models.ForeignKey(Section, models.DO_NOTHING, db_column='id_section', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sensor_type_section'


class SpecialPeriod(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()
    entity = models.TextField(blank=True, null=True)
    influence = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'special_period'
