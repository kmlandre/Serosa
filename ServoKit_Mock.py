class ServoKit(object):
    default_angle = 90
    panPort = 0
    tiltPort = 1
    tiltAngle = 90
    panAngle = 90

    def __init__(self, num_ports):
        print('    ...Initializing "' + str(self) + '"...')

    def setAngle(self, port, angle):
        if port == 0:
            self.panAngle = angle
        if port == 1:
            self.tiltAngle = angle

    def reset(self, port):
        if port == 0:
            self.panAngle = self.default_angle
        if port == 1:
            self.tiltAngle = self.default_angle

    def getAngle(self, port):
        if port == 0:
            return self.panAngle
        if port == 1:
            return self.tiltAngle

    def setActuatorState(self, value):
        # Value should contain a delmited command, which
        # must be passed in one of the following forms:
        #    pan=+5     -- adds 5 degrees to the current pan angle...
        #    tilt=-5    -- subtracts 5 degrees tfromo the current tilt angle...
        #    pan=reset  -- resets the pan to default angle...
        #    tilt=97    -- sets the tile angle to exactly 97 degrees...
        cmdAction = value.split('=')
        portToUse = -1

        print(cmdAction[0])
        print(cmdAction[1])

        #  Determine which port we're trying to access...
        if cmdAction[0] == "tilt":
            portToUse = self.tiltPort
        if cmdAction[0] == "pan":
            portToUse = self.panPort

        #  Determine the nature of the command we're trying to execute...
        if str(cmdAction[1]) == "reset":
            print('Resetting "' + cmdAction[0] + '" servo...')
            self.reset(portToUse)
        if str(cmdAction[1]) == "test":
            print('Test called for "' + cmdAction[0] + '" servo...')
            self.reset(0)
            self.reset(1)
        if cmdAction[1].startswith('+') or cmdAction[1].startswith('-'):
            currentAngle = self.getAngle(portToUse)
            targetAngle = currentAngle + int(cmdAction[1])
            print('Modifying "' + cmdAction[0] + '" angle by ' + cmdAction[1] + ' to ' + str(targetAngle) + '...')
            self.setAngle(portToUse, targetAngle)
        if cmdAction[1].isnumeric():
            self.setAngle(portToUse, int(cmdAction[1]))

        return { 'tilt' : str(self.tiltAngle), 'pan': str(self.panAngle)}

    def getCurrentState(self):
        return { 'tilt' : str(self.tiltAngle), 'pan': str(self.panAngle) }
