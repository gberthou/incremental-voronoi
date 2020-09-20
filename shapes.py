import math

import utils

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
        line = InfiniteLine(center, direction)
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

class InfiniteLine:
    def __init__(self, point, direction):
        self.point = point
        self.direction = direction
        self.normal = utils.orthogonal(self.direction)

    def _k_intersect(self, other):
        u2 = utils.dot(self.direction, self.direction)
        v2 = utils.dot(other.direction, other.direction)
        uv = utils.dot(self.direction, other.direction)

        AC = utils.vector(self.point, other.point)
        AC_u = utils.dot(AC, self.direction)
        AC_v = utils.dot(AC, other.direction)

        lower = u2*v2 - uv * uv
        if lower == 0:
            return None
        return (AC_u * v2 - AC_v * uv) / lower

    def intersect(self, other):
        k = self._k_intersect(other)
        if k == None:
            return None
        return (self.point[0] + k * self.direction[0], self.point[1] + k * self.direction[1])

    def has_point(self, point):
        EPSILON = 1e-4
        AB = utils.vector(self.point, point)
        return abs(utils.dot(AB, self.normal)) < EPSILON

    def constrain(self, other_item, center):
        AB = utils.vector(self.point, other_item.line.point)

        n = self.normal
        if utils.dot(utils.vector(self.point, center), n) < 0:
            n = (-n[0], -n[1])

        v_n = utils.dot(other_item.line.direction, n)
        AB_n = utils.dot(AB, n)

        if v_n > 0:
            other_item.k.set_min(-AB_n / v_n)
        if v_n < 0:
            other_item.k.set_max(-AB_n / v_n)

class Segment:
    def __init__(self, A, B):
        self.A = A
        self.B = B
        self.line = InfiniteLine(A, utils.vector(A, B))

    def intersect(self, infinite_line):
        k = self.line._k_intersect(infinite_line)
        if k != None and k >= 0 and k <= 1:
            return (self.line.point[0] + k * self.line.direction[0], self.line.point[1] + k * self.line.direction[1])
        return None

    def intersect_segment(self, segment):
        inter = self.intersect(segment.line)
        if inter == None:
            return None
        if segment.intersect(self.line) == None:
            return None
        return inter

    def replace(self, old, new):
        if self.A == old:
            self.A = new
        elif self.B == old:
            self.B = new
        else:
            raise Exception("Segment.replace")
        self.line = InfiniteLine(self.A, utils.vector(self.A, self.B))

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

def common_to_segments(A, B):
    if utils.equals(A.A, B.A) or utils.equals(A.A, B.B):
        return A.A
    if utils.equals(A.B, B.A) or utils.equals(A.B, B.B):
        return A.B
    return None

def other_vertex_of_segment(A, x):
    if utils.equals(A.A, x):
        return A.B
    if utils.equals(A.B, x):
        return A.A
    return None

class Shape:
    def __init__(self, point_item):
        self.vertices = set()
        if len(point_item.others) < 2:
            return
        if len(set(other for other in point_item.others if not other.k.is_determined())) > 0:
            return

        # Compute segments edges
        for other in point_item.others:
            kmin = other.k.min
            kmax = other.k.max

            v1 = (other.line.point[0] + kmin * other.line.direction[0], other.line.point[1] + kmin * other.line.direction[1])
            v2 = (other.line.point[0] + kmax * other.line.direction[0], other.line.point[1] + kmax * other.line.direction[1])

            for v in [v1, v2]:
                EPSILON = 1e-4
                distances = list(utils.distance2(v, i) for i in self.vertices)
                if len(distances) == 0 or min(distances) > EPSILON:
                    self.vertices |= {v}

        # Sort vertices to make the shape convex
        self.vertices = list(self.vertices)
        OA = utils.vector(point_item.point, self.vertices[0])
        len_OA = utils.length(OA)
        t = {(self.vertices[0], 0)}
        for vertex in self.vertices[1:]:
            OB = utils.vector(point_item.point, vertex)
            len_OB = utils.length(OB)
            cos_angle = utils.dot(OA, OB) / (len_OA * len_OB)
            if cos_angle < -1:
                cos_angle = -1
            elif cos_angle > 1:
                cos_angle = 1

            angle = math.acos(cos_angle)
            if utils.cross(OA, OB) < 0: # sign of sin
                angle = 2 * math.pi - angle
            t |= {(vertex, angle)}
        self.vertices = list(vertex for vertex, _ in sorted(t, key = lambda x: x[1]))
