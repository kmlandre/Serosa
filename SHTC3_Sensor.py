import ctypes

class SHTC3:
    def __init__(self):
        print('    ...Initializing "' + str(self) + '"...')
        self.dll = ctypes.CDLL("./SHTC3.so")
        init = self.dll.init
        init.restype = ctypes.c_int
        init.argtypes = [ctypes.c_void_p]
        init(None)

    def SHTC3_Read_Temperature(self):
        temperature = self.dll.SHTC3_Read_TH
        temperature.restype = ctypes.c_float
        temperature.argtypes = [ctypes.c_void_p]
        return temperature(None)
        return 32.32

    def SHTC3_Read_Humidity(self):
        humidity = self.dll.SHTC3_Read_RH
        humidity.restype = ctypes.c_float
        humidity.argtypes = [ctypes.c_void_p]
        return humidity(None)
        return 2.07

    def getSensorReading(self):
        return{ 'Temperature' : '%.2f °C'%(self.SHTC3_Read_Temperature()) ,
                'Humidity' : '%.2f%%'%(self.SHTC3_Read_Humidity()) }
