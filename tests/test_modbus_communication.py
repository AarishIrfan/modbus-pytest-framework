import pytest
from src.config import ModbusConfig

@pytest.mark.communication
def test_client_connection(modbus_client):
    assert modbus_client is not None

@pytest.mark.communication
def test_write_and_read_register(modbus_client):
    assert modbus_client.write_register(ModbusConfig.Addresses.WIND_SPEED, 15)
    assert modbus_client.read_register(ModbusConfig.Addresses.WIND_SPEED) == 15
