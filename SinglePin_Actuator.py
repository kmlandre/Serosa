# import RPi.GPIO as GPIO

class SinglePinActuator():
    state = 'off'
    pinNumber = 0

    def __init__(self, pinNumber):
        print('    ...Initializing "' + str(self) + '"...')
        self.state = 'off'
        self.pinNumber = pinNumber
        # self.pin = 18 # The pin ID, edit here to change it
        # GPIO.setmode(GPIO.BCM)
        # GPIO.setup(self.pinNumber, GPIO.OUT)
        # GPIO.setwarnings(False)

    def setActuatorState(self, value):
        if value == "on":
            # GPIO.output(self.pinNumber, True)
            self.state = "on"
        else:
            # GPIO.output(self.pinNumber, False)
            self.state = "off"

        return self.state;

    def getCurrentState(self):
        return self.state;
