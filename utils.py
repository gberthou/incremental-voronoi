import math

def vector(A, B):
    return (B[0] - A[0], B[1] - A[1])

def orthogonal(v):
    return (v[1], -v[0])

def dot(u, v):
    return u[0] * v[0] + u[1] * v[1]

def cross(u, v):
    return u[0] * v[1] - u[1] * v[0]

def distance2(A, B):
    v = vector(A, B)
    return dot(v, v)

def equals(A, B):
    return distance2(A, B) < 1e-4

def length(u):
    return math.sqrt(dot(u, u))

def normalize(v):
    l = length(v)
    return (v[0] / l, v[1] / l)

def center_circumcircle(A, B, C):
    #AB = vector(A, B)
    #AC = vector(A, C)

    #u = normalize(orthogonal(AB))
    #v = normalize(orthogonal(AC))
    #uv = dot(u, v)

    #k = (dot(AC, u) + dot(AB, v) * uv) / (2 - 2 * uv * uv)
    #return (AB[0] / 2 - k * u[0], AB[1] / 2 - k * u[1])

    AB = vector(A, B)
    AC = vector(A, C)
    BC = vector(B, C)

    u = orthogonal(AB)
    v = orthogonal(AC)
    u2 = dot(u, u)
    v2 = dot(v, v)
    uv = dot(u, v)

    k = .5 * (dot(BC, u) * uv - dot(BC, v) * u2) / (uv * uv - u2 * v2)
    return (A[0] + AC[0] / 2 - k * v[0], A[1] + AC[1] / 2 - k * v[1])


def get_triangles(nodes):
    triangles = list()
    for n1 in nodes:
        s = set(i for i in nodes if i != n1)
        t = sorted(s, key = lambda x: distance2(x, n1))
        triangles.append((n1, t[0], t[1]))
    return triangles

class Variable:
    def __init__(self):
        self.min = None
        self.max = None

    def set_min(self, x):
        if self.min == None:
            self.min = x
        else:
            self.min = max(x, self.min)

    def set_max(self, x):
        if self.max == None:
            self.max = x
        else:
            self.max = min(x, self.max)

    def is_valid(self):
        return self.min == None or self.max == None or self.min <= self.max

    def is_determined(self):
        return self.is_valid() and self.min != None and self.max != None

