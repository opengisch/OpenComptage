# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior

from django.contrib.gis.db import models


class Brand(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.TextField()
    formatter_name = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'brand'


class Category(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.TextField()
    code = models.SmallIntegerField()
    light = models.BooleanField()
    id_category = models.ForeignKey('self', models.DO_NOTHING, db_column='id_category')

    class Meta:
        db_table = 'category'


class Class(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.TextField()
    description = models.TextField()

    class Meta:
        db_table = 'class'


class ClassCategory(models.Model):
    id_class = models.OneToOneField(Class, models.DO_NOTHING, db_column='id_class', primary_key=True)
    id_category = models.ForeignKey(Category, models.DO_NOTHING, db_column='id_category')

    class Meta:
        db_table = 'class_category'
        unique_together = (('id_class', 'id_category'),)


class CoreBuilding(models.Model):
    structure_ptr = models.OneToOneField('CoreStructure', models.DO_NOTHING, primary_key=True)
    stories_count = models.IntegerField()

    class Meta:
        db_table = 'core_building'


class CoreStructure(models.Model):
    id = models.BigAutoField(primary_key=True)
    geom = models.GeometryField(srid=2056)
    name = models.CharField(max_length=255)
    label = models.CharField(max_length=255)

    class Meta:
        db_table = 'core_structure'


class Count(models.Model):
    qdmtk_addlayer = True

    id = models.BigAutoField(primary_key=True)
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
        db_table = 'count'


class CountAggregate(models.Model):
    id = models.BigAutoField(primary_key=True)
    type = models.TextField()
    start = models.DateTimeField()
    end = models.DateTimeField()
    file_name = models.TextField()
    import_status = models.SmallIntegerField()
    id_count = models.ForeignKey(Count, models.DO_NOTHING, db_column='id_count')
    id_lane = models.ForeignKey('Lane', models.DO_NOTHING, db_column='id_lane')

    class Meta:
        db_table = 'count_aggregate'


class CountAggregateValueCls(models.Model):
    id = models.BigAutoField(primary_key=True)
    value = models.IntegerField()
    id_count_aggregate = models.ForeignKey(CountAggregate, models.DO_NOTHING, db_column='id_count_aggregate')
    id_category = models.ForeignKey(Category, models.DO_NOTHING, db_column='id_category')

    class Meta:
        db_table = 'count_aggregate_value_cls'


class CountAggregateValueCnt(models.Model):
    id = models.BigAutoField(primary_key=True)
    value = models.SmallIntegerField()
    interval = models.SmallIntegerField()
    id_count_aggregate = models.ForeignKey(CountAggregate, models.DO_NOTHING, db_column='id_count_aggregate')

    class Meta:
        db_table = 'count_aggregate_value_cnt'


class CountAggregateValueDrn(models.Model):
    id = models.BigAutoField(primary_key=True)
    value = models.SmallIntegerField()
    direction = models.SmallIntegerField()
    id_count_aggregate = models.ForeignKey(CountAggregate, models.DO_NOTHING, db_column='id_count_aggregate')

    class Meta:
        db_table = 'count_aggregate_value_drn'


class CountAggregateValueLen(models.Model):
    id = models.BigAutoField(primary_key=True)
    value = models.SmallIntegerField()
    low = models.SmallIntegerField()
    high = models.SmallIntegerField()
    id_count_aggregate = models.ForeignKey(CountAggregate, models.DO_NOTHING, db_column='id_count_aggregate')

    class Meta:
        db_table = 'count_aggregate_value_len'


class CountAggregateValueSds(models.Model):
    id = models.BigAutoField(primary_key=True)
    mean = models.FloatField()
    deviation = models.FloatField()
    id_count_aggregate = models.ForeignKey(CountAggregate, models.DO_NOTHING, db_column='id_count_aggregate')

    class Meta:
        db_table = 'count_aggregate_value_sds'


class CountAggregateValueSpd(models.Model):
    id = models.BigAutoField(primary_key=True)
    value = models.SmallIntegerField()
    low = models.SmallIntegerField()
    high = models.SmallIntegerField()
    id_count_aggregate = models.ForeignKey(CountAggregate, models.DO_NOTHING, db_column='id_count_aggregate')

    class Meta:
        db_table = 'count_aggregate_value_spd'


class CountDetail(models.Model):
    id = models.BigAutoField(primary_key=True)
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
        db_table = 'count_detail'


class DamageLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()
    id_device = models.ForeignKey('Device', models.DO_NOTHING, db_column='id_device')

    class Meta:
        db_table = 'damage_log'


class Device(models.Model):
    id = models.BigAutoField(primary_key=True)
    serial = models.TextField(blank=True, null=True)
    purchase_date = models.DateField(blank=True, null=True)
    name = models.TextField()
    id_model = models.ForeignKey('Model', models.DO_NOTHING, db_column='id_model')

    class Meta:
        db_table = 'device'


class Installation(models.Model):
    qdmtk_addlayer = True

    id = models.BigAutoField(primary_key=True)
    permanent = models.BooleanField()
    name = models.TextField()
    picture = models.TextField(blank=True, null=True)
    geometry = models.GeometryField(blank=True, null=True, srid=2056)
    active = models.BooleanField()

    class Meta:
        db_table = 'installation'


class Lane(models.Model):
    id = models.BigAutoField(primary_key=True)
    number = models.SmallIntegerField()
    direction = models.SmallIntegerField()
    direction_desc = models.TextField(blank=True, null=True)
    id_installation = models.ForeignKey(Installation, models.DO_NOTHING, db_column='id_installation', blank=True, null=True)
    id_section = models.ForeignKey('Section', models.DO_NOTHING, db_column='id_section')

    class Meta:
        db_table = 'lane'


class Model(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.TextField()
    card_name = models.TextField(blank=True, null=True)
    configuration = models.TextField(blank=True, null=True)
    id_brand = models.ForeignKey(Brand, models.DO_NOTHING, db_column='id_brand')

    class Meta:
        db_table = 'model'


class ModelClass(models.Model):
    id_model = models.OneToOneField(Model, models.DO_NOTHING, db_column='id_model', primary_key=True)
    id_class = models.ForeignKey(Class, models.DO_NOTHING, db_column='id_class')

    class Meta:
        db_table = 'model_class'
        unique_together = (('id_model', 'id_class'),)


class Section(models.Model):
    qdmtk_addlayer = True

    id = models.CharField(primary_key=True, max_length=20)
    name = models.TextField()
    owner = models.TextField(blank=True, null=True)
    road = models.TextField(blank=True, null=True)
    way = models.CharField(max_length=1, blank=True, null=True)
    start_pr = models.TextField(blank=True, null=True)
    end_pr = models.TextField(blank=True, null=True)
    start_dist = models.DecimalField(max_digits=1000, decimal_places=500, blank=True, null=True)
    end_dist = models.DecimalField(max_digits=1000, decimal_places=500, blank=True, null=True)
    place_name = models.TextField(blank=True, null=True)
    geometry = models.LineStringField(srid=2056)
    start_validity = models.DateField(blank=True, null=True)
    end_validity = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'section'


class Sensor(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_lane = models.ForeignKey(Lane, models.DO_NOTHING, db_column='id_lane', blank=True, null=True)
    id_sensor_type = models.ForeignKey('SensorType', models.DO_NOTHING, db_column='id_sensor_type', blank=True, null=True)
    start_pr = models.TextField(blank=True, null=True)
    end_pr = models.TextField(blank=True, null=True)
    start_dist = models.DecimalField(max_digits=1000, decimal_places=500, blank=True, null=True)
    end_dist = models.DecimalField(max_digits=1000, decimal_places=500, blank=True, null=True)
    start_service_date = models.DateField(blank=True, null=True)
    end_service_date = models.DateField(blank=True, null=True)
    geometry = models.GeometryField(blank=True, null=True, srid=2056)

    class Meta:
        db_table = 'sensor'


class SensorType(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.TextField()
    permanent = models.BooleanField(blank=True, null=True)

    class Meta:
        db_table = 'sensor_type'


class SensorTypeClass(models.Model):
    id_sensor_type = models.OneToOneField(SensorType, models.DO_NOTHING, db_column='id_sensor_type', primary_key=True)
    id_class = models.ForeignKey(Class, models.DO_NOTHING, db_column='id_class')

    class Meta:
        db_table = 'sensor_type_class'
        unique_together = (('id_sensor_type', 'id_class'),)


class SensorTypeInstallation(models.Model):
    id_sensor_type = models.OneToOneField(SensorType, models.DO_NOTHING, db_column='id_sensor_type', primary_key=True)
    id_installation = models.ForeignKey(Installation, models.DO_NOTHING, db_column='id_installation')

    class Meta:
        db_table = 'sensor_type_installation'
        unique_together = (('id_sensor_type', 'id_installation'),)


class SensorTypeModel(models.Model):
    id_sensor_type = models.OneToOneField(SensorType, models.DO_NOTHING, db_column='id_sensor_type', primary_key=True)
    id_model = models.ForeignKey(Model, models.DO_NOTHING, db_column='id_model')

    class Meta:
        db_table = 'sensor_type_model'
        unique_together = (('id_sensor_type', 'id_model'),)


class SensorTypeSection(models.Model):
    id = models.BigAutoField(primary_key=True)
    geometry = models.GeometryField(blank=True, null=True, srid=2056)
    id_sensor_type = models.ForeignKey(SensorType, models.DO_NOTHING, db_column='id_sensor_type', blank=True, null=True)
    id_section = models.ForeignKey(Section, models.DO_NOTHING, db_column='id_section', blank=True, null=True)

    class Meta:
        db_table = 'sensor_type_section'


class SpecialPeriod(models.Model):
    id = models.BigAutoField(primary_key=True)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()
    entity = models.TextField(blank=True, null=True)
    influence = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'special_period'
