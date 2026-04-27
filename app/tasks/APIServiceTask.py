import uuid
from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
import threading
from typing import Callable
from app.core import SessionQueue, Logger, DisplayManager
from app.domain import StateEvent, EventType

class APIService:
    def __init__(self, queue_to_push: SessionQueue):
        self.app = Flask(__name__)
        self.socketio = SocketIO(self.app, cors_allowed_origins=["http://127.0.0.1:8000"])
        self.queue = queue_to_push
        self.register_sessions = {}
        self.running = False
        self.thread = None
        self.logger = Logger("APIService")

    #################### threading methods
    def start(self):
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()
    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=5) # TODO stop flask
    def _run(self):
        self.__setup()
        self.socketio.run(self.app, host=_HOST, port=_PORT)
    ####################
    def __setup(self):
        self._setup_routes()
        self._setup_ws()

    def __loop(self):
        pass

    def _setup_routes(self):
        @self.app.route("/")
        def home():
            if self.running:
                return "System is running...", 200
            else:
                return "System is down", 500

        @self.app.route("/register/start", methods=['POST'])
        def register():
            if self.running:
                session_id = str(uuid.uuid4())
                event = StateEvent(
                    type=EventType.CARD_REGISTER,
                    payload={
                        "session_id": session_id
                    }
                )
                self.queue.put(event)
                return {"session_id": session_id}, 200
            else:
                return {"error": "system not running"}, 500

    def _setup_ws(self):
        @self.socketio.on('connect')
        def handle_connect():
            self.logger.debug("ws client connected")

        @self.socketio.on('register_subscribe')
        def handle_register_subscribe(data):
            session_id = data.get('session_id')
            if session_id:
                self.register_sessions[session_id] = request.sid

        @self.socketio.on('disconnect')
        def handle_disconnect():
            self.logger.debug("ws client disconnected")

    def emit_uid(self, session_id, uid):
        sid = self.register_sessions.get(session_id)
        if sid:                 # timeout will return -1
            self.socketio.emit(
                "register_result",
                {"session_id": session_id, "uid": uid},
                to=sid
            )
            del self.register_sessions[session_id]
