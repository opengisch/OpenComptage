from statistics import mean


class CountData():

    def __init__(self):
        self.day_data = []
        self.attributes = {}
        self.month_data = [0]*12

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
                      for i in self.day_data]), 1)
        return round(
            mean([self.day_data[i].percent_heavy_vehicles(direction)
                  for i in days]), 1)

    def speed_cumulus(self, direction, days):
        bin_size = len(
            self.day_data[0].hour_data[0].direction_data[0].speed_data)
        _ = [0]*bin_size
        result = [_]*24
        for i in days:
            day = self.day_data[i]
            for j in range(24):
                result[j] = [sum(pair) for pair in zip(
                    result[j], day.hour_data[j].speed(direction))]
        return result

    def category_cumulus(self, direction, days):
        bin_size = len(
            self.day_data[0].hour_data[0].direction_data[0].category_data)
        _ = [0]*bin_size
        result = [_]*24
        for i in days:
            day = self.day_data[i]
            for j in range(24):
                result[j] = [sum(pair) for pair in zip(
                    result[j], day.hour_data[j].category(direction))]
        return result

    def total(self, direction, days):
        return sum([self.day_data[i].total(direction) for i in days])

    def __str__(self):
        return str("Count data: {}".format(self.day_data))
