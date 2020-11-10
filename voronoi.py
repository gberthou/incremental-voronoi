import utils
import shapes
import chunk_generic
import chunk_voronoi

class OtherItem:
    def __init__(self, item, line):
        self.item = item
        self.line = line
        self.k = utils.Variable()

    def is_valid(self):
        return self.k.is_valid()

    def vertices(self):
        if not self.is_valid():
            raise Exception("OtherItem.vertices")
        kmin = self.k.min
        kmax = self.k.max

        v1 = (self.line.point[0] + kmin * self.line.direction[0], self.line.point[1] + kmin * self.line.direction[1])
        v2 = (self.line.point[0] + kmax * self.line.direction[0], self.line.point[1] + kmax * self.line.direction[1])
        return (v1, v2)

class PointItem:
    def __init__(self, key, point):
        self.key = key
        self.point = point
        self.others = set()

    def add_item(self, item):
        u = utils.vector(self.point, item.point)

        direction = utils.orthogonal(u)
        center = (.5 * (self.point[0] + item.point[0]), .5 * (self.point[1] + item.point[1]))
        line = shapes.InfiniteLine(center, direction)
        new_item = OtherItem(item, line)

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

    def is_bounded(self):
        if len(self.others) < 2:
            return False
        if len(set(other for other in self.others if not other.k.is_determined())) > 0:
            return False
        return True

    def delete_points(self, points_to_delete):
        EPSILON = 1e-4
        others_to_delete = set()
        for p in points_to_delete:
            for other in self.others:
                if utils.distance2(other.item.point, p) < EPSILON:
                    others_to_delete |= {other}
        self.others -= others_to_delete

class PointSet:
    def __init__(self):
        self.point_items = set()

    def add_point(self, key, point):
        item = PointItem(key, point)

        for i in self.point_items:
            new_item = item.add_item(i)
            if new_item != None:
                i.add_item(item)
        self.point_items |= {item}

    def delete_points(self, points_to_delete):
        EPSILON = 1e-4
        items_to_delete = set()
        for i in self.point_items:
            to_delete = False
            for p in points_to_delete:
                if utils.distance2(i.point, p) < EPSILON:
                    items_to_delete |= {i}
                    to_delete = True
                    break
            if not to_delete:
                i.delete_points(points_to_delete)
        self.point_items -= items_to_delete

    def item_that_contains(self, point):
        for point_item in self.point_items:
            if not point_item.is_bounded():
                continue

            skip = False
            for other in point_item.others:
                edge_normal = utils.orthogonal(other.line.direction)
                A, B = other.vertices()
                AO = utils.vector(A, point_item.point)
                AP = utils.vector(A, point)
                if utils.dot(AO, edge_normal) * utils.dot(AP, edge_normal) < 0:
                    skip = True
                    break
            if not skip:
                return point_item
        raise Exception("PointSet.item_that_contains: not found")

    def neighbors_of(self, point_item):
        return set(other.item for other in point_item.others)

class VoronoiExplorer:
    def __init__(self, filename, density):
        self.chunk_generator = chunk_voronoi.VoronoiChunkGenerator(density)
        self.chunk_database = chunk_voronoi.VoronoiChunkDatabase(filename)
        self.chunk_manager = chunk_generic.ChunkManager(self.chunk_generator, self.chunk_database)

        self.pointset = PointSet()

    def load_chunk(self, key):
        is_new_chunk, chunk = self.chunk_manager.load_chunk(key)

        if is_new_chunk:
            for i, point in enumerate(chunk):
                self.pointset.add_point((*key, i), point)

    def unload_chunk(self, key):
        deleted_chunk = self.chunk_manager.unload_chunk(key)
        self.pointset.delete_points(deleted_chunk)

    def keep_only_chunks(self, keys):
        deleted_chunks = self.chunk_manager.keep_only_chunks(keys)
        for deleted_chunk in deleted_chunks:
            self.pointset.delete_points(deleted_chunk)

    def loaded_shapes(self):
        return list(shapes.Shape(i) for i in self.pointset.point_items)

