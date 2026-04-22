import pytest
import time
from datetime import datetime
import sqlite3
from bsp import bsp
from unittest.mock import Mock, MagicMock, patch, call
from app.tasks import IntercomRelayMonitor, GateController, TimerManager, VLDMonitor
from app.core import SessionQueue, DisplayManager, SystemStateContext
from app.domain import StateEvent, EventType
from app.main import Application
from app.states import Idle, OpeningGate, SerialDataProcessing, WaitingForVehicleGone, HoldingGate, ClosingGate

@patch('app.core.Database.sqlite3.connect')
@patch('app.main.TimerManager')
@patch('app.main.IntercomRelayMonitor')
@patch('app.main.VLDMonitor')
@patch('app.main.CardValidatorOut')
@patch('app.main.CardValidatorIn')
@patch('app.main.GateController')
class TestLogicFlow:
    def test_vehicle_in_card_not_valid(self, mock_gate_ctrl, mock_validator_in, mock_validator_out, mock_vldmonitor, mock_intercom_relay, mock_timermanager, mock_sqlite):
        mock = MagicMock()
        mock2 = MagicMock()
        mock3 = MagicMock()
        mock4 = MagicMock()
        mock5 = MagicMock()
        mock6 = MagicMock()
        
        mock_gate_ctrl.return_value = mock
        mock_validator_in.return_value = mock2
        mock_validator_out.return_value = mock3
        mock_vldmonitor.return_value = mock4
        mock_intercom_relay.return_value = mock5
        mock_sqlite.return_value = mock6

        app = Application()
        app._Application__setup()
        
        event = StateEvent(
            type=EventType.CARD_TAP,
            payload=None
        )

        app.events_queue.put(event)
        event = StateEvent(
            type=EventType.CARD_IN_VALID,
            payload={
                        "uid": "172A",
                        "number": "123A",
                        "is_valid": False
                    }
        )

        app.events_queue.put(event)

        for i in range(2):
            app._Application__loop()

        assert isinstance(app.ctx._state, Idle)

    def test_vehicle_in_card_valid(self, mock_gate_ctrl, mock_validator_in, mock_validator_out, mock_vldmonitor, mock_intercom_relay, mock_timermanager, mock_sqlite):
        mock = MagicMock()
        mock2 = MagicMock()
        mock3 = MagicMock()
        mock4 = MagicMock()
        mock5 = MagicMock()
        mock6 = MagicMock()
        
        mock_gate_ctrl.return_value = mock
        mock_validator_in.return_value = mock2
        mock_validator_out.return_value = mock3
        mock_vldmonitor.return_value = mock4
        mock_intercom_relay.return_value = mock5
        mock_timermanager.return_value = mock6

        app = Application()
        app._Application__setup()
        
        event = StateEvent(
            type=EventType.CARD_TAP,
            payload=None
        )
        app.events_queue.put(event)
        
        event = StateEvent(
            type=EventType.CARD_IN_VALID,
            payload={
                        "uid": "172A",
                        "number": "123A",
                        "is_valid": True
                    }
        )
        app.events_queue.put(event)

        for i in range(2):
            app._Application__loop()

        assert isinstance(app.ctx._state, WaitingForVehicleGone)

    def test_vehicle_in_complete_valid_flow(self, mock_gate_ctrl, mock_validator_in, mock_validator_out, mock_vldmonitor, mock_intercom_relay, mock_timermanager, mock_sqlite):
        mock = MagicMock()
        mock2 = MagicMock()
        mock3 = MagicMock()
        mock4 = MagicMock()
        mock5 = MagicMock()
        mock6 = MagicMock()
        
        mock_gate_ctrl.return_value = mock
        mock_validator_in.return_value = mock2
        mock_validator_out.return_value = mock3
        mock_vldmonitor.return_value = mock4
        mock_intercom_relay.return_value = mock5
        mock_timermanager.return_value = mock6

        app = Application()
        app._Application__setup()
        
        event = StateEvent(
            type=EventType.CARD_TAP,
            payload=None
        )
        app.events_queue.put(event)
        
        event = StateEvent(
            type=EventType.CARD_IN_VALID,
            payload={
                        "uid": "172A",
                        "number": "123A",
                        "is_valid": True
                    }
        )
        app.events_queue.put(event)

        event = StateEvent(
            type=EventType.VEHICLE_DETECTED,
            payload=None
            
        )
        app.events_queue.put(event)

        event = StateEvent(
            type=EventType.VEHICLE_GONE,
            payload=None
        )
        app.events_queue.put(event)

        event = StateEvent(
            type=EventType.GENERIC_TIMEOUT,
            payload=None
        )
        app.events_queue.put(event)

        l = app.events_queue.qsize()
        for i in range(l):
            app._Application__loop()

        assert isinstance(app.ctx._state, Idle)
    
    
    def test_vehicle_in_complete_alternative_valid_flow(self, mock_gate_ctrl, mock_validator_in, mock_validator_out, mock_vldmonitor, mock_intercom_relay, mock_timermanager, mock_sqlite):
        mock = MagicMock()
        mock2 = MagicMock()
        mock3 = MagicMock()
        mock4 = MagicMock()
        mock5 = MagicMock()
        mock6 = MagicMock()
        
        mock_gate_ctrl.return_value = mock
        mock_validator_in.return_value = mock2
        mock_validator_out.return_value = mock3
        mock_vldmonitor.return_value = mock4
        mock_intercom_relay.return_value = mock5
        mock_timermanager.return_value = mock6

        app = Application()
        app._Application__setup()

        event = StateEvent(
            type=EventType.VEHICLE_DETECTED,
            payload=None
        )
        app.events_queue.put(event)
        
        event = StateEvent(
            type=EventType.CARD_TAP,
            payload=None
        )
        app.events_queue.put(event)
        
        event = StateEvent(
            type=EventType.CARD_IN_VALID,
            payload={
                        "uid": "172A",
                        "number": "123A",
                        "is_valid": True
                    }
        )
        app.events_queue.put(event)

        event = StateEvent(
            type=EventType.VEHICLE_DETECTED,
            payload=None
        )
        app.events_queue.put(event)

        event = StateEvent(
            type=EventType.VEHICLE_GONE,
            payload=None
        )
        app.events_queue.put(event)

        event = StateEvent(
            type=EventType.GENERIC_TIMEOUT,
            payload=None
        )
        app.events_queue.put(event)

        l = app.events_queue.qsize()
        for i in range(l):
            app._Application__loop()

        assert isinstance(app.ctx._state, Idle)

    def test_vehicle_in_when_tapping_card(self, mock_gate_ctrl, mock_validator_in, mock_validator_out, mock_vldmonitor, mock_intercom_relay, mock_timermanager, mock_sqlite):
        mock = MagicMock()
        mock2 = MagicMock()
        mock3 = MagicMock()
        mock4 = MagicMock()
        mock5 = MagicMock()
        mock6 = MagicMock()
        mock4.get_state.return_value = True # HIGH, detected
        
        mock_gate_ctrl.return_value = mock
        mock_validator_in.return_value = mock2
        mock_validator_out.return_value = mock3
        mock_vldmonitor.return_value = mock4
        mock_intercom_relay.return_value = mock5
        mock_timermanager.return_value = mock6

        app = Application()
        app._Application__setup()

        event = StateEvent(
            type=EventType.VEHICLE_DETECTED,
            payload=None
        )
        app.events_queue.put(event)
        
        event = StateEvent(
            type=EventType.CARD_TAP,
            payload=None
        )
        app.events_queue.put(event)
        
        event = StateEvent(
            type=EventType.CARD_IN_VALID,
            payload={
                        "uid": "172A",
                        "number": "123A",
                        "is_valid": True
                    }
        )
        app.events_queue.put(event)

        event = StateEvent(
            type=EventType.VEHICLE_GONE,
            payload=None
        )
        app.events_queue.put(event)

        event = StateEvent(
            type=EventType.GENERIC_TIMEOUT,
            payload=None
        )
        app.events_queue.put(event)

        l = app.events_queue.qsize()
        for i in range(l):
            app._Application__loop()

        assert isinstance(app.ctx._state, Idle)


    def test_multiple_tapper(self, mock_gate_ctrl, mock_validator_in, mock_validator_out, mock_vldmonitor, mock_intercom_relay, mock_timermanager, mock_sqlite):
        mock = MagicMock()
        mock2 = MagicMock()
        mock3 = MagicMock()
        mock4 = MagicMock()
        mock5 = MagicMock()
        mock6 = MagicMock()
        mock4.get_state.return_value = True # HIGH, detected
        
        mock_gate_ctrl.return_value = mock
        mock_validator_in.return_value = mock2
        mock_validator_out.return_value = mock3
        mock_vldmonitor.return_value = mock4
        mock_intercom_relay.return_value = mock5
        mock_timermanager.return_value = mock6

        app = Application()
        app._Application__setup()

        event = StateEvent(
            type=EventType.CARD_TAP,
            payload=None
        )
        app.events_queue.put(event)
        
        event = StateEvent(
            type=EventType.CARD_IN_VALID,
            payload={
                        "uid": "172A",
                        "number": "123A",
                        "is_valid": True
                    }
        )
        app.events_queue.put(event)

        event = StateEvent(     # Should be ignored until first tapper done
            type=EventType.CARD_TAP,
            payload=None
        )
        app.events_queue.put(event)
        
        event = StateEvent(
            type=EventType.VEHICLE_GONE,
            payload=None
        )
        app.events_queue.put(event)

        event = StateEvent(
            type=EventType.GENERIC_TIMEOUT,
            payload=None
        )
        app.events_queue.put(event)

        l = app.events_queue.qsize()
        for i in range(l):
            app._Application__loop()

            if i == 2:
                assert isinstance(app.ctx._state, WaitingForVehicleGone)         
                

        assert isinstance(app.ctx._state, Idle)

    def test_holding_the_gate(self, mock_gate_ctrl, mock_validator_in, mock_validator_out, mock_vldmonitor, mock_intercom_relay, mock_timermanager, mock_sqlite):
        mock = MagicMock()
        mock2 = MagicMock()
        mock3 = MagicMock()
        mock4 = MagicMock()
        mock5 = MagicMock()
        mock6 = MagicMock()
        mock4.get_state.return_value = True # HIGH, detected
        
        mock_gate_ctrl.return_value = mock
        mock_validator_in.return_value = mock2
        mock_validator_out.return_value = mock3
        mock_vldmonitor.return_value = mock4
        mock_intercom_relay.return_value = mock5
        mock_timermanager.return_value = mock6

        app = Application()
        app._Application__setup()

        event = StateEvent(
            type=EventType.CARD_TAP,
            payload=None
        )
        app.events_queue.put(event)
        
        event = StateEvent(
            type=EventType.CARD_IN_VALID,
            payload={
                        "uid": "172A",
                        "number": "123A",
                        "is_valid": True
                    }
        )
        app.events_queue.put(event)

        event = StateEvent(     # Should be ignored until first tapper done
            type=EventType.CARD_TAP,
            payload=None
        )
        app.events_queue.put(event)
        
        event = StateEvent(
            type=EventType.VEHICLE_GONE,
            payload=None
        )
        app.events_queue.put(event)

        event = StateEvent(
            type=EventType.VEHICLE_DETECTED,
            payload=None
        )
        app.events_queue.put(event)

        event = StateEvent(
            type=EventType.VEHICLE_GONE,
            payload=None
        )
        app.events_queue.put(event)

        event = StateEvent(
            type=EventType.VEHICLE_DETECTED,
            payload=None
        )
        app.events_queue.put(event)

        event = StateEvent(
            type=EventType.VEHICLE_GONE,
            payload=None
        )
        app.events_queue.put(event)
        
        event = StateEvent(
            type=EventType.GENERIC_TIMEOUT,
            payload=None
        )
        app.events_queue.put(event)

        l = app.events_queue.qsize()
        for i in range(l):
            app._Application__loop()

            if i == 4:
                assert isinstance(app.ctx._state, HoldingGate)                
            if i == 6:
                assert isinstance(app.ctx._state, HoldingGate)                

        assert isinstance(app.ctx._state, Idle)                


    def test_opening_timeout(self, mock_gate_ctrl, mock_validator_in, mock_validator_out, mock_vldmonitor, mock_intercom_relay, mock_timermanager, mock_sqlite):
        mock = MagicMock()
        mock2 = MagicMock()
        mock3 = MagicMock()
        mock4 = MagicMock()
        mock5 = MagicMock()
        mock6 = MagicMock()
        mock4.get_state.return_value = True # HIGH, detected
        
        mock_gate_ctrl.return_value = mock
        mock_validator_in.return_value = mock2
        mock_validator_out.return_value = mock3
        mock_vldmonitor.return_value = mock4
        mock_intercom_relay.return_value = mock5
        mock_timermanager.return_value = mock6

        app = Application()
        app._Application__setup()

        event = StateEvent(
            type=EventType.CARD_TAP,
            payload=None
        )
        app.events_queue.put(event)
        
        event = StateEvent(
            type=EventType.CARD_IN_VALID,
            payload={
                        "uid": "172A",
                        "number": "123A",
                        "is_valid": True
                    }
        )
        app.events_queue.put(event)

        event = StateEvent(
            type=EventType.GENERIC_TIMEOUT,
            payload=None
        )
        app.events_queue.put(event)

        l = app.events_queue.qsize()
        for i in range(l):
            app._Application__loop()

        assert isinstance(app.ctx._state, ClosingGate)        
    
    def test_serial_reading_timeout(self, mock_gate_ctrl, mock_validator_in, mock_validator_out, mock_vldmonitor, mock_intercom_relay, mock_timermanager, mock_sqlite):
        mock = MagicMock()
        mock2 = MagicMock()
        mock3 = MagicMock()
        mock4 = MagicMock()
        mock5 = MagicMock()
        mock6 = MagicMock()
        mock4.get_state.return_value = True # HIGH, detected
        
        mock_gate_ctrl.return_value = mock
        mock_validator_in.return_value = mock2
        mock_validator_out.return_value = mock3
        mock_vldmonitor.return_value = mock4
        mock_intercom_relay.return_value = mock5
        mock_timermanager.return_value = mock6

        app = Application()
        app._Application__setup()

        event = StateEvent(
            type=EventType.CARD_TAP,
            payload=None
        )
        app.events_queue.put(event)
        
        event = StateEvent(
            type=EventType.GENERIC_TIMEOUT,
            payload=None
        )
        app.events_queue.put(event)

        l = app.events_queue.qsize()
        for i in range(l):
            app._Application__loop()

        assert isinstance(app.ctx._state, Idle)

    def test_intercom_override(self, mock_gate_ctrl, mock_validator_in, mock_validator_out, mock_vldmonitor, mock_intercom_relay, mock_timermanager, mock_sqlite):
        mock = MagicMock()
        mock2 = MagicMock()
        mock3 = MagicMock()
        mock4 = MagicMock()
        mock5 = MagicMock()
        mock6 = MagicMock()
        mock4.get_state.return_value = True # HIGH, detected
        
        mock_gate_ctrl.return_value = mock
        mock_validator_in.return_value = mock2
        mock_validator_out.return_value = mock3
        mock_vldmonitor.return_value = mock4
        mock_intercom_relay.return_value = mock5
        mock_timermanager.return_value = mock6

        app = Application()
        app._Application__setup()

        event = StateEvent(
            type=EventType.CARD_TAP,
            payload=None
        )
        app.events_queue.put(event)
        
        event = StateEvent(
            type=EventType.INTERCOM_OVERRIDE,
            payload=None
        )
        app.events_queue.put(event)

        l = app.events_queue.qsize()
        for i in range(l):
            app._Application__loop()

        assert isinstance(app.ctx._state, WaitingForVehicleGone)

    def test_intercom_override_when_closing(self, mock_gate_ctrl, mock_validator_in, mock_validator_out, mock_vldmonitor, mock_intercom_relay, mock_timermanager, mock_sqlite):
        mock = MagicMock()
        mock2 = MagicMock()
        mock3 = MagicMock()
        mock4 = MagicMock()
        mock5 = MagicMock()
        mock6 = MagicMock()
        mock4.get_state.return_value = True # HIGH, detected
        
        mock_gate_ctrl.return_value = mock
        mock_validator_in.return_value = mock2
        mock_validator_out.return_value = mock3
        mock_vldmonitor.return_value = mock4
        mock_intercom_relay.return_value = mock5
        mock_timermanager.return_value = mock6

        app = Application()
        app._Application__setup()

        event = StateEvent(
            type=EventType.CARD_TAP,
            payload=None
        )
        app.events_queue.put(event)

        event = StateEvent(
            type=EventType.CARD_IN_VALID,
            payload={
                        "uid": "172A",
                        "number": "123A",
                        "is_valid": True
                    }
        )
        app.events_queue.put(event)

        event = StateEvent(
            type=EventType.VEHICLE_DETECTED,
            payload=None
        )
        app.events_queue.put(event)

        event = StateEvent(
            type=EventType.VEHICLE_GONE,
            payload=None
        )
        app.events_queue.put(event)
        
        event = StateEvent(
            type=EventType.INTERCOM_OVERRIDE,
            payload=None
        )
        app.events_queue.put(event)

        l = app.events_queue.qsize()
        for i in range(l):
            app._Application__loop()

        assert isinstance(app.ctx._state, WaitingForVehicleGone)

    def test_intercom_override_when_holding(self, mock_gate_ctrl, mock_validator_in, mock_validator_out, mock_vldmonitor, mock_intercom_relay, mock_timermanager, mock_sqlite):
        mock = MagicMock()
        mock2 = MagicMock()
        mock3 = MagicMock()
        mock4 = MagicMock()
        mock5 = MagicMock()
        mock6 = MagicMock()
        mock4.get_state.return_value = True # HIGH, detected
        
        mock_gate_ctrl.return_value = mock
        mock_validator_in.return_value = mock2
        mock_validator_out.return_value = mock3
        mock_vldmonitor.return_value = mock4
        mock_intercom_relay.return_value = mock5
        mock_timermanager.return_value = mock6

        app = Application()
        app._Application__setup()

        event = StateEvent(
            type=EventType.CARD_TAP,
            payload=None
        )
        app.events_queue.put(event)

        event = StateEvent(
            type=EventType.CARD_IN_VALID,
            payload={
                        "uid": "172A",
                        "number": "123A",
                        "is_valid": True
                    }
        )
        app.events_queue.put(event)

        event = StateEvent(
            type=EventType.VEHICLE_DETECTED,
            payload=None
        )
        app.events_queue.put(event)

        event = StateEvent(
            type=EventType.VEHICLE_GONE,
            payload=None
        )
        app.events_queue.put(event)

        event = StateEvent(
            type=EventType.VEHICLE_DETECTED,
            payload=None
        )
        app.events_queue.put(event)
        
        event = StateEvent(
            type=EventType.INTERCOM_OVERRIDE,
            payload=None
        )
        app.events_queue.put(event)

        l = app.events_queue.qsize()
        for i in range(l):
            app._Application__loop()

        assert isinstance(app.ctx._state, WaitingForVehicleGone)

    def test_intercom_override_when_idle(self, mock_gate_ctrl, mock_validator_in, mock_validator_out, mock_vldmonitor, mock_intercom_relay, mock_timermanager, mock_sqlite):
        mock = MagicMock()
        mock2 = MagicMock()
        mock3 = MagicMock()
        mock4 = MagicMock()
        mock5 = MagicMock()
        mock6 = MagicMock()
        mock4.get_state.return_value = True # HIGH, detected
        
        mock_gate_ctrl.return_value = mock
        mock_validator_in.return_value = mock2
        mock_validator_out.return_value = mock3
        mock_vldmonitor.return_value = mock4
        mock_intercom_relay.return_value = mock5
        mock_timermanager.return_value = mock6

        app = Application()
        app._Application__setup()

        event = StateEvent(
            type=EventType.INTERCOM_OVERRIDE,
            payload=None
        )
        app.events_queue.put(event)

        l = app.events_queue.qsize()
        for i in range(l):
            app._Application__loop()

        assert isinstance(app.ctx._state, WaitingForVehicleGone)                        
        
    # def test_shutdown(self, mock_gate_ctrl, mock_validator_in, mock_validator_out, mock_vldmonitor, mock_intercom_relay, mock_timermanager):
    #     mock = MagicMock()
    #     mock2 = MagicMock()
    #     mock3 = MagicMock()
    #     mock4 = MagicMock()
    #     mock5 = MagicMock()
    #     mock6 = MagicMock()
    #     mock4.get_state.return_value = True # HIGH, detected
        
    #     mock_gate_ctrl.return_value = mock
    #     mock_validator_in.return_value = mock2
    #     mock_validator_out.return_value = mock3
    #     mock_vldmonitor.return_value = mock4
    #     mock_intercom_relay.return_value = mock5
    #     mock_timermanager.return_value = mock6

    #     app = Application()
    #     app._Application__setup()

    #     event = StateEvent(
    #         type=EventType.ASKING_FOR_SHUTDOWN,
    #         payload=None
    #     )
    #     app.events_queue.put(event)
        
    #     l = app.events_queue.qsize()
    #     for i in range(l):
    #         app._Application__loop()

    #     assert isinstance(app.ctx._state, Idle)        
    
