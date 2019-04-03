

class DirectionData():

    def __init__(
            self, light_indexes=[]):
        self.light_indexes = light_indexes
        self.speed_data = []
        self.category_data = []

    def total(self):
        result = sum(self.category_data)
        if result == 0:
            result = sum(self.speed_data)
        return result

    def light_vehicles(self):
        return sum([self.category_data[i] for i in self.light_indexes])

    def heavy_vehicles(self):
        return self.total() - self.light_vehicles()

    def percent_heavy_vehicles(self):
        return round(100 / self.total() * self.heavy_vehicles(), 1)

    def __str__(self):
        return str("Speed_data: {}, category_data: {}".format(
            self.speed_data, self.category_data))
