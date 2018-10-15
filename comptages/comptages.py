# -*- coding: utf-8 -*-

from PyQt5.QtCore import QSettings, QTranslator, qVersion, QCoreApplication, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QFileDialog, QVBoxLayout, QComboBox, QWidget, QDialog
from qgis.gui import QgsDockWidget

from functools import partial

from qgis.core import (
    QgsProject, QgsFeatureRequest, QgsAction, QgsActionManager, QgsRelation,
    QgsEditorWidgetSetup
)
from qgis.utils import qgsfunction

# Initialize Qt resources from file resources.py
from .resources import *

# Import the code for the DockWidget
from .Comptages_dockwidget import ComptagesDockWidget
from .settings import ComptagesSettings
from .utils import load_layer_pg
from .definitions import LAYER_DEFINITIONS
from .filter_dialog import FilterDialog
#from .data_validation_dock import DataValidationWidget
import os.path


class Comptages:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface

        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)

        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'Comptages_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Comptages')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'Comptages')
        self.toolbar.setObjectName(u'Comptages')

        self.pluginIsActive = False
        self.dockwidget = None

        self.settings = ComptagesSettings()

        self.layers = {}
        
    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('Comptages', message)

    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/Comptages/images/icon.png'

        self.action_connect_db = self.add_action(
            ':/plugins/Comptages/images/power.png',
            text=self.tr('Connect DB'),
            callback=partial(self.run_command, 'connect_db'),
            parent=self.iface.mainWindow()
        )

        self.action_create_new = self.add_action(
            ':/plugins/Comptages/images/measure.png',
            text=self.tr('Create new measure'),
            callback=partial(self.run_command, 'create_new'),
            parent=self.iface.mainWindow(),
            enabled_flag=False
        )

        self.action_select = self.add_action(
            ':/plugins/Comptages/images/select_edit.png',
            text=self.tr('Edit measure'),
            callback=partial(self.run_command, 'edit'),
            parent=self.iface.mainWindow(),
            enabled_flag=False
        )

        self.action_filter = self.add_action(
            ':/plugins/Comptages/images/filter.png',
            text=self.tr('Filter'),
            callback=partial(self.run_command, 'filter'),
            parent=self.iface.mainWindow(),
            enabled_flag=False
        )

        self.action_import_periods = self.add_action(
            ':/plugins/Comptages/images/calendar.png',
            text=self.tr('Import special periods'),
            callback=partial(self.run_command, 'import_periods'),
            parent=self.iface.mainWindow(),
            enabled_flag=False
        )

        self.action_settings = self.add_action(
            ':/plugins/Comptages/images/settings.png',
            text=self.tr('Settings'),
            callback=partial(self.run_command, 'settings'),
            parent=self.iface.mainWindow())

    def onClosePlugin(self):
        """Cleanup necessary items here when plugin dockwidget is closed"""

        # disconnects
        self.dockwidget.closingPlugin.disconnect(self.onClosePlugin)

        # remove this statement if dockwidget is to remain
        # for reuse if plugin is reopened
        # Commented next statement since it causes QGIS crashe
        # when closing the docked window:
        # self.dockwidget = None

        self.pluginIsActive = False

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""

        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Comptages'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

    def is_connected(self):
        """Return if the plugin is connected to the database"""

        return True

    def enable_actions_if_allowed(self):
        """Enable or disable the actions depending on the connection status"""

        enable = self.is_connected()

        self.action_create_new.setEnabled(enable)
        self.action_select.setEnabled(enable)
        self.action_filter.setEnabled(enable)
        self.action_import_periods.setEnabled(enable)

    def run(self):
        """Run method that loads and starts the plugin"""

        if not self.pluginIsActive:
            self.pluginIsActive = True

            # dockwidget may not exist if:
            #    first run of plugin
            #    removed on close (see self.onClosePlugin method)
            if self.dockwidget is None:
                # Create the dockwidget (after translation) and keep reference
                self.dockwidget = ComptagesDockWidget()

            # connect to provide cleanup on closing of dockwidget
            self.dockwidget.closingPlugin.connect(self.onClosePlugin)

            # show the dockwidget
            # TODO: fix to allow choice of dock location
            self.iface.addDockWidget(Qt.LeftDockWidgetArea, self.dockwidget)
            self.dockwidget.show()

    def run_command(self, command):

        # TODO check if the layers required by the command are loaded
        print(f"run_command {command}")

        if command == 'connect_db':
            self.load_layers()

        if command == 'edit':
            self.edit()

        if command == 'filter':
            self.show_filter()

        if command == 'create_new':
            self.create_new()
            
        self.enable_actions_if_allowed()

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

                layer = load_layer_pg(
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
        #self.add_layer_actions()
        self.create_relations()
        self.iface.setActiveLayer(self.layers['section'])


    def create_relations(self):
        #rel = QgsRelation()
        #rel.setName('Relation installation - count')
        #rel.setId('rel_installation_count')
        #rel.setReferencedLayer(self.layers['installation'].id())
        #rel.setReferencingLayer(self.layers['count'].id())
        #rel.addFieldPair('id_installation', 'id')
        #QgsProject.instance().relationManager().addRelation(rel)
        
        widget = QgsEditorWidgetSetup('ValueRelation',
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

        widget = QgsEditorWidgetSetup('ValueRelation',
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

        widget = QgsEditorWidgetSetup('ValueRelation',
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

        widget = QgsEditorWidgetSetup('ValueRelation',
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

        widget = QgsEditorWidgetSetup('ValueRelation',
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


    def edit(self):
        # TODO manage error if nothing is to be selected
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
            counts = self.get_counts_of_section(selected_feature.attribute('id'))
            ids = []
            for c in counts:
                ids.append(c.attribute('id'))
            self.open_counts_attribute_table_and_filter(ids)

    def create_new(self):
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

            # TODO set automatically installation_id
            self.layers['count'].startEditing()
            self.iface.setActiveLayer(self.layers['count'])
            self.iface.actionAddFeature().trigger()

            
    def open_counts_attribute_table_and_filter(self, count_ids):
        if not count_ids:
            self.pushInfo("No counts found for this section")
            return

        self.iface.showAttributeTable(
            self.layers['count'],
            f'"id" in ({", ".join(map(str, count_ids))})')

    def get_counts_of_section(self, section_id):
        # select distinct c.id from comptages.lane as l
        # INNER JOIN comptages.installation as i ON
        # (l.id_installation = i.id) INNER JOIN
        # comptages.count as c ON (i.id = c.id_installation)
        # where id_section = '64040050';
        # Best via query or with QGIS api?
        try:
            lanes = self.get_lanes_of_section(section_id)
            installation = self.get_installation_of_lane(next(lanes).attribute('id'))
            counts = self.get_counts_of_installation(installation.attribute('id'))
        except StopIteration:
            return []

        return counts

    def get_lanes_of_section(self, section_id):

        request = QgsFeatureRequest().setFilterExpression(
            f'"id_section" = \'{section_id}\''
        )

        return self.layers['lane'].getFeatures(request)

    def get_installation_of_lane(self, lane_id):

        lane = next(self.layers['lane'].getFeatures(f'"id"={lane_id}'))
        installation_id = lane.attribute('id_installation')

        return next(self.layers['installation'].getFeatures(
            f'"id"={installation_id}'))

    def get_counts_of_installation(self, installation_id):
        # TODO verify if more than one layer is returned

        request = QgsFeatureRequest().setFilterExpression(
            f'"id_installation" = {installation_id}'
        )

        return self.layers['count'].getFeatures(request)
    
    def add_layer_actions(self):
        action_manager = self.layers['count'].actions()

        action_export_configuration = QgsAction(
            QgsAction.GenericPython,
            'Export configuration',
            "from qgis.utils import plugins\nplugins['comptages'].export_configuration([% $id %])")
        action_export_configuration.setActionScopes(['Feature'])
        action_manager.addAction(action_export_configuration)

        action_import_data = QgsAction(
            QgsAction.GenericPython,
            'Import data',
            "from qgis.utils import plugins\nplugins['comptages'].import_data([% $id %])")
        action_import_data.setActionScopes(['Feature'])
        action_manager.addAction(action_import_data)

        action_create_report = QgsAction(
            QgsAction.GenericPython,
            'Create report',
            "from qgis.utils import plugins\nplugins['comptages'].create_report([% $id %])")
        action_create_report.setActionScopes(['Feature'])
        action_manager.addAction(action_create_report)

        action_export_plan = QgsAction(
            QgsAction.GenericPython,
            'Export plan',
            "from qgis.utils import plugins\nplugins['comptages'].export_plan([% $id %])")
        action_export_plan.setActionScopes(['Feature'])
        action_manager.addAction(action_export_plan)

    @staticmethod
    def export_configuration(count_id):
        file_dialog = QFileDialog()
        title = 'Export configuration file'
        path = '/home/mario/workspace/tmp/comptages/'
        file = QFileDialog.getSaveFileName(file_dialog, title, path)
        print(f"export_configuration file {file} for {count_id}")

    @staticmethod
    def import_data(count_id):
        file_dialog = QFileDialog()
        title = 'Import data'
        path = '/home/mario/workspace/tmp/comptages/'
        file = QFileDialog.getOpenFileName(file_dialog, title, path, "Data file (*.A?? *.aV? *.I?? *.V??)")
        print(f"import_data file {file} from {count_id}")

        #self.widget = DataValidationWidget(self.iface)
        #self.widget.show()
  
    @staticmethod
    def create_report(count_id):
        file_dialog = QFileDialog()
        title = 'Export report'
        path = '/home/mario/workspace/tmp/comptages/'
        file = QFileDialog.getSaveFileName(file_dialog, title, path, "PDF (*.pdf)")
        print(f"create_report {file} for {count_id}")

    @staticmethod
    def export_plan(count_id):
        file_dialog = QFileDialog()
        title = 'Export plan'
        path = '/home/mario/workspace/tmp/comptages/'
        file = QFileDialog.getSaveFileName(file_dialog, title, path,  "PDF (*.pdf)")
        print(f"export_plan {file} for {count_id}")

    def apply_qml_styles(self):
        for key in LAYER_DEFINITIONS:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            qml_file_path = os.path.join(current_dir, 'qml', f'{key}.qml')
            self.layers[key].loadNamedStyle(qml_file_path)

    def set_value_relation_fields(self):
        pass

    def pushInfo(self, text):
        self.iface.messageBar().pushInfo('Comptages', text)

    @qgsfunction(args="auto", group="Comptages")
    def is_highlighted(feature, parent):
        highlighted = ['64040050', '10020290', '64080015', '64080019', '64080159']

        if(feature.attribute('id') in highlighted):
            return True
        return False

    def show_filter(self):
        self.dialog = FilterDialog(self.iface)
        self.dialog.show()

        
        
        
