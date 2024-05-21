import numpy as np

class Point:
    counter = 0

    def __init__(self, x, y, z, point_type='point'):
        self.id = Point.counter
        Point.counter += 1
        self.coords = np.array([x, y, z])
        self.type = point_type

class Centroid:
    counter = 0

    def __init__(self, x, y, z):
        self.id = Centroid.counter
        Centroid.counter += 1
        self.coords = np.array([x, y, z])
