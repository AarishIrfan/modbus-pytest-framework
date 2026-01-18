import pytest
import time
from src.modbus_server import WindTurbineModbusServer
from src.modbus_client import IceDetectionModbusClient

@pytest.fixture(scope="module")
def modbus_server():
    server = WindTurbineModbusServer()
    server.start()
    time.sleep(0.2)  # ensure server fully accepts connections
    yield server
    server.stop()


@pytest.fixture
def modbus_client(modbus_server):
    client = IceDetectionModbusClient()
    for attempt in range(5):
        if client.connect():
            break
        time.sleep(0.1)
    else:
        pytest.fail("Could not connect Modbus client to server")
    yield client
    client.disconnect()
