from qgis.PyQt.QtWidgets import QDialog

from comptages.qgissettingmanager import SettingManager, Scope
from comptages.qgissettingmanager.types import String, Integer, Bool
from comptages.qgissettingmanager.setting_dialog import SettingDialog

from comptages.core.utils import get_ui_class

FORM_CLASS = get_ui_class('settings_dialog.ui')


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


class SettingsDialog(QDialog, FORM_CLASS, SettingDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)
        self.settings = Settings()
        SettingDialog.__init__(self, self.settings)
        self.init_widgets()
