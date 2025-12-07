import cv2
import mediapipe as mp
import numpy as np
from game.snake import Direction
from collections import deque
import time

class GestureDetector:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.hand_history = deque(maxlen=5)  # Track last 10 hand positions
        self.last_gesture_time = 0
        self.gesture_cooldown = 0.1  # Seconds between gesture detections

    def detect(self, frame):
        """
        Detect hand gestures from a video frame.
        Returns a Direction or None.
        """
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        
        gesture = None
        
        if results.multi_hand_landmarks:
            landmarks = results.multi_hand_landmarks[0]
            
            # Get hand landmarks
            hand_points = [(lm.x, lm.y, lm.z) for lm in landmarks.landmark]
            
            # Detect gesture based on thumb direction
            current_time = time.time()
            if current_time - self.last_gesture_time > self.gesture_cooldown:
                gesture = self._classify_gesture(hand_points)
                if gesture:
                    self.last_gesture_time = current_time
        else:
            self.hand_history.clear()
        
        return gesture, frame

    def _classify_gesture(self, landmarks):
        """
        Classify gesture based on thumb direction.
        landmarks: list of (x, y, z) tuples for 21 hand points
        """
        # Thumb points: 0=wrist, 1=CMC, 2=MCP, 3=IP, 4=thumb tip
        wrist = landmarks[0]
        thumb_tip = landmarks[4]
        
        # Vector from wrist to thumb tip
        dx = thumb_tip[0] - wrist[0]
        dy = thumb_tip[1] - wrist[1]
        
        # Calculate angle of thumb direction
        angle = np.arctan2(dy, dx)
        
        # Determine direction based on thumb angle
        # Up: -3pi/4 to -pi/4
        if -np.pi * 0.75 < angle < -np.pi * 0.25:
            return Direction.DOWN
        # Right: -pi/4 to pi/4
        elif -np.pi * 0.25 < angle < np.pi * 0.25:
            return Direction.LEFT
        # Down: pi/4 to 3pi/4
        elif np.pi * 0.25 < angle < np.pi * 0.75:
            return Direction.UP
        # Left: 3pi/4 to pi or -3pi/4 to -pi
        elif angle > np.pi * 0.75 or angle < -np.pi * 0.75:
            return Direction.RIGHT
        
        return None

    def draw_landmarks(self, frame, results):
        """Draw hand landmarks on frame for debugging."""
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
        return frame
