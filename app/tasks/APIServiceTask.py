import uuid
import os
from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
import threading
from typing import Callable
from app.core import SessionQueue, Logger, DisplayManager
from app.domain import StateEvent, EventType
import requests

_HOST = "0.0.0.0"
_PORT = 8080

SERVER_IP = os.getenv("SERVER_IP", "127.0.0.1")
SERVER_PORT = os.getenv("SERVER_PORT", "8000")
API_BASE_URL = f"https://{SERVER_IP}:{SERVER_PORT}/api/card"
TOKEN = os.getenv("SERVER_TOKEN_ACCESS")

class APIService:
    def __init__(self, queue_to_push: SessionQueue):
        self.app = Flask(__name__)
        self.socketio = SocketIO(self.app, cors_allowed_origins=["*"])
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
        @self.app.route("/api/card-out-tap", methods=['POST'])
        def card_out_tap():
            event = StateEvent(
                type=EventType.CARD_OUT_TAP,
                payload=None
            )
            self.queue.put(event)
            return {"success": True}, 200
        @self.app.route("/api/card-out-valid", methods=['POST'])
        def card_out_valid():
            data = request.json
            obj = {
                "uid": data["uid"],
                "number": data["uid"],
                "name": data["name"]
                "is_valid": True,
            }
            event = StateEvent(
                type=EventType.CARD_OUT_VALID,
                payload=obj
            )
            self.queue.put(event)

            entry_id = data["uid"]

            response = requests.delete(
                f"http://localhost:8000/api/active-entries/{entry_id}",
                headers=headers,
                timeout=5
            )
            
            return {"success": True}, 200

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
