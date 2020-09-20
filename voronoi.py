import utils
import shapes
import chunk_generic
import chunk_voronoi

class OtherItem:
    def __init__(self, other, line):
        self.other = other
        self.line = line
        self.k = utils.Variable()

    def is_valid(self):
        return self.k.is_valid()

class PointItem:
    def __init__(self, point):
        self.point = point
        self.others = set()

    def add_other(self, other):
        u = utils.vector(self.point, other)

        direction = utils.orthogonal(u)
        center = (.5 * (self.point[0] + other[0]), .5 * (self.point[1] + other[1]))
        line = shapes.InfiniteLine(center, direction)
        new_item = OtherItem(other, line)

        keep_new_item = True
        others_to_remove = set()

        for other in self.others:
            other.line.constrain(new_item, self.point)
            new_item.line.constrain(other, self.point)

            if not other.is_valid():
                others_to_remove |= {other}

            if not new_item.is_valid():
                keep_new_item = False
                break

        self.others -= others_to_remove

        if keep_new_item:
            self.others |= {new_item}
            return new_item
        return None

class PointSet:
    def __init__(self):
        self.point_items = set()

    def add_point(self, point):
        item = PointItem(point)

        for i in self.point_items:
            new_item = item.add_other(i.point)
            if new_item != None:
                i.add_other(point)
        self.point_items |= {item}

class VoronoiExplorer:
    def __init__(self, filename, density):
        self.chunk_generator = chunk_voronoi.VoronoiChunkGenerator(density)
        self.chunk_database = chunk_voronoi.VoronoiChunkDatabase(filename)
        self.chunk_manager = chunk_generic.ChunkManager(self.chunk_generator, self.chunk_database)

        self.pointset = PointSet()

    def load_chunk(self, key):
        is_new_chunk, chunk = self.chunk_manager.load_chunk(key)

        if is_new_chunk:
            for point in chunk:
                self.pointset.add_point(point)

    def unload_chunk(self, key):
        chunk = self.chunk_manager.unload_chunk(key)

    def keep_only_chunks(self, keys):
        self.chunk_manager.keep_only_chunks(keys)
