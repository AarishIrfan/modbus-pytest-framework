import pytest
from src.config import ModbusConfig

@pytest.mark.error
def test_invalid_register_read(modbus_client):
    result = modbus_client.read_register(9999)
    assert result is None

@pytest.mark.error
def test_invalid_register_write(modbus_client):
    success = modbus_client.write_register(9999, 123)
    assert not success
