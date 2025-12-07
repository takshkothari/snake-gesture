# Snake Game - Gesture Control

A modern Snake game with hand gesture control using computer vision. Control the snake by pointing your thumb in the direction you want to move!

## Features

- 🎮 **Gesture Control**: Control the snake using your thumb direction via webcam
- 🎨 **Multiple Skins**: Choose from Classic, Neon, and Retro color schemes
- 🎯 **Score Tracking**: Real-time score and snake length display
- 🎪 **Interactive Menus**: User-friendly navigation with keyboard controls
- ⌨️ **Keyboard Support**: Optional keyboard controls alongside gestures
- 🔄 **Reversible Controls**: Toggle reversed gesture direction in settings

## Project Structure

```
snake-gesture/
├── game/
│   ├── snake.py           # Snake and Food classes
│   ├── game_engine.py     # Game logic and state management
│   └── renderer.py        # Pygame rendering and UI
├── ml/
│   └── gesture_detector.py # Hand gesture detection using MediaPipe
├── app.py                 # Main application entry point
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Installation

### Prerequisites
- Python 3.8 or higher
- Webcam

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/snake-gesture.git
cd snake-gesture
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the game:
```bash
python app.py
```

## Controls

### Gesture Control
- **Thumb pointing up**: Move snake up
- **Thumb pointing right**: Move snake right
- **Thumb pointing down**: Move snake down
- **Thumb pointing left**: Move snake left

### Keyboard Controls
- **Arrow Keys**: Move snake (when gesture detection is not active)
- **UP/DOWN**: Navigate menus
- **ENTER**: Select menu options
- **ESC**: Go back/Quit

## Game Rules

- Eat red food squares to grow and gain points
- Avoid hitting walls and yourself
- Each food eaten gives 10 points
- Game ends on collision

## Menu Options

### Main Menu
- **Start Game**: Begin playing
- **Skins**: Select color scheme

### Skins
- **Classic**: Green snake, red food
- **Neon**: Cyan snake, magenta food
- **Retro**: Yellow snake, orange food

## Configuration

Edit `app.py` to customize:
- `FPS`: Game speed (default: 7)
- `REVERSE_GESTURE`: Toggle reversed controls (default: True)

## Technologies Used

- **Pygame**: Game engine and rendering
- **MediaPipe**: Hand gesture detection
- **OpenCV**: Webcam video processing
- **NumPy**: Mathematical calculations

## Future Enhancements

- [ ] Difficulty levels
- [ ] High score leaderboard
- [ ] Sound effects and music
- [ ] More skin options
- [ ] Mobile support
- [ ] Multiplayer mode

## Troubleshooting

### Webcam not detected
- Check webcam permissions
- Ensure webcam is not in use by another application

### Poor gesture detection
- Ensure adequate lighting
- Keep hand clearly visible to camera
- Adjust confidence thresholds in `gesture_detector.py`

### Game lag
- Reduce `FPS` value in `app.py`
- Close other resource-intensive applications

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Author

Created by Taksh

## Contributing

Contributions are welcome! Feel free to submit issues and pull requests.
