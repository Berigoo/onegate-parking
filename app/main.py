import cv2
from app.tasks import VLDMonitor, CardValidatorIn, CardValidatorOut, IntercomRelayMonitor, CameraMonitor, GateController, TimerManager, DisplayWorker
from app.core import SessionQueue, SystemStateContext, DisplayManager
from app.states import Idle
from bsp import bsp
from app.domain import TextType

class Application:
    def __init__(self):
        self.is_running = False
        self.vld_monitor = None
        self.card_validator_in = None
        self.card_validator_out = None
        self.intercom_relay = None
        self.camera = None
        self.dw = None
        self.gate_ctrl = None
        self.timer_mgr = None
        self.events_queue = None
        self.sessions_queue = None
        self.current_state = None
        self.ctx = None
        self.dm = None

        bsp.bsp_init()
        
    def __setup(self):
        # Initialization
        self.events_queue = SessionQueue()
        self.sessions_queue = SessionQueue() # may invalid
        self.vld_monitor = VLDMonitor(self.events_queue)
        # self.card_validator_in = CardValidatorIn("/dev/ttyUSB0", "/etc/onegate-parking/cards.db", self.events_queue)
        # self.card_validator_out = CardValidatorOut("/dev/ttyUSB1", "/etc/onegate-parking/cards.db", self.events_queue)
        self.intercom_relay = IntercomRelayMonitor(self.events_queue)
        self.gate_ctrl = GateController()
        self.timer_mgr = TimerManager(self.events_queue)
        self.dm = DisplayManager()
        
        # Start monitor services
        self.vld_monitor.start()
        # self.card_validator_in.start()
        # self.card_validator_out.start()
        self.intercom_relay.start()

        # Camera workers and manager
        self.dw = DisplayWorker()
        self.dw.start()
        self.camera = CameraMonitor()
        self.camera.stream_handle(self.dw.show)
        self.camera.cam_connecting_handle(self.dw.show)
        self.camera.start()
        self.dm.set_text(TextType.WELCOME)

        # Initialize state machine context
        # self.ctx = SystemStateContext("Idle", self.vld_monitor, self.card_validator_in, self.card_validator_out, self.intercom_relay, self.camera, self.gate_ctrl, self.timer_mgr, self.sessions_queue, self.dm)
        
    def __loop(self):
        # ev = self.events_queue.get()
        # self.ctx.do(ev)
        True

    def start(self):
        self.is_running = True
        self.__setup()
        while self.is_running:
            self.__loop()
        
        
