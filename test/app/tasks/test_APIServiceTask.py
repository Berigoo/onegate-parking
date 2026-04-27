import pytest
from flask_socketio import SocketIOTestClient
from app.tasks import APIService
from app.core.SessionQueue import SessionQueue

@pytest.fixture
def api_service():
    queue = SessionQueue()
    service = APIService(queue)
    service._APIService__setup()  # call private setup manually
    return service, queue


@pytest.fixture
def client(api_service):
    service, _ = api_service
    return service.app.test_client()


@pytest.fixture
def socket_client(api_service):
    service, _ = api_service
    return service.socketio.test_client(service.app)


def test_register_start(client, api_service):
    service, queue = api_service
    service.running = True

    res = client.post("/register/start")
    data = res.get_json()

    assert res.status_code == 200
    assert "session_id" in data
    assert queue.qsize() == 1

def test_register_subscribe(socket_client, api_service):
    service, _ = api_service

    session_id = "test-session"

    socket_client.emit("register_subscribe", {
        "session_id": session_id
    })

    # check mapping stored
    assert session_id in service.register_sessions

def test_emit_uid(socket_client, api_service):
    service, _ = api_service

    session_id = "test-session"

    # subscribe first
    socket_client.emit("register_subscribe", {
        "session_id": session_id
    })

    # trigger emit
    service.emit_uid(session_id, "UID123")

    received = socket_client.get_received()

    assert len(received) > 0
    event = received[0]

    assert event["name"] == "register_result"
    assert event["args"][0]["uid"] == "UID123"

    # ensure cleanup
    assert session_id not in service.register_sessions

def test_emit_uid_timeout(socket_client, api_service):
    service, _ = api_service

    session_id = "test-session"

    socket_client.emit("register_subscribe", {
        "session_id": session_id
    })

    service.emit_uid("test-session", -1)
    received = socket_client.get_received()

    assert len(received) > 0
    event = received[0]
    assert event["name"] == "register_result"
    assert event["args"][0]["uid"] == -1
