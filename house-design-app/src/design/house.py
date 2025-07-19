class Wall:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def as_dict(self):
        return {'x': self.x, 'y': self.y, 'width': self.width, 'height': self.height}

class House:
    def __init__(self):
        self.walls = []
        self.rooms = []

    def add_wall(self, wall):
        self.walls.append(wall)

    def add_room(self, room):
        self.rooms.append(room)

    def total_area(self):
        return sum(wall.area() for wall in self.walls)

    def __str__(self):
        return f"House with {len(self.walls)} walls and {len(self.rooms)} rooms."