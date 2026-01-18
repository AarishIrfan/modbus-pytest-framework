import threading
import asyncio
import logging
import socket
import time
from pymodbus.server import StartAsyncTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext
from pymodbus.device import ModbusDeviceIdentification
from src.config import ModbusConfig

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WindTurbineModbusServer:
    def __init__(self, host=ModbusConfig.HOST, port=ModbusConfig.PORT):
        self.host = host
        self.port = port
        self.context = None
        self.thread = None
        self.loop = None
        self._ready = threading.Event()
        self._stop_event = threading.Event()
        self._server_task = None

    def initialize_datastore(self):
        store = ModbusSlaveContext(hr=ModbusSequentialDataBlock(0, [0]*1000))
        store.setValues(3, ModbusConfig.Addresses.WIND_SPEED, [0])
        store.setValues(3, ModbusConfig.Addresses.ICE_ALERT, [0])
        store.setValues(3, ModbusConfig.Addresses.PITCH_ANGLE, [0])
        store.setValues(3, ModbusConfig.Addresses.TURBINE_STATUS, [1])
        store.setValues(3, ModbusConfig.Addresses.TEMPERATURE, [20])
        self.context = ModbusServerContext(slaves=store, single=True)
        return self.context

    def _server_thread_target(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self._run_server())

    async def _run_server(self):
        identity = ModbusDeviceIdentification()
        identity.VendorName = "Welfel Wind Turbine Simulator"
        identity.ProductName = "Wind Turbine Control System"
        identity.MajorMinorRevision = "1.0.0"

        self._server_task = asyncio.create_task(
            StartAsyncTcpServer(
                context=self.context,
                identity=identity,
                address=(self.host, self.port),
            )
        )

        self._ready.set()
        logger.info(f"Modbus server started on {self.host}:{self.port}")

        while not self._stop_event.is_set():
            await asyncio.sleep(0.1)

        self._server_task.cancel()
        try:
            await self._server_task
        except asyncio.CancelledError:
            logger.info("Server task cancelled")

    def start(self):
        self.context = self.initialize_datastore()
        self._stop_event.clear()
        self._ready.clear()

        self.thread = threading.Thread(target=self._server_thread_target, daemon=True)
        self.thread.start()

        if not self._ready.wait(timeout=10):
            raise RuntimeError("Modbus server did not become ready in 10 seconds")

        # Tiny sleep to ensure server accepts connections
        time.sleep(0.1)

        for attempt in range(20):
            try:
                with socket.create_connection((self.host, self.port), timeout=0.5):
                    logger.info(f"Server ready and accepting connections at {self.host}:{self.port}")
                    return
            except (ConnectionRefusedError, OSError, TimeoutError):
                time.sleep(0.1)

        raise RuntimeError("Modbus server not reachable after multiple attempts")

    def stop(self):
        logger.info("Stopping Modbus server...")
        self._stop_event.set()
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=5)
            if self.thread.is_alive():
                logger.warning("Server thread did not stop cleanly")
        logger.info("Modbus server stopped")

    def set_register_value(self, address, value):
        if self.context:
            if value < 0:
                value = value & 0xFFFF
            self.context[0].setValues(3, address, [value])

    def get_register_value(self, address):
        if self.context:
            values = self.context[0].getValues(3, address, count=1)
            val = values[0] if values else None
            # Convert to signed
            if val is not None and val > 0x7FFF:
                val -= 0x10000
            return val
        return None
