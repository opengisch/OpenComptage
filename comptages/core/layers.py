import os

from qgis.PyQt.QtCore import QObject
from qgis.PyQt.QtSql import QSqlDatabase, QSqlQuery
from qgis.core import (
    QgsProject, QgsEditorWidgetSetup, QgsVectorLayer,
    QgsCoordinateReferenceSystem, QgsDataSourceUri,
    QgsAction, QgsFeatureRequest, QgsExpressionContextUtils)
from qgis.utils import iface

from comptages.core.definitions import LAYER_DEFINITIONS
from comptages.core.settings import Settings
from comptages.core.utils import push_info


class Layers(QObject):
    IMPORT_STATUS_QUARANTINE = 1
    IMPORT_STATUS_DEFINITIVE = 0

    def __init__(self):
        QObject.__init__(self)
        self.layers = {}

        self.highlighted_sections = []
        self.db = None

    def load_layers(self):
        settings = Settings()

        group_comptages = QgsProject.instance().layerTreeRoot().findGroup(
            'Comptages')
        group_extra = QgsProject.instance().layerTreeRoot().findGroup(
            'Extra')

        if group_comptages is None:
            group_comptages = QgsProject.instance().layerTreeRoot().addGroup(
                'Comptages')

        if group_extra is None and settings.value("extra_layers"):
            group_extra = group_comptages.addGroup('Extra')

        for key in LAYER_DEFINITIONS:
            layer_definition = LAYER_DEFINITIONS[key]

            if not QgsProject.instance().mapLayersByName(
                    layer_definition['display_name']):

                layer = self.load_layer(
                    'comptages',  # Schema
                    layer_definition['table'],
                    layer_definition['geometry'],
                    layer_definition['sql'],
                    layer_definition['display_name'],
                    layer_definition['id'],
                    layer_definition['epsg'],
                )

                if layer_definition['legend']:
                    group_comptages.addLayer(layer)
                elif settings.value("extra_layers"):
                    group_extra.addLayer(layer)

                self.layers[key] = layer

        self.apply_qml_styles()
        self.add_layer_actions()
        self.create_relations()
        iface.setActiveLayer(self.layers['section'])

        self.populate_list_of_highlighted_sections()

        self.layers['count'].featureAdded.connect(self.on_count_added)

    def apply_qml_styles(self):
        for key in LAYER_DEFINITIONS:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            qml_file_path = os.path.join(
                current_dir, os.pardir, 'qml', '{}.qml'.format(key))
            self.layers[key].loadNamedStyle(qml_file_path)

    def create_relations(self):
        # Real relation
        # rel = QgsRelation()
        # rel.setName('Relation installation - count')
        # rel.setId('rel_installation_count')
        # rel.setReferencedLayer(self.layers['installation'].id())
        # rel.setReferencingLayer(self.layers['count'].id())
        # rel.addFieldPair('id_installation', 'id')
        # QgsProject.instance().relationManager().addRelation(rel)

        widget = QgsEditorWidgetSetup(
            'ValueRelation',
            {
                'AllowMulti':       False,
                'AllowNull':        False,
                'FilterExpression': '',
                'Key':              'id',
                'Layer':            self.layers['installation'].id(),
                'OrderByValue':     False,
                'UseCompleter':     False,
                'Value':            'name'
            }
        )
        data_provider = self.layers['count'].dataProvider()
        index = data_provider.fieldNameIndex('id_installation')
        self.layers['count'].setEditorWidgetSetup(index, widget)

        widget = QgsEditorWidgetSetup(
            'ValueRelation',
            {
                'AllowMulti':       False,
                'AllowNull':        False,
                'FilterExpression': '',
                'Key':              'id',
                'Layer':            self.layers['class'].id(),
                'OrderByValue':     False,
                'UseCompleter':     False,
                'Value':            'name'
            }
        )
        data_provider = self.layers['count'].dataProvider()
        index = data_provider.fieldNameIndex('id_class')
        self.layers['count'].setEditorWidgetSetup(index, widget)

        widget = QgsEditorWidgetSetup(
            'ValueRelation',
            {
                'AllowMulti':       False,
                'AllowNull':        False,
                'FilterExpression': '',
                'Key':              'id',
                'Layer':            self.layers['sensor_type'].id(),
                'OrderByValue':     False,
                'UseCompleter':     False,
                'Value':            'name'
            }
        )
        data_provider = self.layers['count'].dataProvider()
        index = data_provider.fieldNameIndex('id_sensor_type')
        self.layers['count'].setEditorWidgetSetup(index, widget)

        widget = QgsEditorWidgetSetup(
            'ValueRelation',
            {
                'AllowMulti':       False,
                'AllowNull':        False,
                'FilterExpression': '',
                'Key':              'id',
                'Layer':            self.layers['device'].id(),
                'OrderByValue':     False,
                'UseCompleter':     False,
                'Value':            'name'
            }
        )
        data_provider = self.layers['count'].dataProvider()
        index = data_provider.fieldNameIndex('id_device')
        self.layers['count'].setEditorWidgetSetup(index, widget)

        widget = QgsEditorWidgetSetup(
            'ValueRelation',
            {
                'AllowMulti':       False,
                'AllowNull':        False,
                'FilterExpression': '',
                'Key':              'id',
                'Layer':            self.layers['model'].id(),
                'OrderByValue':     False,
                'UseCompleter':     False,
                'Value':            'name'
            }
        )
        data_provider = self.layers['count'].dataProvider()
        index = data_provider.fieldNameIndex('id_model')
        self.layers['count'].setEditorWidgetSetup(index, widget)

    def load_layer(
            self, schema, layer_name, geometry, sql, display_name, id_col='',
            epsg=None):

        settings = Settings()
        uri = QgsDataSourceUri()
        uri.setConnection(
            settings.value("db_host"),
            str(settings.value("db_port")),
            settings.value("db_name"),
            settings.value("db_username"),
            settings.value("db_password")
        )

        uri.setDataSource(schema, layer_name, geometry, sql, id_col)
        layer = QgsVectorLayer(uri.uri(), display_name, "postgres")
        if epsg is not None:
            crs = QgsCoordinateReferenceSystem(epsg)
            layer.setCrs(crs)

        QgsProject.instance().addMapLayer(layer, addToLegend=False)

        return layer

    def add_layer_actions(self):
        action_manager = self.layers['count'].actions()
        action_manager.clearActions()

        action = QgsAction(
            QgsAction.GenericPython,
            'Exporter la configuration',
            ("from qgis.utils import plugins\n"
             "plugins['comptages'].do_export_configuration_action([% $id %])")
        )
        action.setActionScopes(['Feature'])
        action_manager.addAction(action)

        action = QgsAction(
            QgsAction.GenericPython,
            'Importation',
            ("from qgis.utils import plugins\n"
             "plugins['comptages'].do_import_single_file_action([% $id %])")
        )
        action.setActionScopes(['Feature'])
        action_manager.addAction(action)

        action = QgsAction(
            QgsAction.GenericPython,
            'Creer un rapport',
            ("from qgis.utils import plugins\n"
             "plugins['comptages'].do_generate_report_action([% $id %])")
        )
        action.setActionScopes(['Feature'])
        action_manager.addAction(action)

        action = QgsAction(
            QgsAction.GenericPython,
            'Creer un plan',
            ("from qgis.utils import plugins\n"
             "plugins['comptages'].do_export_plan_action([% $id %])")
        )
        action.setActionScopes(['Feature'])
        action_manager.addAction(action)

        action = QgsAction(
            QgsAction.GenericPython,
            'Générer les graphiques',
            ("from qgis.utils import plugins\n"
             "plugins['comptages'].do_generate_chart_action([% $id %])")
        )
        action.setActionScopes(['Feature'])
        action_manager.addAction(action)

    def create_count(self):

        layer = self.layers['section']

        selected_count = layer.selectedFeatureCount()
        if selected_count == 0:
            push_info("Veuillez sélectionner un tronçon")
            return
        elif selected_count > 1:
            push_info("Veuillez ne sélectionner qu'un tronçon")
            return
        else:
            selected_feature = next(layer.getSelectedFeatures())

            lanes = self.get_lanes_of_section(selected_feature.attribute('id'))
            installation = self.get_installation_of_lane(
                next(lanes).attribute('id'))

            # Save the id of the installation related to the selected section
            # so we can use in the count form to automatically select the
            # installation in the combobox
            QgsExpressionContextUtils.setProjectVariable(
                QgsProject.instance(),
                'selected_installation', installation.attribute('id'))
            self.layers['count'].startEditing()
            iface.setActiveLayer(self.layers['count'])
            iface.actionAddFeature().trigger()

    def on_count_added(self):
        """Called when a count is added to the layer.
        Refresh the map"""

        self.populate_list_of_highlighted_sections()
        self.layers['section'].triggerRepaint()

    def edit_count(self):
        """Open attribute table of count filtered with only the
        features related to the selected section"""

        # TODO manage error if nothing is to be showed
        # TODO display messages with the correct bar
        layer = self.layers['section']

        selected_count = layer.selectedFeatureCount()
        if selected_count == 0:
            push_info("Veuillez sélectionner un tronçon")
            return
        elif selected_count > 1:
            push_info("Veuillez ne sélectionner qu'un tronçon")
            return
        else:
            selected_feature = next(layer.getSelectedFeatures())
            counts = self.get_counts_of_section(
                selected_feature.attribute('id'))
            ids = []
            for c in counts:
                ids.append(c.attribute('id'))
            self.open_count_attribute_table_and_filter(ids)

    def open_count_attribute_table_and_filter(self, count_ids):
        """Open the attribute table of count filtered on the passed ids"""
        if not count_ids:
            push_info("No counts found for this section")
            return

        iface.showAttributeTable(
            self.layers['count'],
            '"id" in ({})'.format(", ".join(map(str, count_ids))))

    def get_counts_of_section(self, section_id):
        """Return a list of all count features related with the passed
        section"""
        try:
            lanes = self.get_lanes_of_section(section_id)
            installation = self.get_installation_of_lane(
                next(lanes).attribute('id'))
            counts = self.get_counts_of_installation(
                installation.attribute('id'))
        except StopIteration:
            return []

        return counts

    def get_lanes_of_section(self, section_id):
        """Return a list of the lane features of the passed section"""
        request = QgsFeatureRequest().setFilterExpression(
            '"id_section" = \'{}\''.format(section_id)
        )

        return self.layers['lane'].getFeatures(request)

    def get_installation_of_lane(self, lane_id):
        """Return the installation feature of the passes lane"""
        lane = next(self.layers['lane'].getFeatures(
            '"id"={}'.format(lane_id)))
        installation_id = lane.attribute('id_installation')

        return next(self.layers['installation'].getFeatures(
            '"id"={}'.format(installation_id)))

    def get_counts_of_installation(self, installation_id):
        """Return a list of count features related with the passsed
        installation"""
        # TODO verify if more than one layer is returned

        request = QgsFeatureRequest().setFilterExpression(
            '"id_installation" = {}'.format(installation_id)
        )

        return self.layers['count'].getFeatures(request)

    def is_section_highlighted(self, section_id):
        """Return if the passed section has related counts with the current
        filter settings"""

        # TODO optimize with a cached list of sections or using a faster query

        if section_id in self.highlighted_sections:
            return True
        return False

    def populate_list_of_highlighted_sections(
            self, start_date=None, end_date=None, permanent=None,
            sensor=None):
        """Return a list of highlighted sections. Directly on the db
        for performances"""

        self.highlighted_sections = []
        self.init_db_connection()

        query = QSqlQuery(self.db)

        wheres = []
        if start_date:
            wheres.append(
                "c.start_process_date >= '{}'::date".format(start_date))
        if end_date:
            wheres.append("c.end_process_date <= '{}'::date".format(end_date))
        if permanent is not None:
                    wheres.append("i.permanent = '{}'::bool".format(permanent))
        if sensor:
            # TODO
            pass

        where_str = ''
        if wheres:
            where_str = "where " + " and ".join(wheres)

        query_str = ("select distinct l.id_section from comptages.lane as l "
                     "inner join comptages.installation as i on "
                     "(l.id_installation = i.id) inner join "
                     "comptages.count as c on (i.id = c.id_installation) "
                     "{};".format(where_str))

        query.exec_(query_str)

        while query.next():
            self.highlighted_sections.append(str(query.value(0)).strip())

    def apply_filter(self, start_date, end_date, installation, sensor):
        if installation == 0:
            permanent = None
        if installation == 1:
            permanent = True
        if installation == 2:
            permanent = False

        # TODO
        sensor = ''

        self.populate_list_of_highlighted_sections(
            start_date, end_date, permanent, sensor)
        self.layers['section'].triggerRepaint()

    def is_connected(self):
        """Return if the plugin is connected to the database"""
        if self.db is None:
            return False
        return True

    def init_db_connection(self):

        if self.db is None:

            settings = Settings()

            self.db = QSqlDatabase.addDatabase("QPSQL")
            self.db.setHostName(settings.value("db_host"))
            self.db.setPort(settings.value("db_port"))
            self.db.setDatabaseName(settings.value("db_name"))
            self.db.setUserName(settings.value("db_username"))
            self.db.setPassword(settings.value("db_password"))
            self.db.open()

    def close_db_connection(self):
        if self.db is not None:
            self.db.close()
            self.db = None

    def get_installation_name_of_count(self, count_id):
        return self.get_installation_of_count(count_id).attribute('name')

    def get_installation_of_count(self, count_id):
        count = self.get_count(count_id)
        installation = self.get_installation(
            count.attribute('id_installation'))
        return installation

    def get_sections_of_count(self, count_id):
        """Return the sections related to a count"""

        count = self.get_count(count_id)
        installation_id = count.attribute('id_installation')
        lanes = self.get_lanes_of_installation(installation_id)

        # Get only distinct section ids
        section_ids = set()
        for lane in lanes:
            section_ids.add(lane.attribute('id_section'))

        sections = []
        for section_id in section_ids:
            sections.append(self.get_section(section_id))

        return sections

    def get_count(self, count_id):
        """Return the count feature"""

        request = QgsFeatureRequest().setFilterExpression(
            '"id" = {}'.format(count_id)
        )

        return next(self.layers['count'].getFeatures(request))

    def get_installation(self, installation_id):

        request = QgsFeatureRequest().setFilterExpression(
            '"id" = {}'.format(installation_id)
        )

        return next(self.layers['installation'].getFeatures(request))

    def get_lanes_of_installation(self, installation_id):

        request = QgsFeatureRequest().setFilterExpression(
            '"id_installation" = {}'.format(installation_id)
        )

        return self.layers['lane'].getFeatures(request)

    def get_section(self, section_id):
        request = QgsFeatureRequest().setFilterExpression(
            '"id" = {}'.format(section_id)
        )

        return next(self.layers['section'].getFeatures(request))

    def insert_count_detail_row(self, row, count_id, file_name):
        self.init_db_connection()
        query = QSqlQuery(self.db)

        query_str = ("insert into comptages.count_detail ("
                     "numbering, timestamp, "
                     "distance_front_front, distance_front_back, "
                     "speed, length, height, "
                     "file_name, import_status, "
                     "id_lane, id_count, id_category) values ("
                     "{}, '{}', {}, {}, {}, {}, '{}', '{}', {}, {}, "
                     "{}, {})".format(
                         row['numbering'],
                         row['timestamp'],
                         row['distance_front_front'],
                         row['distance_front_back'],
                         row['speed'],
                         row['length'],
                         row['height'],
                         file_name,
                         self.IMPORT_STATUS_QUARANTINE,
                         row['lane'],
                         count_id,
                         row['category_id']))

        query.exec_(query_str)

    def insert_count_aggregate_row(self, row, row_type, count_id, file_name,
                                   bins):
        self.init_db_connection()
        query = QSqlQuery(self.db)

        lanes = {1: 2345, 2: 2346}

        query_str = ("insert into comptages.count_aggregate ("
                     "type, \"start\", \"end\", file_name, import_status, "
                     "id_count, id_lane) "
                     "values ("
                     "'{}', '{}', '{}', '{}', {}, {}, {})".format(
                         row_type,
                         row['start'],
                         row['end'],
                         file_name,
                         self.IMPORT_STATUS_QUARANTINE,
                         count_id,
                         lanes[row['channel']]))

        query_str_value = ""
        if row_type == 'SPD':
            query_str_value = self._create_query_str_aggregate_spd(
                row, bins)
        elif row_type == 'LEN':
            query_str_value = self._create_query_str_aggregate_len(
                row, bins)
        elif row_type == 'CLS':
            query_str_value = self._create_query_str_aggregate_cls(
                row, bins)
        elif row_type == 'SDS':
            # Insert the values in the SPD table and only the
            # mean and the deviation in the SDS table
            query_str_value = self._create_query_str_aggregate_spd(
                row, bins)
            query_str_value.append(self._create_query_str_aggregate_sds(
                row, bins))
        elif row_type == 'DRN':
            query_str_value = self._create_query_str_aggregate_drn(
                row, bins)
        elif row_type == 'CNT':
            query_str_value = self._create_query_str_aggregate_cnt(
                row, bins)

        query.exec_(query_str)

        for _ in query_str_value:
            query.exec_(_)

    def _create_query_str_aggregate_spd(self, row, spdbins):
        queries = []
        for i in range(1, len(spdbins)):
            data = row['data_{}'.format(i)]
            if not data == '':
                speed_low = spdbins[i-1]
                speed_high = spdbins[i]
                queries.append(
                    ("insert into comptages.count_aggregate_value_spd ("
                     "value, low, high, "
                     "id_count_aggregate) values ("
                     "{}, {}, {}, "
                     "(select currval('comptages.count_aggregate_id_seq'))"
                     ")".format(
                         data,
                         speed_low,
                         speed_high)))
        return queries

    def _create_query_str_aggregate_sds(self, row, spdbins):
        query = ''
        speed_data_cols = len(spdbins) - 1
        mean = int(row['data_{}'.format(speed_data_cols + 1)]) / 10
        deviation = int(row['data_{}'.format(speed_data_cols + 2)]) / 10
        query = ("insert into comptages.count_aggregate_value_sds ("
                 "mean, deviation, "
                 "id_count_aggregate) values ("
                 "{}, {}, "
                 "(select currval('comptages.count_aggregate_id_seq'))"
                 ")".format(
                     mean,
                     deviation))
        return query

    def _create_query_str_aggregate_len(self, row, lenbins):
        queries = []

        for i in range(1, len(lenbins)):
            data = row['data_{}'.format(i)]
            if not data == '':
                length_low = lenbins[i-1]
                length_high = lenbins[i]
                queries.append(
                    ("insert into comptages.count_aggregate_value_len ("
                     "value, low, high, "
                     "id_count_aggregate) values ("
                     "{}, {}, {}, "
                     "(select currval('comptages.count_aggregate_id_seq'))"
                     ")".format(
                         data,
                         length_low,
                         length_high)))

        return queries

    def _create_query_str_aggregate_cls(self, row, catbins):
        queries = []

        for i in range(1, len(catbins)+1):
            data = row['data_{}'.format(i)]
            if not data == '':
                category = catbins[i-1]
                queries.append(
                    ("insert into comptages.count_aggregate_value_cls ("
                     "value, id_category, "
                     "id_count_aggregate) values ("
                     "{}, {}, "
                     "(select currval('comptages.count_aggregate_id_seq'))"
                     ")".format(
                         data,
                         category)))
        return queries

    def _create_query_str_aggregate_drn(self, row, dirbins):
        queries = []
        for i in range(1, dirbins+1):
            data = row['data_{}'.format(i)]
            if not data == '':
                direction = i
                queries.append(
                    ("insert into comptages.count_aggregate_value_drn ("
                     "value, direction, "
                     "id_count_aggregate) values ("
                     "{}, {}, "
                     "(select currval('comptages.count_aggregate_id_seq'))"
                     ")".format(
                         data,
                         direction)))
        return queries

    def _create_query_str_aggregate_cnt(self, row, countbins):
        queries = []
        for i in range(1, countbins+1):
            data = row['data_{}'.format(i)]
            if not data == '':
                countbin = i
                queries.append(
                    ("insert into comptages.count_aggregate_value_cnt ("
                     "value, interval, "
                     "id_count_aggregate) values ("
                     "{}, {}, "
                     "(select currval('comptages.count_aggregate_id_seq'))"
                     ")".format(
                         data,
                         countbin)))
        return queries

    def get_category_bins(self, class_name):
        """Return an array with the ids of the categories of the
        passed class"""

        self.init_db_connection()
        query = QSqlQuery(self.db)

        query_str = (
            "select cc.id_category from "
            "comptages.class_category as cc "
            "join comptages.category as cat on cc.id_category = cat.id "
            "join comptages.class as cl on cl.id = cc.id_class "
            "where cl.name = '{}'".format(class_name))

        query.exec_(query_str)

        catbins = []
        while query.next():
            catbins.append(query.value(0))

        return catbins

    def get_aggregate_speed_chart_data(
            self, count_id, status):

        self.init_db_connection()
        query = QSqlQuery(self.db)

        query_str = (
            "select sum(spd.value), spd.low, spd.high from "
            "comptages.count_aggregate as agg "
            "join comptages.count_aggregate_value_spd as spd "
            "on	agg.id = spd.id_count_aggregate "
            "where agg.id_count = {} and agg.type = 'SPD' "
            "and agg.import_status = {} "
            "group by spd.low, spd.high "
            "order by spd.low;".format(count_id, status))

        query.exec_(query_str)
        x = []
        y = []
        while query.next():
            x.append("{}-{} km/h".format(
                str(query.value(1)),
                str(query.value(2))))
            y.append(query.value(0))

        return x, y

    def get_aggregate_category_chart_data(self, count_id, status):
        self.init_db_connection()
        query = QSqlQuery(self.db)

        query_str = (
            "select sum(cls.value), cat.code, cat.name from "
            "comptages.count_aggregate as agg "
            "join comptages.count_aggregate_value_cls as cls "
            "on agg.id = cls.id_count_aggregate "
            "join comptages.category as cat "
            "on cls.id_category = cat.id "
            "where agg.id_count = {} and agg.type = 'CLS' "
            "and agg.import_status = {} "
            "group by cat.code, cat.name "
            "order by cat.code;".format(count_id, status))

        query.exec_(query_str)
        labels = []
        values = []
        while query.next():
            labels.append("{} ({})".format(
                str(query.value(2)),
                str(query.value(1))))
            values.append(query.value(0))

        return labels, values

    def get_days_of_aggregate_dataset(self, count_id, status):
        self.init_db_connection()
        query = QSqlQuery(self.db)

        query_str = (
            "select distinct date_trunc('day', start) as day from "
            "comptages.count_aggregate where id_count = {} "
            "and import_status = {} "
            "order by day;".format(count_id, status))

        query.exec_(query_str)
        days = []
        while query.next():
            days.append(query.value(0).toString('yyyy-MM-dd hh:mm:ss'))

        return days

    def get_aggregate_time_chart_data(
            self, count_id, status, lane_or_direction):

        xs = []
        ys = []

        days = self.get_days_of_aggregate_dataset(count_id, status)
        for day in days:
            x, y = self.get_aggregate_time_chart_data_day(
                count_id, day, status, lane_or_direction)
            xs.append(x)
            ys.append(y)
        return xs, ys, days

    def get_aggregate_time_chart_data_day(
            self, count_id, day, status, lane_or_direction):
        self.init_db_connection()
        query = QSqlQuery(self.db)

        # TODO verify if lane or direction
        lane_or_direction_str = "and agg.id_lane = {}".format(
            lane_or_direction)

        query_str = (
            "select date_part('hour', agg.start), "
            "date_part('hour', agg.end), sum(cls.value) from "
            "comptages.count_aggregate as agg "
            "join comptages.count_aggregate_value_cls as cls "
            "on agg.id = cls.id_count_aggregate "
            "where agg.id_count = {} and agg.type = 'CLS' "
            " {} "
            "and date_trunc('day', agg.start) = '{}' "
            "and agg.import_status = {} "
            "group by agg.start, agg.end "
            "order by agg.start".format(
                count_id, lane_or_direction_str, day, status)
        )
        print(query_str)
        query.exec_(query_str)

        x = ["00h-01h", "01h-02h", "02h-03h", "03h-04h", "04h-05h", "05h-06h",
             "06h-07h", "07h-08h", "08h-09h", "09h-10h", "10h-11h", "11h-12h",
             "12h-13h", "13h-14h", "14h-15h", "15h-16h", "16h-17h", "17h-18h",
             "18h-19h", "19h-20h", "20h-21h", "21h-22h", "22h-23h", "23h-00h"]
        y = [None]*24

        while query.next():
            y[int(query.value(0))] = query.value(2)

        return x, y

    def get_detail_category_chart_data(self, count_id, status):
        self.init_db_connection()
        query = QSqlQuery(self.db)

        query_str = (
            "select cat.code, cat.name, count(det.id_category) from "
            "comptages.count_detail as det "
            "join comptages.category as cat "
            "on det.id_category = cat.id "
            "where det.id_count = {} "
            "and det.import_status = {} "
            "group by det.id_category, cat.code, cat.name "
            "order by cat.code;".format(count_id, status))

        query.exec_(query_str)
        labels = []
        values = []
        while query.next():
            labels.append("{} ({})".format(
                str(query.value(1)),
                str(query.value(0))))
            values.append(query.value(2))

        return labels, values

    def get_detail_speed_chart_data(self, count_id, status):

        self.init_db_connection()
        query = QSqlQuery(self.db)

        query_str = (
            "select * from ("
            "select 0 as low, 10, count(*) from "
            "comptages.count_detail where id_count = {0} and speed "
            "between 0 and 10 and import_status = {1} union "
            "select 10, 20, count(*) from "
            "comptages.count_detail where id_count = {0} and speed "
            "between 10 and 20 and import_status = {1} union "
            "select 20, 30, count(*) from "
            "comptages.count_detail where id_count = {0} and speed "
            "between 20 and 30 and import_status = {1} union "
            "select 30, 40, count(*) from "
            "comptages.count_detail where id_count = {0} and speed "
            "between 30 and 40 and import_status = {1} union "
            "select 40, 50, count(*) from "
            "comptages.count_detail where id_count = {0} and speed "
            "between 40 and 50 and import_status = {1} union "
            "select 50, 60, count(*) from "
            "comptages.count_detail where id_count = {0} and speed "
            "between 50 and 60 and import_status = {1} union "
            "select 60, 70, count(*) from "
            "comptages.count_detail where id_count = {0} and speed "
            "between 60 and 70 and import_status = {1} union "
            "select 70, 80, count(*) from "
            "comptages.count_detail where id_count = {0} and speed "
            "between 70 and 80 and import_status = {1} union "
            "select 80, 90, count(*) from "
            "comptages.count_detail where id_count = {0} and speed "
            "between 80 and 90 and import_status = {1} union "
            "select 90, 100, count(*) from "
            "comptages.count_detail where id_count = {0} and speed "
            "between 90 and 100 and import_status = {1} union "
            "select 100, 110, count(*) from "
            "comptages.count_detail where id_count = {0} and speed "
            "between 100 and 110 and import_status = {1} union "
            "select 110, 120, count(*) from "
            "comptages.count_detail where id_count = {0} and speed "
            "between 110 and 120 and import_status = {1} union "
            "select 120, 999, count(*) from "
            "comptages.count_detail where id_count = {0} and speed "
            "between 120 and 999 and import_status = {1}"
            ") as foo order by low".format(count_id, status))

        query.exec_(query_str)
        x = []
        y = []
        while query.next():
            x.append("{}-{} km/h".format(
                str(query.value(0)),
                str(query.value(1))))
            y.append(query.value(2))

        return x, y

    def get_days_of_detail_dataset(self, count_id):
        self.init_db_connection()
        query = QSqlQuery(self.db)

        query_str = (
            "select distinct date_trunc('day', timestamp) as day "
            "from comptages.count_detail where id_count = {} "
            "order by day;".format(count_id))

        query.exec_(query_str)
        days = []
        while query.next():
            days.append(query.value(0).toString('yyyy-MM-dd hh:mm:ss'))

        return days

    def get_detail_time_chart_data(self, count_id, status):

        xs = []
        ys = []

        days = self.get_days_of_detail_dataset(count_id)
        for day in days:
            x, y = self.get_detail_time_chart_data_day(count_id, day, status)
            xs.append(x)
            ys.append(y)
        return xs, ys, days

    def get_detail_time_chart_data_day(self, count_id, day, status):
        self.init_db_connection()
        query = QSqlQuery(self.db)

        query_str = (
            "select date_part('hour', timestamp), "
            "date_part('hour', timestamp) + 1, "
            "count(date_part('hour', timestamp)) "
            "from comptages.count_detail "
            "where id_count = {} and "
            "date_trunc('day', timestamp) = '{}' "
            "and import_status = {} "
            "group by date_part('hour', timestamp);".format(
                count_id, day, status)
        )

        query.exec_(query_str)

        x = ["00h-01h", "01h-02h", "02h-03h", "03h-04h", "04h-05h", "05h-06h",
             "06h-07h", "07h-08h", "08h-09h", "09h-10h", "10h-11h", "11h-12h",
             "12h-13h", "13h-14h", "14h-15h", "15h-16h", "16h-17h", "17h-18h",
             "18h-19h", "19h-20h", "20h-21h", "21h-22h", "22h-23h", "23h-00h"]
        y = [None]*24

        while query.next():
            y[int(query.value(0))] = query.value(2)

        return x, y

    def is_data_aggregate(self, count_id):
        self.init_db_connection()
        query = QSqlQuery(self.db)

        query_str = (
            "select id from comptages.count_aggregate "
            "where id_count = {}".format(count_id))

        query.exec_(query_str)
        if query.next():
            return True
        return False

    def is_data_detail(self, count_id):
        self.init_db_connection()
        query = QSqlQuery(self.db)

        query_str = (
            "select id from comptages.count_detail "
            "where id_count = {}".format(count_id))

        query.exec_(query_str)
        if query.next():
            return True
        return False

    def guess_count_id(self, site, start_rec, stop_rec):
        """Try to identify the count related to an imported file"""

        self.init_db_connection()
        query = QSqlQuery(self.db)

        query_str = (
            "select cou.id from comptages.installation as ins "
            "join comptages.count as cou on ins.id = cou.id_installation "
            "where ins.name = '{}' and ins.active = true "
            "and cou.start_service_date <= '{}' "
            "and cou.end_service_date >= '{}';".format(
                site, start_rec, stop_rec))

        query.exec_(query_str)
        if query.next():
            return query.value(0)
        return None

    def get_quarantined_counts(self):
        self.init_db_connection()
        query = QSqlQuery(self.db)

        query_str = (
            "select distinct(agg.id_count) from "
            "comptages.count_aggregate as agg where agg.import_status = {0} "
            "union select distinct(det.id_count) from comptages.count_detail "
            "as det where det.import_status = {0};".format(
                self.IMPORT_STATUS_QUARANTINE))

        result = []
        query.exec_(query_str)
        while query.next():
            result.append(query.value(0))
        return result

    def select_and_zoom_on_section_of_count(self, count_id):
        sections = self.get_sections_of_count(count_id)
        layer = self.layers['section']
        layer.selectByIds([x.id() for x in sections])
        iface.setActiveLayer(layer)
        iface.actionZoomToSelected().trigger()

    def change_status_of_count_data(self, count_id, new_status):
        self.init_db_connection()
        query = QSqlQuery(self.db)

        query_strs = []

        query_strs.append(
            "update comptages.count_aggregate set import_status = {} "
            "where id_count = {}".format(new_status, count_id))

        query_strs.append(
            "update comptages.count_detail set import_status = {} "
            "where id_count = {}".format(new_status, count_id))

        for _ in query_strs:
            query.exec_(_)

        push_info("Les données ont été importées")

    def delete_count_data(self, count_id):
        self.init_db_connection()
        query = QSqlQuery(self.db)

        query_strs = []

        query_strs.append(
            "delete from comptages.count_aggregate where id_count = "
            "{}".format(count_id))

        query_strs.append(
            "delete from comptages.count_detail where id_count = "
            "{}".format(count_id))

        for _ in query_strs:
            query.exec_(_)

        push_info("Les données ont été supprimées")

    def get_predefined_config_from_count(self, count_id):
        count = self.get_count(count_id)
        model = self.get_model(count.attribute('id_model'))

        return model.attribute('configuration')

    def get_model(self, model_id):
        request = QgsFeatureRequest().setFilterExpression(
            '"id" = {}'.format(model_id))

        return next(self.layers['model'].getFeatures(request))

    def get_class_name_of_count(self, count_id):
        count = self.get_count(count_id)
        clazz = self.get_class(count.attribute('id_class'))

        return clazz.attribute('name')

    def get_class(self, class_id):
        request = QgsFeatureRequest().setFilterExpression(
            '"id" = {}'.format(class_id))

        return next(self.layers['class'].getFeatures(request))

    def get_lanes_of_count(self, count_id):

        return self.get_lanes_of_installation(
            self.get_installation_of_count(count_id).attribute('id'))
