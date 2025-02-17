import math


class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vec = (x, y)
        self.mag = math.sqrt(x**2 + y**2)

    def normalise(self):
        if self.mag == 0:
            return self.copy()
        return Vec2(self.x / self.mag, self.y / self.mag)

    def copy(self):
        return Vec2(self.x, self.y)

    def dot(self, otherVec2):
        return self.x * otherVec2.x + self.y * otherVec2.y

    def multiply_vec(self, otherVec2):
        return Vec2(self.x * otherVec2.x, self.y * otherVec2.y)

    def clamp(self, lowerBound=(0, 0), upperBound=(255, 255)):
        return Vec2(min(max(self.x, lowerBound[0]), upperBound[0]),
                    min(max(self.y, lowerBound[1]), upperBound[1]))

    def set(self, x=False, y=False):
        if x:
            self.x = x
        if y:
            self.y = y

    def update_val(self):
        self.vec = (self.x, self.y)
        self.mag = math.sqrt(self.x**2 + self.y**2)

    def __add__(self, otherVec2):
        return Vec2(self.x + otherVec2.x, self.y + otherVec2.y)

    def __sub__(self, otherVec2):
        return Vec2(self.x - otherVec2.x, self.y - otherVec2.y)

    def __mul__(self, mag):
        return Vec2(self.x * mag, self.y * mag)

    def __truediv__(self, mag):
        return Vec2(self.x / mag, self.y / mag)

    def __neg__(self):
        return Vec2(-self.x, -self.y)

    def __abs__(self):
        return Vec2(abs(self.x), abs(self.y))

    def __str__(self):
        return f"{self.x} {self.y}"

    def __mod__(self, n):
        return Vec2(self.x % n, self.y % n)

    def __floordiv__(self, n):
        return Vec2(self.x // n, self.y // n)