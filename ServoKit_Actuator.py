import time
import adafruit_servokit

class ServoKit(object):
    default_angle = 90
    panPort = 0
    tiltPort = 1
    tiltAngle = 90
    panAngle = 90

    def __init__(self, num_ports):
        print('    ...Initializing "' + str(self) + '"...')
        self.kit = adafruit_servokit.ServoKit(channels=16)
        self.num_ports = num_ports
        self.resetAll()
        print("Initializing complete.")

    def setAngle(self, port, angle):
        if angle < 0:
            self.kit.servo[port].angle = 0
        elif angle > 180:
            self.kit.servo[port].angle = 180
        else:
            self.kit.servo[port].angle = angle

    def getAngle(self, port):
        return self.kit.servo[port].angle

    def reset(self, port):
        self.kit.servo[port].angle = self.default_angle

    def resetAll(self):
        for i in range(self.num_ports):
            self.kit.servo[i].angle = self.default_angle

    def test(self):
        servoKit = ServoKit(4)
        print("Start ServoKit test")
        for i in range(0,180, 5):
            servoKit.setAngle(0, i)
            servoKit.setAngle(2, i)
            time.sleep(.05)
        for i in range(180,0,-5):
            servoKit.setAngle(0, i)
            servoKit.setAngle(2, i)
            time.sleep(.05)

        for i in range(15,145, 5):
            servoKit.setAngle(1, i)
            servoKit.setAngle(3, i)
            time.sleep(.05)
        for i in range(145,15,-5):
            servoKit.setAngle(1, i)
            servoKit.setAngle(3, i)
            time.sleep(.05)

        servoKit.resetAll()

    def setActuatorState(self, value):
        # Value should contain a delmited command, which
        # must be passed in one of the following forms:
        #    pan=+5     -- adds 5 degrees to the current pan angle...
        #    tilt=-5    -- subtracts 5 degrees tfromo the current tilt angle...
        #    pan=reset  -- resets the pan to default angle...
        #    tilt=97    -- sets the tile angle to exactly 97 degrees...
        cmdAction = value.split('=')
        portToUse = -1

        #  Determine which port we're trying to access...
        if cmdAction[0] == 'tilt':
            portToUse = self.tiltPort
        if cmdAction[0] == 'pan':
            portToUse = self.panPort

        #  Determine the nature of the command we're trying to execute...
        if str(cmdAction[1]) == "reset":
            self.reset(portToUse)
        if str(cmdAction[1]) == "test":
            self.test()
        if cmdAction[1].startswith('+') or cmdAction[1].startswith('-'):
            currentAngle = self.getAngle(portToUse)
            targetAngle = currentAngle + int(cmdAction[1])
            self.setAngle(portToUse, targetAngle)
        if cmdAction[1].isnumeric():
            self.setAngle(portToUse, int(cmdAction[1]))

        self.tiltAngle = self.getAngle(tiltPort)
        self.panAngle = self.getAngle(panPort)

        return { 'tilt' : str(self.tiltAngle), 'pan': str(self.panAngle) }

    def getCurrentState(self):
        return { 'tilt' : str(self.tiltAngle), 'pan': str(self.panAngle) }
