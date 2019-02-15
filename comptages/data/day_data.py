

class DayData():

    def __init__(self):
        self.hour_data = []

    def total(self, direction=None):
        return sum([i.total(direction) for i in self.hour_data])

    def light_vehicles(self, direction=None):
        return sum([i.light_vehicles(direction) for i in self.hour_data])

    def heavy_vehicles(self, direction=None):
        return sum([i.heavy_vehicles(direction) for i in self.hour_data])

    def percent_heavy_vehicles(self, direction=None):
        if self.total(direction) * self.heavy_vehicles(direction) == 0:
            return 0
        return round(100 / self.total(direction) *
                     self.heavy_vehicles(direction), 2)

    def __str__(self):
        return str(self.hour_data)
