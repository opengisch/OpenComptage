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

        self.set_command(
            'SITE',
            self.layers.get_installation_name_of_count(self.count_id))
        self.set_command('LOCATION', sections[0].attribute('name'))
        self.set_command(
            'FILENAME',
            self.layers.get_installation_name_of_count(self.count_id))
        self.set_command(
            'CLASS',
            self.layers.get_class_name_of_count(self.count_id))
        self.set_command('LPLENS', '200')

        lanes = self.layers.get_lanes_of_count(self.count_id)
        sensor_type = self.layers.get_sensor_type_of_count(self.count_id)
        channels_str = ''
        sensors_str = ''
        carriageway_nr = 0
        sensor_length = None

        for i, lane in enumerate(lanes):
            channels_str += '{} '.format(i+1)
            if sensor_type.attribute('name') == 'Boucle':
                sensors_str += '{} '.format('LL')
            else:
                sensors_str += '{} '.format('TT')

            if self.layers.check_sensor_of_lane(lane.id()):
                carriageway_nr += 1

            length = self.layers.get_sensor_length(lane.id())
            if length:
                sensor_length = length

        self.set_command('CHANNELS', channels_str)
        self.set_command('SENSORS', sensors_str)

        self.set_command(
            'CARRIAGEWAY',
            ' '.join('1' * carriageway_nr) + ' ' + ' '.join('0' * (8 - carriageway_nr)))

        if sensor_length and sensor_length < 6:
            self.set_command('LPSEPS', '300')
        else:
            self.set_command('LPSEPS', '500')

    def set_command(self, command, value):
        self.commands[command] = value

    def set_predefined_config(self):
        return self.layers.get_predefined_config_from_count(self.count_id)

    def write_file(self, file):
        with open(file, 'w') as f:
            f.write('{}\n'.format(self.set_predefined_config()))
            for command in self.commands.keys():
                f.write('{} = {}\n'.format(command, self.commands[command]))
