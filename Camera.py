import VideoStreaming_Camera_Mock

class Camera():
    actuator = None

    def __init__(self):
        print('    ...Initializing "' + str(self) + '"...')
        self.actuator = VideoStreaming_Camera_Mock.VideoStreaming()
        return self

    def setActuatorState(self, value):
        return self.actuator.setActuatorState(value)

    def getCurrentState(self):
        return self.actuator.getCurrentState()

    def decrementCountdown(self):
        # Do nothing.  Countdown does not apply.
       return
