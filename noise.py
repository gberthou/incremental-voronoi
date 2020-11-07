from opensimplex import OpenSimplex

class Noise:
    def __init__(self, zoom, seed = 0):
        self.noise = OpenSimplex(seed)
        self.zoom = zoom

    def get(self, X, Y):
        return (X+Y)/10
        return self.noise.noise2d(x = (X * self.zoom), y = (Y * self.zoom))
