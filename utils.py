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

