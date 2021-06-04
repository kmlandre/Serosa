import SHTC3_Mock

class InternalTempAndHumidity():
    sensor = None

    def __init__(self):
        print('    ...Initializing "' + str(self) + '"...')
        self.sensor = SHTC3_Mock.SHTC3()
        return self

    def getSensorReading(self):
        return self.sensor.getSensorReading()
