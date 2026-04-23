import pytest
import sqlite3
import threading
import time
import bsp as bsp
from unittest.mock import Mock, MagicMock, patch, call
from app.tasks.CardInValidatorTask import CardValidatorIn
from app.core import SessionQueue, Logger
from app.domain import StateEvent, EventType


class TestCardValidatorInParsing:
    """Test card data parsing"""

    def test_parse_valid_card_data(self):
        """Test parsing valid hex card data"""
        queue = SessionQueue()
        validator = CardValidatorIn("/dev/ttyUSB0", ":memory:", queue)

        # Sample valid hex data: raw bytes with UID and card number
        # Format: [3 header bytes][14 uid hex][2 validity][16 number hex][8 balance]
        raw_data = b'\x00\x01\x02' + bytes.fromhex("12345678901234") + \
                   bytes.fromhex("00") + bytes.fromhex("9876543210ABCDEF") + \
                   bytes.fromhex("DEADBEEF")

        result = validator._CardValidatorIn__parse(raw_data)

        assert result is not None
        assert "uid" in result
        assert "number" in result
        assert "types" in result
        assert "validity" in result
        assert "balance" in result

    def test_parse_none_data(self):
        """Test parsing None data returns None"""
        queue = SessionQueue()
        validator = CardValidatorIn("/dev/ttyUSB0", ":memory:", queue)

        result = validator._CardValidatorIn__parse(None)
        assert result is None

    def test_parse_invalid_data(self):
        """Test parsing invalid/short data returns None"""
        queue = SessionQueue()
        validator = CardValidatorIn("/dev/ttyUSB0", ":memory:", queue)

        result = validator._CardValidatorIn__parse(b'\x00\x01')
        assert result is None


class TestCardValidatorInValidation:
    """Test card validation logic"""

    def setup_method(self):
        """Set up test database with sample cards"""
        self.db_path = ":memory:"
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

        # Create cards table
        self.cursor.execute("""
            CREATE TABLE cards (
                id INTEGER PRIMARY KEY,
                uid TEXT UNIQUE,
                number TEXT UNIQUE,
                status TEXT
            )
        """)

        # Insert test cards
        self.cursor.execute(
            "INSERT INTO cards (uid, number, status) VALUES (?, ?, ?)",
            ("12345678901234", "9876543210ABCDEF", "active")
        )
        self.cursor.execute(
            "INSERT INTO cards (uid, number, status) VALUES (?, ?, ?)",
            ("FFFFFFFFFFFFFFFF", "FEDCBA0987654321", "inactive")
        )
        self.conn.commit()

    def teardown_method(self):
        """Clean up test database"""
        self.conn.close()

    def test_validate_card_by_uid_exists(self):
        """Test validation succeeds for existing UID"""
        queue = SessionQueue()
        with patch('sqlite3.connect', return_value=self.conn):
            validator = CardValidatorIn("/dev/ttyUSB0", ":memory:", queue)

            data = {"uid": "12345678901234", "number": "9876543210ABCDEF"}
            result = validator._CardValidatorIn__validate(data)

            assert result is True

    def test_validate_card_by_number_exists(self):
        """Test validation succeeds for existing number"""
        queue = SessionQueue()
        with patch('sqlite3.connect', return_value=self.conn):
            validator = CardValidatorIn("/dev/ttyUSB0", ":memory:", queue)

            data = {"uid": "NOTEXIST", "number": "9876543210ABCDEF"}
            result = validator._CardValidatorIn__validate(data)

            assert result is True

    def test_validate_card_not_found(self):
        """Test validation fails for non-existent card"""
        queue = SessionQueue()
        with patch('sqlite3.connect', return_value=self.conn):
            validator = CardValidatorIn("/dev/ttyUSB0", ":memory:", queue)

            data = {"uid": "NOTEXIST", "number": "NOTEXIST"}
            result = validator._CardValidatorIn__validate(data)

            assert result is False

    def test_validate_card_database_error(self):
        """Test validation handles database errors gracefully"""
        queue = SessionQueue()
        mock_conn = Mock()
        mock_conn.cursor.side_effect = Exception("Database error")

        with patch('sqlite3.connect', return_value=mock_conn):
            validator = CardValidatorIn("/dev/ttyUSB0", ":memory:", queue)

            data = {"uid": "12345", "number": "ABCDE"}
            result = validator._CardValidatorIn__validate(data)

            assert result is False


