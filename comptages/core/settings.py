from comptages.qgissettingmanager import SettingManager, Scope
from comptages.qgissettingmanager.setting_dialog import SettingDialog
from comptages.qgissettingmanager.types import String, Integer


class ComptagesSettings(SettingManager):

    def __init__(self):
        SettingManager.__init__(self, 'comptages')

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

        
