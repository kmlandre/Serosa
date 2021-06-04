import ServoKit_Mock

class CameraServos():
    actuator = None
    numberOfServoPorts = 2

    def __init__(self):
        print('    ...Initializing "' + str(self) + '"...')
        self.actuator = ServoKit_Mock.ServoKit(self.numberOfServoPorts)
        return self

    def setActuatorState(self, value):
        return self.actuator.setActuatorState(value)

    def getCurrentState(self):
        return self.actuator.getCurrentState()

    def decrementCountdown(self):
        # Do nothing.  Countdown does not apply.
       return
