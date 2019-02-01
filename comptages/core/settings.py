import os

from qgis.PyQt.QtWidgets import QDialog
from qgis.PyQt.uic import loadUiType

from comptages.qgissettingmanager import SettingManager, Scope
from comptages.qgissettingmanager.types import String, Integer, Bool
from comptages.qgissettingmanager.setting_dialog import SettingDialog


class Settings(SettingManager):
    def __init__(self):
        SettingManager.__init__(self, 'Comptages')

        self.add_setting(
            String("db_host", Scope.Global, 'comptages-db'))
        self.add_setting(
            String("db_name", Scope.Global, 'comptages'))
        self.add_setting(
            Integer("db_port", Scope.Global, 5432))
        self.add_setting(
            String("db_username", Scope.Global, 'postgres'))
        self.add_setting(
            String("db_password", Scope.Global, 'postgres'))
        self.add_setting(
            Bool("extra_layers", Scope.Global, False))
        self.add_setting(
            String("config_export_directory", Scope.Global, '/'))
        self.add_setting(
            String("plan_export_directory", Scope.Global, '/'))
        self.add_setting(
            String("data_import_directory", Scope.Global, '/'))
        self.add_setting(
            String("picture_directory", Scope.Global, '/'))
        self.add_setting(
            String("report_export_directory", Scope.Global, '/'))


def get_ui_class(ui_file):
    """Get UI Python class from .ui file.
       Can be filename.ui or subdirectory/filename.ui
    :param ui_file: The file of the ui in svir.ui
    :type ui_file: str
    """
    os.path.sep.join(ui_file.split('/'))
    ui_file_path = os.path.abspath(
            os.path.join(
                    os.path.dirname(__file__),
                    os.pardir,
                    'ui',
                    ui_file
            )
    )
    return loadUiType(ui_file_path)[0]


FORM_CLASS = get_ui_class('settings_dialog.ui')


class SettingsDialog(QDialog, FORM_CLASS, SettingDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)
        self.settings = Settings()
        SettingDialog.__init__(self, self.settings)
        self.init_widgets()
