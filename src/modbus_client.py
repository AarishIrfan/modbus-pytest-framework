from pymodbus.client import ModbusTcpClient
from src.config import ModbusConfig
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IceDetectionModbusClient:
    def __init__(self, host=ModbusConfig.HOST, port=ModbusConfig.PORT, retries=5, retry_delay=0.5):
        self.host = host
        self.port = port
        self.client = None
        self.retries = retries
        self.retry_delay = retry_delay

    def connect(self):
        self.client = ModbusTcpClient(host=self.host, port=self.port, timeout=ModbusConfig.TIMEOUT)
        for attempt in range(1, self.retries + 1):
            if self.client.connect():
                logger.info(f"Connected to Modbus server {self.host}:{self.port} on attempt {attempt}")
                return True
            logger.warning(f"Connection attempt {attempt} failed, retrying in {self.retry_delay}s...")
            time.sleep(self.retry_delay)
        logger.error(f"Failed to connect to Modbus server after {self.retries} attempts")
        if self.client:
            self.client.close()
        return False

    def disconnect(self):
        if self.client:
            self.client.close()
            logger.info("Disconnected from server")

    def read_register(self, address):
        if not self.client:
            return None
        try:
            result = self.client.read_holding_registers(address, 1)
            if result.isError():
                return None
            val = result.registers[0]
            # Convert 16-bit unsigned to signed
            if val > 0x7FFF:
                val -= 0x10000
            return val
        except Exception as e:
            logger.error(f"Read register {address} failed: {e}")
            return None

    def write_register(self, address, value):
        if not self.client:
            return False
        # Convert negative values to 16-bit unsigned
        if value < 0:
            value = value & 0xFFFF
        try:
            result = self.client.write_register(address, value)
            return not result.isError()
        except Exception as e:
            logger.error(f"Write register {address}={value} failed: {e}")
            return False

    # Convenience methods
    def get_wind_speed(self):
        return self.read_register(ModbusConfig.Addresses.WIND_SPEED)

    def get_temperature(self):
        return self.read_register(ModbusConfig.Addresses.TEMPERATURE)

    def get_pitch_angle(self):
        return self.read_register(ModbusConfig.Addresses.PITCH_ANGLE)

    def get_turbine_status(self):
        return self.read_register(ModbusConfig.Addresses.TURBINE_STATUS)
