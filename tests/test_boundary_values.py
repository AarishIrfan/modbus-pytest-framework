import pytest
from src.config import ModbusConfig

@pytest.mark.boundary
def test_wind_speed_boundaries(modbus_client):
    # Min boundary
    modbus_client.write_register(ModbusConfig.Addresses.WIND_SPEED, ModbusConfig.Ranges.WIND_SPEED_MIN)
    assert modbus_client.get_wind_speed() == ModbusConfig.Ranges.WIND_SPEED_MIN

    # Max boundary
    modbus_client.write_register(ModbusConfig.Addresses.WIND_SPEED, ModbusConfig.Ranges.WIND_SPEED_MAX)
    assert modbus_client.get_wind_speed() == ModbusConfig.Ranges.WIND_SPEED_MAX


@pytest.mark.boundary
def test_temperature_boundaries(modbus_client):
    # Min boundary
    modbus_client.write_register(ModbusConfig.Addresses.TEMPERATURE, ModbusConfig.Ranges.TEMP_MIN)
    assert modbus_client.get_temperature() == ModbusConfig.Ranges.TEMP_MIN

    # Max boundary
    modbus_client.write_register(ModbusConfig.Addresses.TEMPERATURE, ModbusConfig.Ranges.TEMP_MAX)
    assert modbus_client.get_temperature() == ModbusConfig.Ranges.TEMP_MAX
