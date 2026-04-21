import cv2
from app.tasks import VLDMonitor, CardValidatorIn, CardValidatorOut, IntercomRelayMonitor, CameraMonitor, GateController, TimerManager, DisplayWorker
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
        self.dw = None
        self.gate_ctrl = None
        self.timer_mgr = None
        self.events_queue = None
        self.sessions_queue = None
        self.current_state = None
        self.ctx = None
        self.dm = None

        # Initialize hardware interface if available. In test environments
        # or non-RPi setups, this call may fail; swallow exceptions to keep
        # unit tests deterministic while still allowing mocked components
        # to be exercised.
        try:
            bsp.bsp_init()
        except Exception:
            pass
        
    def __setup(self):
        # Initialization
        # self.events_queue = SessionQueue()
        # self.sessions_queue = SessionQueue() # may invalid
        # self.vld_monitor = VLDMonitor(self.events_queue)
        # self.card_validator_in = CardValidatorIn("/dev/ttyUSB0", "/etc/onegate-parking/cards.db", self.events_queue)
        # self.card_validator_out = CardValidatorOut("/dev/ttyUSB1", "/etc/onegate-parking/cards.db", self.events_queue)
        # self.intercom_relay = IntercomRelayMonitor(self.events_queue)
        # self.gate_ctrl = GateController()
        # self.timer_mgr = TimerManager(self.events_queue)
        
        # Start monitor services
        # self.vld_monitor.start()
        # self.card_validator_in.start()
        # self.card_validator_out.start()
        # self.intercom_relay.start()
        self.dw = DisplayWorker()
        self.dw.start()
        self.camera = CameraMonitor()
        self.camera.stream_handle(dw.show)
        self.camera.start()

        # # Assign callback video frame
        # self.camera.stream_handle(self.__handle_video_stream)
        # self.camera.cam_connecting_handle(self.__handle_cam_connecting)

        # Initialize state machine context
        # self.ctx = SystemStateContext("Idle", self.vld_monitor, self.card_validator_in, self.card_validator_out, self.intercom_relay, self.camera, self.gate_ctrl, self.timer_mgr, self.sessions_queue, self.dm)
        
    def __loop(self):
        # ev = self.events_queue.get()
        # self.ctx.do(ev)
        True

    # def __handle_video_stream(self, frame):
    #     self.dm.render(frame)

    #     if cv2.waitKey(1) & 0xFF == ord('q'):
    #         self.cam.release()
    #         cv2.destroyAllWindows() # TODO gracefull exit
    #         return

    # def __handle_cam_connecting(self):
    #     self.dm.render(None)

    #     # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     #     self.cam.release()
    #     #     cv2.destroyAllWindows() # TODO gracefull exit
    #     #     return
        
    def start(self):
        self.is_running = True
        self.__setup()
        while self.is_running:
            self.__loop()
        
        
