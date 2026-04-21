import cv2
import numpy as np
from app.domain import TextType

# Resolusi Canvas UI (Contoh: 1280x720)
UI_WIDTH = 1280
UI_HEIGHT = 720
FONT = cv2.FONT_HERSHEY_DUPLEX
CAM_W, CAM_H = 854, 480 
CAM_X = (UI_WIDTH - CAM_W) // 2
CAM_Y = 80
BOX_X = 40
BOX_Y = 590
BOX_W = UI_WIDTH - 80
BOX_H = 100
WINDOW_NAME = "Monitor Gate"

class DisplayManager:           # A singleton class
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
           cls._instance = super(DisplayManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if getattr(self, "_initialized", False):
            return
        
        self.current_text: TextType = TextType.UNDEFINED
        self.current_color = (0, 255, 0)
        
        cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
        cv2.setWindowProperty(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        self._initialized = True

    def set_text(self, text: TextType):
        self.current_text = text

    def set_color(self, color):
        self.current_color = color

    def render(self, frame=None):
        canvas = self.__header()
        
        if frame is not None:
            self.__camera_stream(canvas, frame)
        else:
            self.__camera_connecting(canvas)

        self.__write_text(canvas)
        
        cv2.imshow(WINDOW_NAME, canvas) # Render

    def __camera_stream(self, canvas, frame):
        resized_cam = cv2.resize(frame, (CAM_W, CAM_H))
        canvas[CAM_Y:CAM_Y+CAM_H, CAM_X:CAM_X+CAM_W] = resized_cam

        # Garis tepi (Border) putih untuk container kamera
        cv2.rectangle(canvas, (CAM_X-2, CAM_Y-2), (CAM_X+CAM_W+2, CAM_Y+CAM_H+2), (255, 255, 255), 3)
        return canvas
    
    def __camera_connecting(self, canvas):
        cv2.rectangle(canvas, (CAM_X, CAM_Y), (CAM_X+CAM_W, CAM_Y+CAM_H), (80, 80, 80), -1)
        cv2.putText(canvas, "MENGHUBUNGKAN KAMERA...", (CAM_X + 180, CAM_Y + 240), FONT, 1, (200, 200, 200), 2)

        # Garis tepi (Border) putih untuk container kamera
        cv2.rectangle(canvas, (CAM_X-2, CAM_Y-2), (CAM_X+CAM_W+2, CAM_Y+CAM_H+2), (255, 255, 255), 3)
        return canvas

    def __write_text(self, canvas):
        # Menghitung posisi teks agar persis di tengah (Center Alignment)
        text_size = cv2.getTextSize(self.current_text, FONT, 1.8, 3)[0]
        text_x = BOX_X + (BOX_W - text_size[0]) // 2
        text_y = BOX_Y + (BOX_H + text_size[1]) // 2

        # Efek bayangan hitam (Drop shadow) pada teks
        cv2.putText(canvas, self.current_text, (text_x+3, text_y+3), FONT, 1.8, (0, 0, 0), 4)
        # Menulis Teks Utama
        cv2.putText(canvas, self.current_text, (text_x, text_y), FONT, 1.8, self.current_color, 3)
            
    def __header(self):
        canvas = np.zeros((UI_HEIGHT, UI_WIDTH, 3), dtype=np.uint8)
        canvas[:] = (30, 30, 30) # Warna abu-abu gelap
        # Header Judul
        cv2.putText(canvas, "SISTEM GATE PARKIR", (40, 50), FONT, 1.2, (255, 255, 255), 2)
        return canvas