class TestMainHWTests:
    def test_invoker_intercom(self):
        bsp.bsp_init()
        events_queue = SessionQueue()
        session_queue = SessionQueue()
        intercom_relay = IntercomRelayMonitor(events_queue)
        vld = VLDMonitor(events_queue)
        gate_ctrl = GateController()
        timer_mgr = TimerManager(events_queue)
        dm = DisplayManager()
        ctx = SystemStateContext("Idle", vld, None, None, intercom_relay, None, gate_ctrl, timer_mgr, session_queue, dm)

        intercom_relay.start()
        vld.start()

        print("Waiting for intercom signal...")
        time.sleep(3)

        assert events_queue.qsize() == 1

        intercom_relay.stop()
        vld.stop()
        ev = events_queue.get()
        ctx.do(ev)
        
        assert isinstance(ctx._state, WaitingForVehicleGone) 

    def test_invoker_intercom_with_vld(self):
        bsp.bsp_init()
        events_queue = SessionQueue()
        session_queue = SessionQueue()
        intercom = IntercomRelayMonitor(events_queue)
        vld = VLDMonitor(events_queue)
        gate_ctrl = GateController()
        timer_mgr = TimerManager(events_queue)
        dm = DisplayManager()
        ctx = SystemStateContext("Idle", vld, None, None, intercom, None, gate_ctrl, timer_mgr, session_queue, dm)
        intercom.start()
        vld.start()

        print("Waiting for intercom signal...")

        ev = events_queue.get()
        print("ev:", ev)
        ctx.do(ev)
        print(ctx._state)

        print("Waiting for vld signal going low...")

        ev = events_queue.get()
        print("ev:", ev)
        ctx.do(ev)

        ev = events_queue.get()
        print("ev:", ev)
        ctx.do(ev)
        print(ctx._state)
        
        assert isinstance(ctx._state, ClosingGate)

        ev = events_queue.get()
        ctx.do(ev)

        intercom.stop()
        vld.stop()
        
        assert isinstance(ctx._state, Idle)

    def test_when_valid_dummy_card_data(self):
        bsp.bsp_init()
        events_queue = SessionQueue()
        session_queue = SessionQueue()
        intercom = IntercomRelayMonitor(events_queue)
        vld = VLDMonitor(events_queue)
        gate_ctrl = GateController()
        timer_mgr = TimerManager(events_queue)
        dm = DisplayManager()
        ctx = SystemStateContext("Idle", vld, None, None, intercom, None, gate_ctrl, timer_mgr, session_queue, dm)
        intercom.start()
        vld.start()        
        
        event = StateEvent(
            type=EventType.CARD_TAP,
            payload=None
        )
        events_queue.put(event)
        event = StateEvent(
            type=EventType.CARD_IN_VALID,
            payload={
                        "uid": "11223344",
                        "number": "1231232",
                        "is_valid": True
                    }
        )
        events_queue.put(event)

        ev = events_queue.get()
        ctx.do(ev)
        ev = events_queue.get()
        ctx.do(ev)
        
        print('waiting for vehicle gone...')

        ev = events_queue.get()
        ctx.do(ev)
        ev = events_queue.get()
        ctx.do(ev)

        print('waiting for closing timeout expired...')
        
        ev = events_queue.get()
        ctx.do(ev)
        
        intercom.stop()
        vld.stop()

        assert isinstance(ctx._state, Idle)


        
        
        

        

        
