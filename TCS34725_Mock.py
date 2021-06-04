class TCS34725:
    R = 241
    G = 248
    B = 200
    C = 23
    RGB888_R = 241
    RGB888_G = 248
    RGB888_B = 200
    RGB888 = 0XF1F8C8
    RGB565 = 0XF7D9

    def __init__(self, address=0x29, debug=False):
        print('    ...Initializing "' + str(self) + '"...')

    def getSensorReading(self):
        return {"r" : "%d"%self.RGB888_R,
                "g" : "%d"%self.RGB888_G,
                "b" : "%d"%self.RGB888_B,
                "c" : "%#x "%self.C,
                "RGB565" : "%#x "%self.RGB565,
                "RGB888" : "%#x "%self.RGB888,
                "lux" : "%d"%0,
                "colorTemperature" : "%dK"%0}
