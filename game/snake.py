import random
from enum import Enum

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class Snake:
    def __init__(self, grid_width, grid_height):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.body = [(grid_width // 2, grid_height // 2)]
        self.direction = Direction.RIGHT
        self.next_direction = Direction.RIGHT

    def move(self):
        self.direction = self.next_direction
        dx, dy = self.direction.value
        head_x, head_y = self.body[0]
        new_head = (head_x + dx, head_y + dy)
        self.body.insert(0, new_head)

    def grow(self):
        pass  # Body already extended by move()

    def check_collision(self):
        head = self.body[0]
        # Check wall collision
        if head[0] < 1 or head[0] >= self.grid_width or head[1] < 1 or head[1] >= self.grid_height:
            return True
        # Check self collision
        if head in self.body[1:]:
            return True
        return False

class Food:
    def __init__(self, grid_width, grid_height):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.position = self.spawn()

    def spawn(self):
        x = random.randint(1, max(1, self.grid_width - 4))
        y = random.randint(1, max(1, self.grid_height - 5))
        return (x, y)
