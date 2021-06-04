
class GlobalThrottle():
    defaultThrottle = 100
    currentThrottle = 0

    def __init__(self):
        print('    ...Initializing "' + str(self) + '"...')
        self.currentThrottle = self.defaultThrottle
        return self

    def setActuatorState(self, value):
        self.currentThrottle = int(value)
        return self.currentThrottle

    def getCurrentState(self):
        return self.currentThrottle

    def decrementCountdown(self):
        # Do nothing.  Countdown does not apply.
       return
