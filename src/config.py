class ModbusConfig:
    HOST = "127.0.0.1"
    PORT = 5020
    TIMEOUT = 3
    
    class Addresses:
        WIND_SPEED = 120
        ICE_ALERT = 121
        PITCH_ANGLE = 122
        TURBINE_STATUS = 123
        TEMPERATURE = 124
        
    class Ranges:
        WIND_SPEED_MIN = 0
        WIND_SPEED_MAX = 100
        TEMP_MIN = -40
        TEMP_MAX = 60
        PITCH_MIN = 0
        PITCH_MAX = 90
        
    class Alerts:
        ICE_DETECTED = 1
        NO_ICE = 0
        TURBINE_RUNNING = 1
        TURBINE_STOPPED = 0
