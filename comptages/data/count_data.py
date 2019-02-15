from statistics import mean


# TODO: rename in CountDataSection ?
class CountData():

    def __init__(self):
        self.day_data = []

    def average_total(self, direction=None, days=None):
        if days is None:
            return round(
                mean([i.total(direction) for i in self.day_data]))
        return round(
            mean([self.day_data[i].total(direction) for i in days]))

    def average_light_vehicles(self, direction=None, days=None):
        if days is None:
            return round(
                mean([i.light_vehicles(direction) for i in self.day_data]))
        return round(
            mean([self.day_data[i].light_vehicles(direction) for i in days]))

    def average_heavy_vehicles(self, direction=None, days=None):
        if days is None:
            return round(
                mean([i.heavy_vehicles(direction) for i in self.day_data]))
        return round(
            mean([self.day_data[i].heavy_vehicles(direction) for i in days]))

    def average_percent_heavy_vehicles(self, direction=None, days=None):
        if days is None:
            return round(
                mean([i.percent_heavy_vehicles(direction)
                      for i in self.day_data]), 2)
        return round(
            mean([self.day_data[i].percent_heavy_vehicles(direction)
                  for i in days]), 2)

    def __str__(self):
        return str("Count data: {}".format(self.day_data))
