import os
import cv2
import time
import threading
import queue
from typing import Callable
from app.core import SessionQueue, Logger, DisplayManager
from app.domain import StateEvent, EventType

CAM_RETRY_DELAY = 5

class DisplayWorker:
    def __init__(self, window_name="Camera"):
        self.window_name = window_name
        self.frame_queue = queue.Queue(maxsize=1)
        self.running = False
        self.thread = None
        self.dm = None

    def start(self):
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    def _run(self):
        # cv2.namedWindow(self.window_name)
        self.dm = DisplayManager() 
        while self.running:
            cv2.imshow(self.window_name, self.frame_queue.get())
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()

    def show(self, frame):
        try:
            canvas = self.dm.render(frame)
            self.frame_queue.put_nowait(canvas)
        except queue.Full:
            pass

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)


class CameraMonitor:
    def __init__(self):
        self.running = False
        self.thread = None
        self.logger = Logger("Camera")
        self.cam = None
        self.cam_handle: Callable = None
        self.cam_connecting: Callable = None

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
            self.logger.debug('looping')
            self.__loop()
    ####################

    #################### Task Logic
    def stream_handle(self, callback: Callable): # when frame is valid
        self.cam_handle = callback

    def cam_connecting_handle(self, callback: Callable):
        self.cam_connecting = callback

    def __connect(self):
        rtsp = f"rtsp://{os.getenv('CAM_USERNAME')}:{os.getenv('CAM_PASSWORD')}@{os.getenv('CAM_IP')}:{os.getenv('CAM_PORT')}/Streaming/Channels/101"

        self.logger.info(rtsp)
        if self.cam:
            if not self.cam.isOpened():
                self.cam.release()
        self.cam = cv2.VideoCapture(rtsp)

    def __setup(self):
        self.__connect()
        
    def __loop(self):
        if not self.cam.isOpened():
            self.logger.info('Reconnecting...')
            if self.cam_connecting is not None:
                self.cam_connecting()
            time.sleep(CAM_RETRY_DELAY)
            self.__connect()
            return

        ret, frame = self.cam.read()
        if not ret:
            self.logger.warning('Disconnnected!')
            if self.cam_connecting is not None:
                self.cam_connecting()
            self.cam.release()
            time.sleep(CAM_RETRY_DELAY)
            self.__connect()
            return

        if self.cam_handle is not None:
            self.logger.info("sending frame")
            self.cam_handle(frame)
        
