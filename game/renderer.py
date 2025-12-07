import pygame

class Renderer:
    def __init__(self, window_width, window_height, grid_size):
        self.window_width = window_width
        self.window_height = window_height
        self.grid_size = grid_size
        self.screen = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption("Snake Game")
        
        # Padding and layout constants
        self.padding = 15
        self.game_area_x = self.padding
        self.game_area_y = self.padding + 50

    def render(self, game_engine, show_menu=False, selected_menu_option=0, game_over_option=0):
        self.screen.fill((10, 10, 15))
        
        if show_menu:
            self._draw_menu(selected_menu_option)
        else:
            # Draw game area background with gradient effect
            game_area_width = self.window_width - 2 * self.padding
            game_area_height = self.window_height - self.game_area_y - self.padding
            game_area_rect = pygame.Rect(self.game_area_x, self.game_area_y, game_area_width, game_area_height)
            pygame.draw.rect(self.screen, (15, 15, 20), game_area_rect)
            pygame.draw.rect(self.screen, (80, 200, 100), game_area_rect, 3)
            
            # Draw grid background
            for x in range(0, game_area_width, self.grid_size):
                pygame.draw.line(self.screen, (30, 30, 40), 
                    (self.game_area_x + x, self.game_area_y),
                    (self.game_area_x + x, self.game_area_y + game_area_height), 1)
            for y in range(0, game_area_height, self.grid_size):
                pygame.draw.line(self.screen, (30, 30, 40),
                    (self.game_area_x, self.game_area_y + y),
                    (self.game_area_x + game_area_width, self.game_area_y + y), 1)
            
            # Draw snake
            for i, segment in enumerate(game_engine.snake.body):
                rect = pygame.Rect(
                    self.game_area_x + segment[0] * self.grid_size + 1,
                    self.game_area_y + segment[1] * self.grid_size + 1,
                    self.grid_size - 2,
                    self.grid_size - 2
                )
                # Head is brighter
                if i == 0:
                    pygame.draw.rect(self.screen, game_engine.snake_color, rect)
                    pygame.draw.rect(self.screen, (100, 255, 100), rect, 2)
                else:
                    color = tuple(int(c * 0.7) for c in game_engine.snake_color)
                    pygame.draw.rect(self.screen, color, rect)
            
            # Draw food with animation effect
            food_rect = pygame.Rect(
                self.game_area_x + game_engine.food.position[0] * self.grid_size + 2,
                self.game_area_y + game_engine.food.position[1] * self.grid_size + 2,
                self.grid_size - 4,
                self.grid_size - 4
            )
            pygame.draw.rect(self.screen, game_engine.food_color, food_rect)
            pygame.draw.rect(self.screen, (255, 150, 0), food_rect, 2)
            
            # Draw score and info at top
            self._draw_score_bar(game_engine)
            
            # Draw game over message centered
            if game_engine.game_over:
                self._draw_game_over_screen(game_over_option)
        
        pygame.display.flip()

    def _draw_score_bar(self, game_engine):
        """Draw score and game info bar."""
        bar_height = 45
        bar_rect = pygame.Rect(0, 0, self.window_width, bar_height)
        pygame.draw.rect(self.screen, (20, 20, 30), bar_rect)
        pygame.draw.line(self.screen, (80, 200, 100), (0, bar_height), (self.window_width, bar_height), 2)
        
        # Score
        score_font = pygame.font.Font(None, 32)
        score_text = score_font.render(f"SCORE: {game_engine.score}", True, (80, 200, 100))
        self.screen.blit(score_text, (self.padding + 10, 7))
        
        # Snake length
        length_font = pygame.font.Font(None, 28)
        length_text = length_font.render(f"Length: {len(game_engine.snake.body)}", True, (200, 200, 100))
        self.screen.blit(length_text, (self.window_width - 200, 10))

    def _draw_menu(self, selected_option):
        """Draw main menu screen."""
        # Title
        title_font = pygame.font.Font(None, 80)
        title_text = title_font.render("SNAKE", True, (80, 200, 100))
        title_rect = title_text.get_rect(center=(self.window_width // 2, self.window_height // 2 - 180))
        self.screen.blit(title_text, title_rect)
        
        subtitle_font = pygame.font.Font(None, 36)
        subtitle_text = subtitle_font.render("GESTURE CONTROL", True, (200, 200, 100))
        subtitle_rect = subtitle_text.get_rect(center=(self.window_width // 2, self.window_height // 2 - 110))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Menu options
        options = ["Start Game", "Skins"]
        menu_font = pygame.font.Font(None, 50)
        
        for i, option in enumerate(options):
            color = (255, 255, 0) if i == selected_option else (200, 200, 200)
            option_text = menu_font.render(option, True, color)
            option_rect = option_text.get_rect(center=(self.window_width // 2, self.window_height // 2 + 30 + i * 80))
            
            # Highlight box for selected option
            if i == selected_option:
                box_rect = option_rect.inflate(40, 20)
                pygame.draw.rect(self.screen, (80, 200, 100), box_rect, 3)
            
            self.screen.blit(option_text, option_rect)
        
        # Instructions
        inst_font = pygame.font.Font(None, 24)
        inst_text = inst_font.render("Use UP/DOWN to navigate, ENTER to select", True, (150, 150, 150))
        inst_rect = inst_text.get_rect(center=(self.window_width // 2, self.window_height - 50))
        self.screen.blit(inst_text, inst_rect)

    def _draw_skins_menu(self, selected_skin):
        """Draw skins selection screen."""
        # Title
        title_font = pygame.font.Font(None, 60)
        title_text = title_font.render("SELECT SKIN", True, (80, 200, 100))
        title_rect = title_text.get_rect(center=(self.window_width // 2, self.window_height // 2 - 150))
        self.screen.blit(title_text, title_rect)
        
        # Skin options with color preview
        skins = ["Classic", "Neon", "Retro"]
        skin_colors = [(0, 255, 0), (0, 255, 255), (255, 255, 0)]
        skin_font = pygame.font.Font(None, 48)
        
        for i, (skin, color) in enumerate(zip(skins, skin_colors)):
            text_color = (255, 255, 0) if i == selected_skin else (200, 200, 200)
            skin_text = skin_font.render(skin, True, text_color)
            skin_rect = skin_text.get_rect(center=(self.window_width // 2 + 100, self.window_height // 2 + i * 70))
            
            # Color preview box
            preview_rect = pygame.Rect(self.window_width // 2 - 150, self.window_height // 2 - 10 + i * 70, 80, 50)
            pygame.draw.rect(self.screen, color, preview_rect)
            pygame.draw.rect(self.screen, (200, 200, 200), preview_rect, 2)
            
            # Highlight box for selected skin
            if i == selected_skin:
                box_rect = skin_rect.inflate(40, 20)
                pygame.draw.rect(self.screen, (80, 200, 100), box_rect, 3)
            
            self.screen.blit(skin_text, skin_rect)
        
        # Back instruction
        back_font = pygame.font.Font(None, 32)
        back_text = back_font.render("Press ESC to go back", True, (150, 150, 150))
        back_rect = back_text.get_rect(center=(self.window_width // 2, self.window_height - 50))
        self.screen.blit(back_text, back_rect)

    def render_skins_menu(self, selected_skin):
        """Render skins menu."""
        self.screen.fill((10, 10, 15))
        self._draw_skins_menu(selected_skin)
        pygame.display.flip()

    def _draw_game_over_screen(self, selected_option=0):
        """Draw centered game over screen with menu options."""
        # Semi-transparent overlay
        overlay = pygame.Surface((self.window_width, self.window_height))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Game over title
        game_over_font = pygame.font.Font(None, 80)
        game_over_text = game_over_font.render("GAME OVER", True, (255, 100, 100))
        game_over_rect = game_over_text.get_rect(center=(self.window_width // 2, self.window_height // 2 - 140))
        self.screen.blit(game_over_text, game_over_rect)
        
        # Game over options
        options = ["Restart", "Main Menu"]
        option_font = pygame.font.Font(None, 44)
        
        for i, option in enumerate(options):
            color = (255, 255, 0) if i == selected_option else (200, 200, 200)
            option_text = option_font.render(option, True, color)
            option_rect = option_text.get_rect(center=(self.window_width // 2, self.window_height // 2 - 20 + i * 80))
            
            # Highlight box for selected option
            if i == selected_option:
                box_rect = option_rect.inflate(40, 20)
                pygame.draw.rect(self.screen, (80, 200, 100), box_rect, 3)
            
            self.screen.blit(option_text, option_rect)