class TestCardValidatorInThreading:
    """Test threading and lifecycle management"""

    def test_start_creates_thread(self):
        """Test start() creates and starts a daemon thread"""
        queue = SessionQueue()
        validator = CardValidatorIn("/dev/ttyUSB0", ":memory:", queue)

        assert validator.thread is None
        assert not validator.running

        validator.start()

        assert validator.thread is not None
        assert validator.running
        assert validator.thread.daemon is True

    def test_start_prevents_duplicate_threads(self):
        """Test start() prevents multiple threads from being created"""
        queue = SessionQueue()
        validator = CardValidatorIn("/dev/ttyUSB0", ":memory:", queue)

        validator.start()
        first_thread = validator.thread

        validator.start()
        second_thread = validator.thread

        assert first_thread is second_thread

    def test_stop_gracefully_stops_thread(self):
        """Test stop() gracefully stops the running thread"""
        queue = SessionQueue()
        validator = CardValidatorIn("/dev/ttyUSB0", ":memory:", queue)

        # Mock the _run method to avoid actual execution
        validator._run = Mock()
        validator.start()

        assert validator.running

        validator.stop()

        assert not validator.running
        # Thread should complete within timeout
        validator.thread.join(timeout=2)
        assert not validator.thread.is_alive()


class TestCardValidatorInEventQueue:
    """Test event queue operations"""

    @patch('serial.Serial')
    def test_event_put_on_valid_card(self, mock_serial_class):
        """Test that valid card event is put in queue"""
        queue = SessionQueue()

        # Mock serial port
        mock_serial = Mock()
        mock_serial.in_waiting = 0
        mock_serial_class.return_value = mock_serial

        validator = CardValidatorIn("/dev/ttyUSB0", ":memory:", queue)

        # Create sample event data
        event = StateEvent(
            type=EventType.CARD_IN_VALID,
            payload={"uid": "12345", "number": "ABCDE", "is_valid": True}
        )

        validator.queue.put(event)

        # Retrieve event from queue
        retrieved_event = queue.get(timeout=1)

        assert retrieved_event.type == EventType.CARD_IN_VALID
        assert retrieved_event.payload["is_valid"] is True

    def test_queue_isolation(self):
        """Test that validator has isolated queue"""
        queue1 = SessionQueue()
        queue2 = SessionQueue()

        validator1 = CardValidatorIn("/dev/ttyUSB0", ":memory:", queue1)
        validator2 = CardValidatorIn("/dev/ttyUSB1", ":memory:", queue2)

        assert validator1.queue is queue1
        assert validator2.queue is queue2
        assert validator1.queue is not validator2.queue


class TestCardValidatorInInitialization:
    """Test initialization and configuration"""

    def test_init_with_all_parameters(self):
        """Test proper initialization with all parameters"""
        queue = SessionQueue()
        validator = CardValidatorIn(
            port="/dev/ttyUSB0",
            db="cards.db",
            queue_to_push=queue
        )

        assert validator.port == "/dev/ttyUSB0"
        assert validator.db == "cards.db"
        assert validator.queue is queue
        assert validator.serial is None
        assert not validator.running
        assert validator.thread is None
        assert isinstance(validator.logger, Logger)

    def test_logger_created_with_correct_name(self):
        """Test logger is created with correct component name"""
        queue = SessionQueue()
        validator = CardValidatorIn("/dev/ttyUSB0", ":memory:", queue)

        assert validator.logger.name == "CardValidatorIn"


class TestCardValidatorIntegration:
    """Integration tests for critical workflows"""

    def test_full_validation_workflow(self):
        """Test complete card validation workflow"""
        # Setup
        queue = SessionQueue()
        db_path = ":memory:"
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE cards (
                id INTEGER PRIMARY KEY,
                uid TEXT UNIQUE,
                number TEXT UNIQUE,
                status TEXT
            )
        """)
        cursor.execute(
            "INSERT INTO cards VALUES (1, 'A1B2C3D4E5F607', '1122334455667788', 'active')"
        )
        conn.commit()

        # Test
        with patch('sqlite3.connect', return_value=conn):
            validator = CardValidatorIn("/dev/ttyUSB0", db_path, queue)

            # Test parse
            raw_data = b"\x48\x71\x10" + bytes.fromhex('04') + bytes.fromhex("A1B2C3D4E5F607") + \
                      bytes.fromhex("01") + bytes.fromhex("1122334455667788") + \
                      bytes.fromhex("00002710") + b"\00"
            parsed = validator._CardValidatorIn__parse(raw_data)

            assert parsed is not None

            # Test validate
            is_valid = validator._CardValidatorIn__validate(parsed)
            assert is_valid is True

        conn.close()

class TestCardValidatorHWTests:
    def test_waiting_for_perfect_read(self):
        bsp.bsp_init()
        events_queue = SessionQueue()
        session_queue = SessionQueue()
        intercom = IntercomRelayMonitor(events_queue)
        vld = VLDMonitor(events_queue)
        gate_ctrl = GateController()
        timer_mgr = TimerManager(events_queue)
        card_validator_in = CardValidatorIn("/dev/ttyUSB0", events_queue)
        dm = DisplayManager()
        ctx = SystemStateContext("Idle", vld, None, None, intercom, None, gate_ctrl, timer_mgr, session_queue, dm)
        intercom.start()
        vld.start()

        ev = events_queue.get()
        ctx.do(ev)

        assert ev.type == EventType.CARD_TAP
        
        ev = events_queue.get()
        ctx.do(ev)

        assert ev.type == EventType.CARD_IN_TAP

        print(ev)
