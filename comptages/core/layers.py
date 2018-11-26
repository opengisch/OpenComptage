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

    def __init__(self):
        QObject.__init__(self)
        self.layers = {}

        self.highlighted_sections = []
        self.db = None

    def load_layers(self):

        group_comptages = QgsProject.instance().layerTreeRoot().findGroup(
            'Comptages')

        if group_comptages is None:
            group_comptages = QgsProject.instance().layerTreeRoot().addGroup(
                'Comptages')

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

                self.layers[key] = layer

                print("loaded_layer: {}".format(layer_definition['display_name']))

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
            'Export configuration',
            ("from qgis.utils import plugins\n"
             "plugins['comptages'].do_export_configuration_action([% $id %])")
        )
        action.setActionScopes(['Feature'])
        action_manager.addAction(action)

        action = QgsAction(
            QgsAction.GenericPython,
            'Import data',
            ("from qgis.utils import plugins\n"
             "plugins['comptages'].do_import_data_action([% $id %])")
        )
        action.setActionScopes(['Feature'])
        action_manager.addAction(action)

        action = QgsAction(
            QgsAction.GenericPython,
            'Create report',
            ("from qgis.utils import plugins\n"
             "plugins['comptages'].do_generate_report_action([% $id %])")
        )
        action.setActionScopes(['Feature'])
        action_manager.addAction(action)

        action = QgsAction(
            QgsAction.GenericPython,
            'Export plan',
            ("from qgis.utils import plugins\n"
             "plugins['comptages'].do_export_plan_action([% $id %])")
        )
        action.setActionScopes(['Feature'])
        action_manager.addAction(action)

        action = QgsAction(
            QgsAction.GenericPython,
            'Generate chart',
            ("from qgis.utils import plugins\n"
             "plugins['comptages'].do_generate_chart_action([% $id %])")
        )
        action.setActionScopes(['Feature'])
        action_manager.addAction(action)

    def create_count(self):

        layer = self.layers['section']

        selected_count = layer.selectedFeatureCount()
        if selected_count == 0:
            push_info("Please select a section")
            return
        elif selected_count > 1:
            push_info("Please select only one section")
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
            push_info("Please select a section")
            return
        elif selected_count > 1:
            push_info("Please select only one section")
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
        settings = Settings()

        db = QSqlDatabase.addDatabase("QPSQL")
        db.setHostName(settings.value("db_host"))
        db.setPort(settings.value("db_port"))
        db.setDatabaseName(settings.value("db_name"))
        db.setUserName(settings.value("db_username"))
        db.setPassword(settings.value("db_password"))
        db.open()

        query = QSqlQuery(db)

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
        print(query_str)
        query.exec_(query_str)

        while query.next():
            self.highlighted_sections.append(str(query.value(0)).strip())

        db.close()

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
        """Return the installation of a count"""

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
                     "file_name, "
                     "id_lane, id_count, id_category) values ("
                     "{}, '{}', {}, {}, {}, {}, '{}', '{}', {}, {}, "
                     "{})".format(
                         row['numbering'],
                         row['timestamp'],
                         row['distance_front_front'],
                         row['distance_front_back'],
                         row['speed'],
                         row['length'],
                         row['height'],
                         file_name,
                         row['channel'],
                         count_id,
                         row['category_id']))

        query.exec_(query_str)

    def insert_count_aggregate_row(self, row, row_type, count_id, file_name,
                                   bins):
        self.init_db_connection()
        query = QSqlQuery(self.db)

        query_str = ("insert into comptages.count_aggregate ("
                     "type, \"start\", \"end\", file_name, id_count, id_lane) "
                     "values ("
                     "'{}', '{}', '{}', '{}', {}, {})".format(
                         row_type,
                         row['start'],
                         row['end'],
                         file_name,
                         count_id,
                         row['channel']))

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
            pass
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

        for i in range(1, catbins+1):
            data = row['data_{}'.format(i)]
            if not data == '':
                category = i
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

        print(query_str)
        query.exec_(query_str)

        catbins = []
        while query.next():
            catbins.append(query.value(0))

        return catbins
