import DS18B20_Temperature

class ExternalTemperature():
    device_file = 'DS18B20_Temperature.mock'
    sensor = None

    def __init__(self):
        print('    ...Initializing "' + str(self) + '"...')
        self.sensor = DS18B20_Temperature.DS18B20(self.device_file)
        return self

    def getSensorReading(self):
        return self.sensor.getSensorReading()
