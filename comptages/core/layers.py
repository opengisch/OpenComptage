import os

from qgis.PyQt.QtCore import QObject
from qgis.core import (
    QgsProject, QgsEditorWidgetSetup, QgsVectorLayer,
    QgsCoordinateReferenceSystem, QgsDataSourceUri,
    QgsAction, QgsFeatureRequest)

from comptages.core.definitions import LAYER_DEFINITIONS
from comptages.core.settings import ComptagesSettings


class Layers(QObject):

    def __init__(self, iface):
        QObject.__init__(self)
        self.iface = iface
        self.layers = {}

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

                print(f"loaded_layer: {layer_definition['display_name']}")

        self.apply_qml_styles()
        self.add_layer_actions()
        self.create_relations()
        self.iface.setActiveLayer(self.layers['section'])

    def apply_qml_styles(self):
        for key in LAYER_DEFINITIONS:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            qml_file_path = os.path.join(
                current_dir, os.pardir, 'qml', f'{key}.qml')
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

        settings = ComptagesSettings()
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

    def edit_count(self):
        """Open attribute table of count filtered with only the
        features related to the selected section"""

        # TODO manage error if nothing is to be showed
        # TODO display messages with the correct bar
        layer = self.layers['section']

        selected_count = layer.selectedFeatureCount()
        if selected_count == 0:
            self.pushInfo("Please select a section")
            return
        elif selected_count > 1:
            self.pushInfo("Please select only one section")
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
            self.pushInfo("No counts found for this section")
            return

        self.iface.showAttributeTable(
            self.layers['count'],
            f'"id" in ({", ".join(map(str, count_ids))})')

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
            f'"id_section" = \'{section_id}\''
        )

        return self.layers['lane'].getFeatures(request)

    def get_installation_of_lane(self, lane_id):
        """Return the installation feature of the passes lane"""
        lane = next(self.layers['lane'].getFeatures(f'"id"={lane_id}'))
        installation_id = lane.attribute('id_installation')

        return next(self.layers['installation'].getFeatures(
            f'"id"={installation_id}'))

    def get_counts_of_installation(self, installation_id):
        """Return a list of count features related with the passsed
        installation"""
        # TODO verify if more than one layer is returned

        request = QgsFeatureRequest().setFilterExpression(
            f'"id_installation" = {installation_id}'
        )

        return self.layers['count'].getFeatures(request)

    def is_section_highlighted(self, section_id):
        """Return if the passed section has related counts with the current
        filter settings"""

        # TODO optimize with a cached list of sections or using a faster query

        if not self.get_counts_of_section(section_id):
            return False
        return True
