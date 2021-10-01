import os

from qgis.PyQt.QtCore import QObject, QVariant
from qgis.PyQt.QtSql import QSqlDatabase, QSqlQuery
from qgis.core import (
    QgsProject, QgsEditorWidgetSetup, QgsVectorLayer,
    QgsCoordinateReferenceSystem, QgsDataSourceUri,
    QgsAction, QgsFeatureRequest, QgsExpressionContextUtils,
    QgsField, QgsVectorLayerJoinInfo)
from qgis.utils import iface

from comptages.core.definitions import LAYER_DEFINITIONS
from comptages.core.settings import Settings
from comptages.core.utils import push_info, connect_to_db


class Layers(QObject):
    IMPORT_STATUS_QUARANTINE = 1
    IMPORT_STATUS_DEFINITIVE = 0

    def __init__(self):
        QObject.__init__(self)
        self.layers = {}

        self.highlighted_sections = []
        self.db = None
        self.lanes_cache = dict()

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
        self.create_virtual_fields()
        self.create_joins()
        self.create_relations()
        iface.setActiveLayer(self.layers['section'])

        self.populate_list_of_highlighted_sections()

        self.layers['count'].featureAdded.connect(self.on_count_added)

        from qgis.core import QgsExpressionContextUtils
        QgsExpressionContextUtils.setProjectVariable(
            QgsProject.instance(), 'highlighted_installation', '')

    def apply_qml_styles(self):
        for key in LAYER_DEFINITIONS:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            qml_file_path = os.path.join(
                current_dir, os.pardir, 'qml', '{}.qml'.format(key))
            self.layers[key].loadNamedStyle(qml_file_path)

    def create_virtual_fields(self):
        # TJM
        field = QgsField( 'tjm', QVariant.LongLong )
        self.layers['tjm'].addExpressionField( 'mean( "value", group_by:="count_id")', field )

    def create_joins(self):
        # Join TJM (total virtual field) in count table
        join = QgsVectorLayerJoinInfo()
        join.setJoinLayer(self.layers['tjm'])
        join.setJoinFieldName('count_id')
        join.setTargetFieldName('id')
        join.setUsingMemoryCache(False)
        join.setJoinFieldNamesSubset(['tjm'])
        join.setPrefix('')
        self.layers['count'].addJoin(join)

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
                'AllowNull':        True,
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
                # """
                # CASE WHEN current_value('id_sensor_type') = 1 THEN \"id\" IN ('1', '2', '4', '6', '7')
                # WHEN current_value('id_sensor_type') = 2 THEN \"id\" IN ('1', '3', '5')
                # WHEN current_value('id_sensor_type') = 3 THEN \"id\" IN ('12')
                # ELSE \"id\"
                # END""",
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
             "plugins['comptages'].do_export_configuration_action([% attribute( $currentfeature, 'id' ) %])")
        )
        action.setActionScopes(['Feature'])
        action_manager.addAction(action)

        action = QgsAction(
            QgsAction.GenericPython,
            'Importation',
            ("from qgis.utils import plugins\n"
             "plugins['comptages'].do_import_single_file_action([% attribute( $currentfeature, 'id' ) %])")
        )
        action.setActionScopes(['Feature'])
        action_manager.addAction(action)

        action = QgsAction(
            QgsAction.GenericPython,
            'Creer un rapport',
            ("from qgis.utils import plugins\n"
             "plugins['comptages'].do_generate_report_action([% attribute( $currentfeature, 'id' ) %])")
        )
        action.setActionScopes(['Feature'])
        action_manager.addAction(action)

        action = QgsAction(
            QgsAction.GenericPython,
            'Creer un plan',
            ("from qgis.utils import plugins\n"
             "plugins['comptages'].do_export_plan_action([% attribute( $currentfeature, 'id' ) %])")
        )
        action.setActionScopes(['Feature'])
        action_manager.addAction(action)

        action = QgsAction(
            QgsAction.GenericPython,
            'Générer les graphiques',
            ("from qgis.utils import plugins\n"
             "plugins['comptages'].do_generate_chart_action([% attribute( $currentfeature, 'id' ) %])")
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

    def get_counts_of_section_by_year(self, section_id, year):
        """Return a list of all count features related with the passed
        section for the passed year"""

        try:
            lanes = self.get_lanes_of_section(section_id)
            installation = self.get_installation_of_lane(
                next(lanes).attribute('id'))
            counts = self.get_counts_of_installation(
                installation.attribute('id'))
        except StopIteration:
            return []

        print(counts)
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

        request = QgsFeatureRequest().setFilterExpression(
            '"id_installation" = {}'.format(installation_id)
        )

        return self.layers['count'].getFeatures(request)

    def is_section_highlighted(self, section_id):
        """Return if the passed section has related counts with the current
        filter settings"""

        if section_id in self.highlighted_sections:
            return True
        return False

    def populate_list_of_highlighted_sections(
            self, start_date=None, end_date=None, permanent=None,
            sensor_type_id=None, tjm=None, axe=None):
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
        if sensor_type_id:
            wheres.append("c.id_sensor_type = {}".format(sensor_type_id))
        if tjm:
            if tjm[1] >= 30000:
                wheres.append("t.value >= {}".format(tjm[0]))
            else:
                wheres.append("t.value between {} and {}".format(tjm[0], tjm[1]))
        if axe:
            wheres.append("s.owner = '{}' and s.road = '{}'".format(axe[0], axe[1]))

        where_str = ''
        if wheres:
            where_str = "where " + " and ".join(wheres)

        query_str = ("select distinct l.id_section from comptages.lane as l "
                     "inner join comptages.installation as i on "
                     "(l.id_installation = i.id) inner join "
                     "comptages.count as c on (i.id = c.id_installation) "
                     "left join comptages.tjm as t on "
                     "(l.id = t.lane_id) "
                     "inner join comptages.section as s on"
                     "(l.id_section = s.id) "
                     "{};".format(where_str))
        query.exec_(query_str)

        while query.next():
            self.highlighted_sections.append(str(query.value(0)).strip())

    def apply_filter(
            self, start_date, end_date, installation_choice, sensor_choice, tjm, axe):
        if installation_choice == 0:
            permanent = None
        elif installation_choice == 1:
            permanent = True
        elif installation_choice == 2:
            permanent = False

        if sensor_choice == 0:
            sensor_type_id = None
        elif sensor_choice == 1:
            sensor_type_id = self.get_sensor_type_id('Boucle')
        elif sensor_choice == 2:
            sensor_type_id = self.get_sensor_type_id('Tube')

        self.populate_list_of_highlighted_sections(
            start_date, end_date, permanent, sensor_type_id, tjm, axe)
        self.layers['section'].triggerRepaint()

    def is_connected(self):
        """Return if the plugin is connected to the database"""
        if self.db is None:
            return False
        return True

    def init_db_connection(self):
        if self.db is None:
            self.db = connect_to_db()

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

    def get_section_ids_of_count(self, count_id):
        """Return the section ids related to a count"""

        count = self.get_count(count_id)
        installation_id = count.attribute('id_installation')

        lanes = self.get_lanes_of_installation(installation_id)

        # Get only distinct section ids
        section_ids = set()
        for lane in lanes:
            section_ids.add(lane.attribute('id_section'))

        return list(section_ids)

    def get_sections_with_data_of_count(self, count_id, status):

        self.init_db_connection()
        query = QSqlQuery(self.db)

        query_str = (
            "select distinct(lan.id_section) from comptages.count_aggregate "
            "as cou "
            "join comptages.lane as lan "
            "on lan.id = cou.id_lane "
            "where cou.id_count = {0} "
            "and import_status = {1} "
            "union "
            "select distinct(lan.id_section) from comptages.count_detail "
            "as cou "
            "join comptages.lane as lan "
            "on lan.id = cou.id_lane "
            "where cou.id_count = {0} "
            "and import_status = {1} ".format(count_id, status))

        result = []
        query.exec_(query_str)
        while query.next():
            result.append(query.value(0))
        return result

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

    def get_aggregate_speed_chart_data(
            self, count_id, status, section_id):

        self.init_db_connection()
        query = QSqlQuery(self.db)

        query_str = (
            "select sum(spd.value), spd.low, spd.high from "
            "comptages.count_aggregate as agg "
            "join comptages.count_aggregate_value_spd as spd "
            "on	agg.id = spd.id_count_aggregate "
            "join comptages.lane as lan "
            "on agg.id_lane = lan.id "
            "where agg.id_count = {} and agg.type = 'SPD' "
            "and agg.import_status = {} "
            "and lan.id_section = '{}'"
            "group by spd.low, spd.high "
            "order by spd.low;".format(count_id, status, section_id))

        query.exec_(query_str)
        x = []
        y = []
        while query.next():
            x.append("{}-{} km/h".format(
                str(query.value(1)),
                str(query.value(2))))
            y.append(query.value(0))

        return x, y

    def get_aggregate_category_chart_data(self, count_id, status, section_id):
        self.init_db_connection()
        query = QSqlQuery(self.db)

        query_str = (
            "select sum(cls.value), cat.code, cat.name from "
            "comptages.count_aggregate as agg "
            "join comptages.count_aggregate_value_cls as cls "
            "on agg.id = cls.id_count_aggregate "
            "join comptages.category as cat "
            "on cls.id_category = cat.id "
            "join comptages.lane as lan "
            "on agg.id_lane = lan.id "
            "where agg.id_count = {} and agg.type = 'CLS' "
            "and agg.import_status = {} "
            "and lan.id_section = '{}' "
            "group by cat.code, cat.name "
            "order by cat.code;".format(count_id, status, section_id))

        query.exec_(query_str)
        labels = []
        values = []
        while query.next():
            labels.append("{} ({})".format(
                str(query.value(2)),
                str(query.value(1))))
            values.append(query.value(0))

        return labels, values

    def get_aggregate_total(self, count_id, status, section_id):
        self.init_db_connection()
        query = QSqlQuery(self.db)

        query_str = (
            "select sum(spd.value) from "
            "comptages.count_aggregate as agg "
            "join comptages.count_aggregate_value_spd as spd "
            "on agg.id = spd.id_count_aggregate "
            "join comptages.lane as lan "
            "on agg.id_lane = lan.id "
            "where agg.id_count = {} and agg.type = 'SPD' "
            "and agg.import_status = {} "
            "and lan.id_section = '{}';".format(count_id, status, section_id))

        query.exec_(query_str)

        if query.next():
            return query.value(0)
        return None

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

    def get_aggregate_time_chart_data_by_lane(
            self, count_id, status, lane, section_id):

        xs = []
        ys = []

        days = self.get_days_of_aggregate_dataset(count_id, status)

        # Get info from one of the table depending on which one contains data
        types = self.get_type_of_aggregate_count(count_id, status)
        value_type = ''
        if 'CLS' in types:
            value_type = 'CLS'
        elif 'SPD' in types:
            value_type = 'SPD'
        elif 'DRN' in types:
            value_type = 'DRN'
        elif 'CNT' in types:
            value_type = 'CNT'
        elif 'LEN' in types:
            value_type = 'LEN'

        if value_type == '':
            return xs, ys, days

        for day in days:
            x, y = self.get_aggregate_time_chart_data_day_by_lane(
                count_id, day, status, lane, section_id, value_type)
            xs.append(x)
            ys.append(y)
        return xs, ys, days

    def get_aggregate_time_chart_data_day_by_lane(
            self, count_id, day, status, lane, section_id, value_type):
        self.init_db_connection()
        query = QSqlQuery(self.db)

        query_str = (
            "select date_part('hour', agg.start), "
            "date_part('hour', agg.end), sum(cls.value) from "
            "comptages.count_aggregate as agg "
            "join comptages.count_aggregate_value_{5} as cls "
            "on agg.id = cls.id_count_aggregate "
            "join comptages.lane as lan "
            "on agg.id_lane = lan.id "
            "where agg.id_count = {0} and agg.type = '{5}' "
            "and agg.id_lane = {1} "
            "and date_trunc('day', agg.start) = '{2}' "
            "and agg.import_status = {3} "
            "and lan.id_section = '{4}' "
            "group by agg.start, agg.end "
            "order by agg.start".format(
                count_id, lane, day, status, section_id, value_type)
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

    def get_aggregate_time_chart_data_by_direction(
            self, count_id, status, direction, section_id):

        xs = []
        ys = []

        days = self.get_days_of_aggregate_dataset(count_id, status)

        # Get info from one of the table depending on which one contains data
        types = self.get_type_of_aggregate_count(count_id, status)
        value_type = ''
        if 'CLS' in types:
            value_type = 'CLS'
        elif 'SPD' in types:
            value_type = 'SPD'
        elif 'DRN' in types:
            value_type = 'DRN'
        elif 'CNT' in types:
            value_type = 'CNT'
        elif 'LEN' in types:
            value_type = 'LEN'

        if value_type == '':
            return xs, ys, days

        for day in days:
            x, y = self.get_aggregate_time_chart_data_day_by_direction(
                count_id, day, status, direction, section_id, value_type)
            xs.append(x)
            ys.append(y)
        return xs, ys, days

    def get_aggregate_time_chart_data_day_by_direction(
            self, count_id, day, status, direction, section_id, value_type):
        self.init_db_connection()
        query = QSqlQuery(self.db)

        query_str = (
            "select date_part('hour', agg.start), "
            "date_part('hour', agg.end), sum(cls.value) from "
            "comptages.count_aggregate as agg "
            "join comptages.count_aggregate_value_{5} as cls "
            "on agg.id = cls.id_count_aggregate "
            "join comptages.lane as lan on "
            "agg.id_lane = lan.id "
            "where agg.id_count = {0} and agg.type = '{5}' "
            "and lan.direction = {1} "
            "and date_trunc('day', agg.start) = '{2}' "
            "and agg.import_status = {3} "
            "and lan.id_section = '{4}' "
            "group by agg.start, agg.end, lan.direction "
            "order by agg.start".format(
                count_id, direction, day, status, section_id, value_type)
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

    def get_detail_category_chart_data(self, count_id, status, section_id):
        self.init_db_connection()
        query = QSqlQuery(self.db)

        query_str = (
            "select cat.code, cat.name, count(det.id_category) from "
            "comptages.count_detail as det "
            "join comptages.category as cat "
            "on det.id_category = cat.id "
            "join comptages.lane as lan "
            "on det.id_lane = lan.id "
            "where det.id_count = {} "
            "and det.import_status = {} "
            "and lan.id_section = '{}' "
            "group by det.id_category, cat.code, cat.name "
            "order by cat.code;".format(count_id, status, section_id))

        query.exec_(query_str)
        labels = []
        values = []
        while query.next():
            labels.append("{} ({})".format(
                str(query.value(1)),
                str(query.value(0))))
            values.append(query.value(2))

        return labels, values

    def get_detail_speed_chart_data(self, count_id, status, section_id):

        self.init_db_connection()
        query = QSqlQuery(self.db)

        query_str = (
            "select * from ("

            "select 0 as low, 10, count(*) from "
            "comptages.count_detail "
            "join comptages.lane as lan "
            "on id_lane = lan.id where lan.id_section = '{2}' "
            "and id_count = {0} and speed "
            "between 0 and 9 and import_status = {1} union "

            "select 10, 20, count(*) from "
            "comptages.count_detail "
            "join comptages.lane as lan "
            "on id_lane = lan.id where lan.id_section = '{2}' "
            "and id_count = {0} and speed "
            "between 10 and 19 and import_status = {1} union "

            "select 20, 30, count(*) from "
            "comptages.count_detail "
            "join comptages.lane as lan "
            "on id_lane = lan.id where lan.id_section = '{2}' "
            "and id_count = {0} and speed "
            "between 20 and 29 and import_status = {1} union "

            "select 30, 40, count(*) from "
            "comptages.count_detail "
            "join comptages.lane as lan "
            "on id_lane = lan.id where lan.id_section = '{2}' "
            "and id_count = {0} and speed "
            "between 30 and 39 and import_status = {1} union "

            "select 40, 50, count(*) from "
            "comptages.count_detail "
            "join comptages.lane as lan "
            "on id_lane = lan.id where lan.id_section = '{2}' "
            "and id_count = {0} and speed "
            "between 40 and 49 and import_status = {1} union "

            "select 50, 60, count(*) from "
            "comptages.count_detail "
            "join comptages.lane as lan "
            "on id_lane = lan.id where lan.id_section = '{2}' "
            "and id_count = {0} and speed "
            "between 50 and 59 and import_status = {1} union "

            "select 60, 70, count(*) from "
            "comptages.count_detail "
            "join comptages.lane as lan "
            "on id_lane = lan.id where lan.id_section = '{2}' "
            "and id_count = {0} and speed "
            "between 60 and 69 and import_status = {1} union "

            "select 70, 80, count(*) from "
            "comptages.count_detail "
            "join comptages.lane as lan "
            "on id_lane = lan.id where lan.id_section = '{2}' "
            "and id_count = {0} and speed "
            "between 70 and 79 and import_status = {1} union "

            "select 80, 90, count(*) from "
            "comptages.count_detail "
            "join comptages.lane as lan "
            "on id_lane = lan.id where lan.id_section = '{2}' "
            "and id_count = {0} and speed "
            "between 80 and 89 and import_status = {1} union "

            "select 90, 100, count(*) from "
            "comptages.count_detail "
            "join comptages.lane as lan "
            "on id_lane = lan.id where lan.id_section = '{2}' "
            "and id_count = {0} and speed "
            "between 90 and 99 and import_status = {1} union "

            "select 100, 110, count(*) from "
            "comptages.count_detail "
            "join comptages.lane as lan "
            "on id_lane = lan.id where lan.id_section = '{2}' "
            "and id_count = {0} and speed "
            "between 100 and 109 and import_status = {1} union "

            "select 110, 120, count(*) from "
            "comptages.count_detail "
            "join comptages.lane as lan "
            "on id_lane = lan.id where lan.id_section = '{2}' "
            "and id_count = {0} and speed "
            "between 110 and 119 and import_status = {1} union "

            "select 120, 999, count(*) from "
            "comptages.count_detail "
            "join comptages.lane as lan "
            "on id_lane = lan.id where lan.id_section = '{2}' "
            "and id_count = {0} and speed "
            "between 120 and 999 and import_status = {1}"

            ") as foo order by low".format(count_id, status, section_id))

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
            "select distinct date_trunc('day', timestamp at time zone 'Europe/Zurich') as day "
            "from comptages.count_detail where id_count = {} "
            "order by day;".format(count_id))

        query.exec_(query_str)
        days = []
        while query.next():
            days.append(query.value(0).toString('yyyy-MM-dd hh:mm:ss'))

        return days

    def get_detail_time_chart_data_by_lane(
            self, count_id, status, lane, section_id):

        xs = []
        ys = []

        days = self.get_days_of_detail_dataset(count_id)
        for day in days:
            x, y = self.get_detail_time_chart_data_day_by_lane(
                count_id, day, status, lane, section_id)
            xs.append(x)
            ys.append(y)
        return xs, ys, days

    def get_detail_time_chart_data_day_by_lane(
            self, count_id, day, status, lane, section_id):
        self.init_db_connection()
        query = QSqlQuery(self.db)

        query_str = (
            "select date_part('hour', timestamp), "
            "date_part('hour', timestamp) + 1, "
            "count(date_part('hour', timestamp)) "
            "from comptages.count_detail "
            "join comptages.lane as lan "
            "on id_lane = lan.id "
            "where id_count = {} and "
            "date_trunc('day', timestamp) = '{}' "
            "and import_status = {} "
            "and id_lane = {} "
            "and lan.id_section = '{}' "
            "group by date_part('hour', timestamp);".format(
                count_id, day, status, lane, section_id)
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

    def get_detail_time_chart_data_by_direction(
            self, count_id, status, direction, section_id):

        xs = []
        ys = []

        days = self.get_days_of_detail_dataset(count_id)
        for day in days:
            x, y = self.get_detail_time_chart_data_day_by_direction(
                count_id, day, status, direction, section_id)
            xs.append(x)
            ys.append(y)
        return xs, ys, days

    def get_detail_time_chart_data_day_by_direction(
            self, count_id, day, status, direction, section_id):
        self.init_db_connection()
        query = QSqlQuery(self.db)

        query_str = (
            "select date_part('hour', timestamp), "
            "date_part('hour', timestamp) + 1, "
            "count(date_part('hour', timestamp)) "
            "from comptages.count_detail as cou "
            "join comptages.lane as lan on "
            "cou.id_lane = lan.id "
            "where id_count = {} and "
            "date_trunc('day', timestamp) = '{}' "
            "and import_status = {} "
            "and lan.direction = {} "
            "and lan.id_section = '{}' "
            "group by date_part('hour', timestamp);".format(
                count_id, day, status, direction, section_id)
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

    def change_status_of_count_data(self, count_id, section_id, new_status):
        self.init_db_connection()
        query = QSqlQuery(self.db)

        query_strs = []

        query_strs.append(
            "update comptages.count_aggregate as cou set import_status = {} "
            "from comptages.lane as lan "
            "where cou.id_lane = lan.id "
            "and id_count = {} "
            "and lan.id_section = '{}'".format(
                new_status, count_id, section_id))

        query_strs.append(
            "update comptages.count_detail as cou set import_status = {} "
            "from comptages.lane as lan "
            "where cou.id_lane = lan.id "
            "and id_count = {} "
            "and lan.id_section = '{}'".format(
                new_status, count_id, section_id))

        for _ in query_strs:
            query.exec_(_)

        push_info("Les données ont été importées")

    def delete_count_data(self, count_id, section_id, status):
        self.init_db_connection()
        query = QSqlQuery(self.db)

        query_strs = []

        query_strs.append(
            "delete from comptages.count_aggregate as cou "
            "using comptages.lane as lan "
            "where cou.id_lane = lan.id "
            "and cou.id_count = {} "
            "and cou.import_status = {} "
            "and lan.id_section = '{}' ".format(
                count_id, status, section_id))

        query_strs.append(
            "delete from comptages.count_detail as cou "
            "using comptages.lane as lan "
            "where cou.id_lane = lan.id "
            "and cou.id_count = {} "
            "and cou.import_status = {} "
            "and lan.id_section = '{}' ".format(
                count_id, status, section_id))

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

    def get_lanes_dict(self, count_id):

        # Cached values
        if count_id in self.lanes_cache:
            return self.lanes_cache[count_id]

        lanes = self.get_lanes_of_count(count_id)

        result = dict()
        for lane in lanes:
            result[lane.attribute('number')] = lane.attribute('id')

        self.lanes_cache[count_id] = result
        return result

    def invalidate_lanes_cache(self):
        """ To be called after an import is finished"""
        self.lanes_cache = dict()

    def get_sensor_type_of_count(self, count_id):
        sensor_type_id = self.get_count(count_id).attribute('id_sensor_type')
        return self.get_sensor_type(sensor_type_id)

    def get_sensor_type(self, sensor_type_id):
        """Return the sensor_type feature"""

        request = QgsFeatureRequest().setFilterExpression(
            '"id" = {}'.format(sensor_type_id)
        )
        return next(self.layers['sensor_type'].getFeatures(request))

    def get_sensor_type_id(self, sensor_type):
        request = QgsFeatureRequest().setFilterExpression(
            '"name" = \'{}\''.format(sensor_type)
        )
        return next(self.layers['sensor_type'].getFeatures(
            request)).attribute('id')

    def get_directions_of_count(self, count_id):
        """Return a list of the directions of a count"""
        self.init_db_connection()
        query = QSqlQuery(self.db)

        query_str = (
            "select lan.direction from comptages.count as cou "
            "join comptages.lane as lan on "
            "cou.id_installation = lan.id_installation "
            "where cou.id = {} group by lan.direction;".format(
                count_id))

        result = []
        query.exec_(query_str)
        while query.next():
            result.append(int(query.value(0)))
        return result

    def write_special_period(
            self, start_date, end_date, description, entity, influence):
        """Insert into special_period only if it is not altready present"""

        self.init_db_connection()
        query = QSqlQuery(self.db)

        query_str = ("INSERT INTO comptages.special_period "
                     "(start_date, end_date, description, entity, influence) "
                     "SELECT '{0}', '{1}', '{2}', '{3}', '{4}' "
                     "WHERE NOT EXISTS ( "
                     "SELECT id FROM comptages.special_period WHERE "
                     "start_date = '{0}' AND end_date = '{1}' AND "
                     "description = '{2}' AND entity = '{3}' AND "
                     "influence = '{4}');".format(
                         start_date,
                         end_date,
                         description,
                         entity,
                         influence))

        query.exec_(query_str)

    def get_special_period(self, special_period_id):
        request = QgsFeatureRequest().setFilterExpression(
            '"id" = {}'.format(special_period_id))

        return next(self.layers['special_period'].getFeatures(request))

    def get_special_period_overlaps(self, start_date, end_date):
        """Return the ids of the special periods thats overlaps the
        passed dates"""

        self.init_db_connection()
        query = QSqlQuery(self.db)

        query_str = (
            "select * from comptages.special_period where "
            "('{0}' >= start_date AND '{0}' < end_date) OR "
            "('{1}' >= start_date AND '{1}' < end_date) OR "
            "('{0}' < start_date AND '{1}' >= end_date); ".format(
                start_date, end_date))

        result = []
        query.exec_(query_str)
        while query.next():
            result.append(int(query.value(0)))
        return result

    def check_dates(self, start_date, end_date):
        """Called from the count's QGIS form, return a string to be
        displayed to the user showing if there is a special period
        during the count dates"""

        special_periods = self.get_special_period_overlaps(
            start_date.toString('yyyy-MM-dd'),
            end_date.toString('yyyy-MM-dd'))

        result = []
        for special_period_id in special_periods:
            special_period = self.get_special_period(special_period_id)
            start = special_period.attribute(
                'start_date').toString('dd.MM.yyyy')
            end = special_period.attribute(
                'end_date').addDays(-1).toString('dd.MM.yyyy')

            if start == end:
                result.append('{} ({})'.format(
                    special_period.attribute('description'),
                    start))
            else:
                result.append('{} ({}-{})'.format(
                    special_period.attribute('description'),
                    start,
                    end))
        return '; '.join(result)

    def count_contains_data(self, count_id):
        self.init_db_connection()
        query = QSqlQuery(self.db)

        query_str = (
            "select id from comptages.count_aggregate where id_count = {0} "
            "and import_status = {1} "
            "union select id from comptages.count_detail where id_count = {0} "
            "and import_status = {1}; ".format(
                count_id, self.IMPORT_STATUS_DEFINITIVE))

        query.exec_(query_str)
        if query.next():
            return True
        return False

    def get_type_of_aggregate_count(self, count_id, import_status):
        self.init_db_connection()
        query = QSqlQuery(self.db)

        query_str = (
            "select distinct(type) from comptages.count_aggregate where "
            "id_count = {} and import_status = {};".format(
                count_id, import_status))

        result = []
        query.exec_(query_str)
        while query.next():
            result.append(query.value(0))
        return result

    def get_characteristic_speeds(
            self, count_id, hour, direction, start_timestamp, end_timestamp,
            section_id):
        self.init_db_connection()
        query = QSqlQuery(self.db)
        result = []

        query_str = (
            "select count(*) from comptages.count_detail as det join "
            "comptages.lane as lan on det.id_lane = lan.id "
            "where det.id_count = {} and lan.direction = {} "
            "and lan.id_section = '{}' "
            "and date_part('hour', det.timestamp) = {} "
            "and det.timestamp>='{}' and det.timestamp<'{}';".format(
                count_id, direction, section_id, hour, start_timestamp,
                end_timestamp))

        query.exec_(query_str)
        if query.next():
            count = query.value(0)
        else:
            return [0, 0, 0, 0]

        percent = []
        percent.append(int(count * 0.15))
        percent.append(int(count * 0.5))
        percent.append(int(count * 0.85))

        for i in percent:
            if i < 0:
                i = 0
            query_str = (
                "select det.speed from comptages.count_detail as det join "
                "comptages.lane as lan on det.id_lane = lan.id "
                "where det.id_count = {} and lan.direction = {} "
                "and lan.id_section = '{}' "
                "and date_part('hour', det.timestamp) = {} "
                "and det.timestamp>='{}' and det.timestamp<'{}' "
                "order by speed "
                "offset ({}-1) rows "
                "fetch next 1 rows only;".format(
                    count_id, direction, section_id, hour, start_timestamp,
                    end_timestamp, i))
            query.exec_(query_str)
            query.next()
            if query.value(0) and query.value(0) >= 1:
                result.append(query.value(0))
            else:
                result.append('NA')

        query_str = (
            "select coalesce(avg(det.speed), 0) from "
            "comptages.count_detail as det join "
            "comptages.lane as lan on det.id_lane = lan.id "
            "where det.id_count = {} and lan.direction = {} "
            "and lan.id_section = '{}' "
            "and date_part('hour', det.timestamp) = {} "
            "and det.timestamp>='{}' and det.timestamp<'{}';".format(
                count_id, direction, section_id, hour, start_timestamp,
                end_timestamp))
        query.exec_(query_str)
        query.next()
        if query.value(0) and query.value(0) >= 1:
            result.append(query.value(0))
        else:
            result.append('NA')

        return result

    def get_formatter_name(self, model_name):
        request = QgsFeatureRequest().setFilterExpression(
            '"name" = \'{}\''.format(model_name)
        )
        return next(self.layers['brand'].getFeatures(
            request)).attribute('formatter_name')

    def get_classes_of_section(self, section_id):
        result = set()
        counts = self.get_counts_of_section(section_id)

        for count in counts:
            result.add(self.get_class_name_of_count(count.attribute('id')))

        return result

    def check_sensor_of_lane(self, lane_id):
        """ Check id a lane is registered in the sensor table"""

        self.init_db_connection()
        query = QSqlQuery(self.db)

        query_str = (
            "select id from comptages.sensor where id_lane = {0};".format(
                lane_id))

        query.exec_(query_str)
        if query.next():
            return True
        return False

    def get_sensor_length(self, lane_id):
        """ Get length of geometry in the sensor table"""

        self.init_db_connection()
        query = QSqlQuery(self.db)

        query_str = (
            "select ST_LENGTH(geometry) from comptages.sensor where id_lane = {};".format(lane_id))

        query.exec_(query_str)

        if query.next():
            return query.value(0)
        return None
