import cv2
from app.domain import TextType

# Resolusi Canvas UI (Contoh: 1280x720)
UI_WIDTH = 1280
UI_HEIGHT = 720
FONT = cv2.FONT_HERSHEY_DUPLEX
CAM_W, CAM_H = 854, 480 
CAM_X = (UI_WIDTH - cam_w) // 2
CAM_Y = 80
WINDOW_NAME = "Monitor Gate"

class DisplayManager:
    def __init__(self):
        self.current_text: TextType = TextType.UNDEFINED
        
        cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
        cv2.setWindowProperty(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    def set_text(self, canvas, text: TextType):
        self.current_text = text

    def render(self, frame=None):
        canvas = self.__header()
        
        if frame:
            self.__camera_stream(canvas, frame)
        else:
            self.__camera_connecting(canvas)

        self.__write_text()
        
        cv2.imshow(WINDOW_NAME, canvas) # Render

    def __camera_stream(self, canvas, frame):
        resized_cam = cv2.resize(latest_frame, (CAM_W, CAM_H))
        canvas[CAM_Y:CAM_Y+CAM_H, CAM_X:CAM_X+CAM_W] = resized_cam

        # Garis tepi (Border) putih untuk container kamera
        cv2.rectangle(canvas, (cam_x-2, cam_y-2), (cam_x+cam_w+2, cam_y+cam_h+2), (255, 255, 255), 3)
        return canvas
    
    def __camera_connecting(self, canvas):
        cv2.rectangle(canvas, (cam_x, cam_y), (cam_x+cam_w, cam_y+cam_h), (80, 80, 80), -1)
        cv2.putText(canvas, "MENGHUBUNGKAN KAMERA...", (cam_x + 180, cam_y + 240), font, 1, (200, 200, 200), 2)
        cv2.imshow(WINDOW_NAME, canvas)

        # Garis tepi (Border) putih untuk container kamera
        cv2.rectangle(canvas, (cam_x-2, cam_y-2), (cam_x+cam_w+2, cam_y+cam_h+2), (255, 255, 255), 3)
        return canvas

    def __write_text(self):
        # Menghitung posisi teks agar persis di tengah (Center Alignment)
        text_size = cv2.getTextSize(self.current_text, FONT, 1.8, 3)[0]
        text_x = box_x + (box_w - text_size[0]) // 2
        text_y = box_y + (box_h + text_size[1]) // 2

        # Efek bayangan hitam (Drop shadow) pada teks
        cv2.putText(canvas, self.current_text, (text_x+3, text_y+3), FONT, 1.8, (0, 0, 0), 4)
        # Menulis Teks Utama
        cv2.putText(canvas, self.current_text, (text_x, text_y), FONT, 1.8, color, 3)
            
    def __header(self):
        canvas = np.zeros((UI_HEIGHT, UI_WIDTH, 3), dtype=np.uint8)
        canvas[:] = (30, 30, 30) # Warna abu-abu gelap
        # Header Judul
        cv2.putText(canvas, "SISTEM GATE PARKIR", (40, 50), FONT, 1.2, (255, 255, 255), 2)
        return canvas

DM = DisplayManager()
