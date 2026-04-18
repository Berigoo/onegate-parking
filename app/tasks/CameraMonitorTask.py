import os
import cv2
import time
import threading
from typing import Callable
from app.core import SessionQueue, Logger
from app.domain import StateEvent, EventType

CAM_RETRY_DELAY = 5

class CameraMonitor:
    def __init__(self):
        self.running = False
        self.thread = None
        self.logger = Logger("Camera")
        self.cam = None
        self.cam_handle: Callable = None
        self.generic_handle: Callable = None

    #################### threading methods
    def start(self):
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()
    def stop(self):
        self.running = False
        if self.cam:
            self.cam.release()
        if self.thread:
            self.thread.join(timeout=5)
    def _run(self):
        self.__setup()
        while self.running:
            self.__loop()
    ####################

    #################### Task Logic
    def stream_handle(self, callback: Callable): # when frame is valid
        self.cam_handle = callback

    def cam_connecting_handle(self, callback: Callable):
        self.cam_connecting = callback

    def __connect(self):
        rtsp = f"rtsp://{os.getenv('CAM_USERNAME')}:{os.getenv('CAM_PASSWORD')}@{os.getenv('CAM_IP')}:{os.getenv('CAM_PORT')}/Streaming/Channels/101"

        if self.cam:
            if not self.cam.isOpened():
                self.cam.release()
        self.cam = cv2.VideoCapture(rtsp)

    def __setup(self):
        self.__connect()
        
    def __loop(self):
        if not self.cam.isOpened():
            self.logger.info('Reconnecting...')
            time.sleep(CAM_RETRY_DELAY)
            self.__connect()
            if self.cam_handle is not None:
                self.cam_connecting()
            return

        ret, frame = self.cam.read()
        if not ret:
            self.logger.warning('Disconnnected!')
            self.cam.release()
            time.sleep(CAM_RETRY_DELAY)
            self.__connect()
            if self.cam_handle is not None:
                self.cam_connecting()
            return

        if self.cam_handle is not None:
            self.cam_handle(frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            self.cam.release()
            cv2.destroyAllWindows() # TODO gracefull exit
            return
            

        
