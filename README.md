# **Wind Turbine Modbus Test Framework**

This project is a **simulation of a wind turbine** using Modbus TCP.
It comes with a server that mimics turbine sensors and a client that can read/write data. Perfect for **testing boundary values, error handling, and Modbus communication** in a simple way.

---

## **What’s Inside**

* `src/`

  * `modbus_server.py` — runs a simulated wind turbine server
  * `modbus_client.py` — talks to the server (reads/writes registers)
  * `config.py` — Modbus addresses and sensor ranges
* `tests/`

  * Pytest tests for boundaries, errors, and communication
* `pytest.ini` — test configuration

---

## **Features You Can See**

* Wind turbine sensors:

  * Wind speed, temperature, pitch angle, turbine status, ice alert
* Test different scenarios:

  * Boundary limits (min/max wind speed or temperature)
  * Invalid register access
  * Connection and communication
* Works on **Windows and Linux** with Python 3.10+

---

## **How to Run It**

1. Clone the repo and go to the folder:

```bash
git clone <repo-url>
cd modbus-pytest-framework
```

2. Create a Python virtual environment:

```bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Linux/macOS
```

3. Install requirements:

```bash
pip install -r requirements.txt
```

---

### **Run the Tests**

```bash
pytest
```

You’ll see tests pass/fail in the console, and an HTML coverage report is generated at `reports/test_report.html`.

---

### **Quick Demo**

```python
from src.modbus_server import WindTurbineModbusServer
from src.modbus_client import IceDetectionModbusClient
from src.config import ModbusConfig
import time

server = WindTurbineModbusServer()
server.start()
time.sleep(0.2)

client = IceDetectionModbusClient()
client.connect()

client.write_register(ModbusConfig.Addresses.WIND_SPEED, 12)
print("Wind speed:", client.get_wind_speed())

client.write_register(ModbusConfig.Addresses.TEMPERATURE, -40)
print("Temperature:", client.get_temperature())

client.disconnect()
server.stop()
```

Run this and watch the server and client interact in real-time. Simple and visual for presentations.

---

## **Why This Project Exists**

* Test your Modbus clients without needing real hardware
* Quickly simulate different sensor values and error conditions
* Learn async + threading in Python in a practical way


Do you want me to do that?
