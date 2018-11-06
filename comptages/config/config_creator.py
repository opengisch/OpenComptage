import abc


class ConfigCreator(metaclass=abc.ABCMeta):

    def __init__(self, layers, count_id):
        self.layers = layers
        self.count_id = count_id

    def write_file(self, file):
        pass


class ConfigCreatorCmd(ConfigCreator):

    commands = dict()

    def set_section_commands(self):
        sections = self.layers.get_sections_of_count(self.count_id)

        self.set_command('SITE', sections[0].attribute('id'))
        self.set_command('LOCATION', sections[0].attribute('name'))

    def set_command(self, command, value):
        self.commands[command] = value

    def write_file(self, file):
        with open(file, 'w') as f:
            for command in self.commands.keys():
                f.write(f'{command} = {self.commands[command]}\n')
