import pygame
from game.snake import Snake, Food, Direction

class GameEngine:
    def __init__(self, grid_width, grid_height, reverse_gesture_direction=False):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.snake = Snake(grid_width, grid_height)
        self.food = Food(grid_width, grid_height)
        self.score = 0
        self.game_over = False
        self.reverse_gesture_direction = reverse_gesture_direction
        
        # Skin options
        self.snake_color = (0, 255, 0)  # Default green
        self.food_color = (255, 0, 0)   # Default red
        self.skins = {
            'classic': {'snake': (0, 255, 0), 'food': (255, 0, 0)},
            'neon': {'snake': (0, 255, 255), 'food': (255, 0, 255)},
            'retro': {'snake': (255, 255, 0), 'food': (255, 165, 0)},
        }
        self.current_skin = 'classic'
        self._apply_skin('classic')

    def _apply_skin(self, skin_name):
        """Apply color scheme based on selected skin."""
        if skin_name in self.skins:
            self.current_skin = skin_name
            self.snake_color = self.skins[skin_name]['snake']
            self.food_color = self.skins[skin_name]['food']

    def handle_input(self, keys):
        if keys[pygame.K_UP] and self.snake.direction != Direction.DOWN:
            self.snake.next_direction = Direction.UP
        elif keys[pygame.K_DOWN] and self.snake.direction != Direction.UP:
            self.snake.next_direction = Direction.DOWN
        elif keys[pygame.K_LEFT] and self.snake.direction != Direction.RIGHT:
            self.snake.next_direction = Direction.LEFT
        elif keys[pygame.K_RIGHT] and self.snake.direction != Direction.LEFT:
            self.snake.next_direction = Direction.RIGHT

    def handle_gesture(self, gesture):
        """Handle gesture input from gesture detector."""
        # Reverse direction if enabled
        if self.reverse_gesture_direction:
            gesture = self._reverse_direction(gesture)
        
        if isinstance(gesture, Direction):
            if gesture == Direction.UP and self.snake.direction != Direction.DOWN:
                self.snake.next_direction = Direction.UP
            elif gesture == Direction.DOWN and self.snake.direction != Direction.UP:
                self.snake.next_direction = Direction.DOWN
            elif gesture == Direction.LEFT and self.snake.direction != Direction.RIGHT:
                self.snake.next_direction = Direction.LEFT
            elif gesture == Direction.RIGHT and self.snake.direction != Direction.LEFT:
                self.snake.next_direction = Direction.RIGHT

    def _reverse_direction(self, direction):
        """Reverse the direction for opposite control."""
        reverse_map = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT
        }
        return reverse_map.get(direction, direction)

    def update(self):
        if not self.game_over:
            # Check if next move would go out of bounds
            dx, dy = self.snake.next_direction.value
            head_x, head_y = self.snake.body[0]
            next_head = (head_x + dx, head_y + dy)
            
            # Game over if moving outside bounds
            if (next_head[0] < 0 or next_head[0] >= self.grid_width - 1 or
                next_head[1] < 0 or next_head[1] >= self.grid_height - 4):
                self.game_over = True
                return
            
            self.snake.next_direction = self.snake.next_direction
            self.snake.move()
            
            # Check food collision
            if self.snake.body[0] == self.food.position:
                self.score += 10
                self.food.position = self.food.spawn()
            else:
                self.snake.body.pop()
            
            # Check self-collision
            if self.snake.body[0] in self.snake.body[1:]:
                self.game_over = True

    def reset_game(self):
        self.snake = Snake(self.grid_width, self.grid_height)
        self.food = Food(self.grid_width, self.grid_height)
        self.score = 0
        self.game_over = False
