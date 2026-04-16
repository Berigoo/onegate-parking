import cv2
from app.tasks import VLDMonitor, CardValidatorIn, CardValidatorOut, IntercomRelayMonitor, CameraMonitor, GateController, TimerManager
from app.core import SessionQueue, SystemStateContext
from app.states import Idle
from bsp import bsp

class Application:
    def __init__(self):
        self.is_running = False
        self.vld_monitor = None
        self.card_validator_in = None
        self.card_validator_out = None
        self.intercom_relay = None
        self.camera = None
        self.gate_ctrl = None
        self.timer_mgr = None
        self.session_queue = None
        self.current_state = None
        self.ctx = None

        bsp.bsp_init()
        
    def __setup(self):
        # Initialization
        self.session_queue = SessionQueue()
        self.vld_monitor = VLDMonitor(self.session_queue)
        self.card_validator_in = CardValidatorIn("/dev/ttyUSB0", "/etc/onegate-parking/cards.db", self.session_queue)
        self.card_validator_out = CardValidatorOut("/dev/ttyUSB1", "/etc/onegate-parking/cards.db", self.session_queue)
        self.intercom_relay = IntercomRelayMonitor(self.session_queue)
        self.camera = CameraMonitor()
        self.gate_ctrl = GateController()
        self.timer_mgr = TimerManager(self.session_queue)

        # Start monitor services
        self.vld_monitor.start()
        self.card_validator_in.start()
        self.card_validator_out.start()
        self.intercom_relay.start()
        self.camera.start()

        # Assign callback video frame
        self.camera.stream_handle(self.__handle_video_stream)

        # Initialize state machine context
        self.ctx = SystemStateContext("Idle", self.vld_monitor, self.card_validator_in, self.card_validator_out, self.intercom_relay, self.camera, self.gate_ctrl, self.timer_mgr)
        
    def __loop(self):
        ev = self.session_queue.get()
        self.ctx.do(ev)

    def __handle_video_stream(self, frame):
        cv2.imshow("In Intercom Camera", frame)
        
    def start(self):
        self.is_running = True
        self.__setup()
        while self.is_running:
            self.__loop()
        
        

