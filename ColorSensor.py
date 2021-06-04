import TCS34725_Mock

class ColorSensor():
    sensor = None

    def __init__(self):
        print('    ...Initializing "' + str(self) + '"...')
        self.sensor = TCS34725_Mock.TCS34725()
        return self

    def getSensorReading(self):
        return self.sensor.getSensorReading()
