class VideoStreaming():
    webPage ="""\
    <html>
    <head>
    <title>Serosa Video Streaming</title>
    </head>
    <body>
    <h1>PiCamera MJPEG Streaming Demo</h1>
    <img src="stream.mjpg" width="$srcWidth$" height="$srcHeight$" />
    </body>
    </html>
    """

    resolution = '640x480'
    srcWidth = '???'
    srcHeight = '???'
    framerate = 24
    format = 'mjpeg'
    camera = None
    address = None
    server = None
    serverPort = 8000
    currentlyStreaming = False

    def __init__(self, resolution='640x480', framerate=24, serverPort=8000):
        print('    ...Initializing "' + str(self) + '"...')

        self.resolution = resolution
        self.framerate = framerate
        self.serverPort = serverPort

        screenDimensions = resolution.split('x')
        self.srcWidth = screenDimensions[0]
        self.srcHeight = screenDimensions[1]
        self.webPage = self.webPage.replace('$srcWidth$', self.srcWidth)
        self.webPage = self.webPage.replace('$srcHeight$', self.srcHeight)

    def startStreaming(self):
        self.currentlyStreaming = True

    def stopStreaming(self):
        self.currentlyStreaming = False

    def setActuatorState(self, value):
        if str(value) == "start":
            if self.currentlyStreaming == False:
                self.startStreaming()
        if str(value) == "stop":
            if self.currentlyStreaming == True:
                self.stopStreaming()
                
        return{ 'Port' : self.serverPort,
                'Resolution' : self.resolution,
                'Framerate' : self.framerate,
                'Format' : self.format,
                'Streaming' : self.currentlyStreaming}

    def getCurrentState(self):
        return{ 'Port' : self.serverPort,
                'Resolution' : self.resolution,
                'Framerate' : self.framerate,
                'Format' : self.format,
                'Streaming' : self.currentlyStreaming}
