class SHTC3:
    def __init__(self):
        print('    ...Initializing "' + str(self) + '"...')

    def SHTC3_Read_Temperature(self):
        return 32.32

    def SHTC3_Read_Humidity(self):
        return 2.07

    def getSensorReading(self):
        return{ 'Temperature' : '%.2f °C'%(self.SHTC3_Read_Temperature()) ,
                'Humidity' : '%.2f%%'%(self.SHTC3_Read_Humidity()) }
