#i2c address
LPS22HB_I2C_ADDRESS	  =  0x5C

class LPS22HB(object):
    def __init__(self,address=LPS22HB_I2C_ADDRESS):
        print('    ...Initializing "' + str(self) + '"...')

    def getSensorReading(self):
        PRESS_DATA = 997.15
        TEMP_DATA = 31.86

        print('Pressure = %6.2f hPa , Temperature = %6.2f °C\r\n'%(PRESS_DATA,TEMP_DATA))

        return { 'Pressure' : '%6.2f hPa'%(PRESS_DATA) , 'Temperature': '%6.2f °C'%(TEMP_DATA) }
