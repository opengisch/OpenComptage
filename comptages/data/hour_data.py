

class HourData():

    def __init__(self):
        self.direction_data = []

    def total(self, direction=None):
        if direction is None:
            return sum([i.total() for i in self.direction_data])
        return self.direction_data[direction].total()

    def light_vehicles(self, direction=None):
        if direction is None:
            return sum([i.light_vehicles() for i in self.direction_data])
        return self.direction_data[direction].light_vehicles()

    def heavy_vehicles(self, direction=None):
        if direction is None:
            return sum([i.heavy_vehicles() for i in self.direction_data])
        return self.direction_data[direction].heavy_vehicles()

    def percent_heavy_vehicles(self, direction=None):
        if self.total(direction) * self.heavy_vehicles(direction) == 0:
            return 0
        return round(100 / self.total(direction) *
                     self.heavy_vehicles(direction), 2)

    def __str__(self):
        return str(self.direction_data)
