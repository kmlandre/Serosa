import SinglePin_Actuator

class InternalFan():
    pinNumber = 18
    actuator = None

    def __init__(self):
        print('    ...Initializing "' + str(self) + '"...')
        self.actuator = SinglePin_Actuator.SinglePinActuator(self.pinNumber)
        return self

    def setActuatorState(self, value):
        return self.actuator.setActuatorState(value)

    def getCurrentState(self):
        return self.actuator.getCurrentState()

    def decrementCountdown(self):
        # Do nothing.  Countdown does not apply.
       return
