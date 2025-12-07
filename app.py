import pygame
import cv2
from game.game_engine import GameEngine
from game.renderer import Renderer
from ml.gesture_detector import GestureDetector

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE
FPS = 5

def main():
    pygame.init()
    
    # Set to True to reverse gesture direction
    REVERSE_GESTURE = True
    
    game_engine = GameEngine(GRID_WIDTH, GRID_HEIGHT, reverse_gesture_direction=REVERSE_GESTURE)
    renderer = Renderer(WINDOW_WIDTH, WINDOW_HEIGHT, GRID_SIZE)
    gesture_detector = GestureDetector()
    
    # Open webcam for gesture detection
    cap = cv2.VideoCapture(0)
    
    clock = pygame.time.Clock()
    running = True
    in_menu = True
    in_skins_menu = False
    selected_menu_option = 0
    selected_skin = 0
    game_over_option = 0
    
    while running:
        ret, frame = cap.read()
        
        if ret:
            gesture, frame = gesture_detector.detect(frame)
            if gesture and not in_menu and not in_skins_menu and not game_engine.game_over:
                game_engine.handle_gesture(gesture)
            
            cv2.imshow('Gesture Detection', frame)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if in_skins_menu:
                    if event.key == pygame.K_UP:
                        selected_skin = (selected_skin - 1) % 3
                    elif event.key == pygame.K_DOWN:
                        selected_skin = (selected_skin + 1) % 3
                    elif event.key == pygame.K_RETURN:
                        skins_list = ['classic', 'neon', 'retro']
                        game_engine._apply_skin(skins_list[selected_skin])
                        in_skins_menu = False
                    elif event.key == pygame.K_ESCAPE:
                        in_skins_menu = False
                elif game_engine.game_over:
                    if event.key == pygame.K_UP:
                        game_over_option = (game_over_option - 1) % 2
                    elif event.key == pygame.K_DOWN:
                        game_over_option = (game_over_option + 1) % 2
                    elif event.key == pygame.K_RETURN:
                        if game_over_option == 0:
                            game_engine.reset_game()
                            game_over_option = 0
                        elif game_over_option == 1:
                            in_menu = True
                            game_over_option = 0
                elif in_menu:
                    if event.key == pygame.K_UP:
                        selected_menu_option = (selected_menu_option - 1) % 2
                    elif event.key == pygame.K_DOWN:
                        selected_menu_option = (selected_menu_option + 1) % 2
                    elif event.key == pygame.K_RETURN:
                        if selected_menu_option == 0:
                            in_menu = False
                            game_engine.reset_game()
                        elif selected_menu_option == 1:
                            in_skins_menu = True
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                else:
                    if event.key == pygame.K_ESCAPE:
                        in_menu = True
        
        keys = pygame.key.get_pressed()
        if not in_menu and not in_skins_menu and not game_engine.game_over:
            game_engine.handle_input(keys)
            game_engine.update()
        
        if in_skins_menu:
            renderer.render_skins_menu(selected_skin)
        else:
            renderer.render(game_engine, show_menu=in_menu, selected_menu_option=selected_menu_option, game_over_option=game_over_option)
        
        # Close webcam window if it's closed
        if cv2.getWindowProperty('Gesture Detection', cv2.WND_PROP_VISIBLE) < 1:
            running = False
        
        clock.tick(FPS)
    
    cap.release()
    cv2.destroyAllWindows()
    pygame.quit()

if __name__ == "__main__":
    main()
