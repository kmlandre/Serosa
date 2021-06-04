import LPS22HB_Mock

class InternalPressure():
    sensor = None

    def __init__(self):
        print('    ...Initializing "' + str(self) + '"...')
        self.sensor = LPS22HB_Mock.LPS22HB()
        return self

    def getSensorReading(self):
        return self.sensor.getSensorReading()
