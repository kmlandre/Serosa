import glob
import time

class DS18B20():
    device_file = ''

    def __init__(self, device_file):
        print('    ...Initializing "' + str(self) + '"...')
        # self.base_dir = '/sys/bus/w1/devices/'
        # self.device_folder = glob.glob(self.base_dir + '28*')[0]
        # self.device_file = self.device_folder + '/w1_slave'
        self.device_file = device_file

    def readTempRaw(self):
        #device_file = 'DS18B20_Temperature.mock'
        f = open(self.device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines

    def getSensorReading(self):
        lines = self.readTempRaw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self.readTempRaw(self)
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            temp_f = temp_c * 9.0 / 5.0 + 32.0
            ## return temp_c ## , temp_f
            return { 'C' : str(temp_c) + ' °C' , 'F': str(temp_f) + ' °F'}
