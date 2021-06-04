import io
import picamera
import logging
import socketserver
from threading import Condition
from http import server

class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

class StreamingHandler(server.BaseHTTPRequestHandler, webPage):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = webPage.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

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

    streamingOutput = StreamingOutput()
    streamingServer = StreamingServer()
    streamingHandler = StreamingHandler()
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
        #with picamera.PiCamera(resolution='640x480', framerate=24, format='mjpeg') as camera:
        self.camera = picamera.PiCamera(self.resolution, self.framerate, self.format)
        output = streamingOutput
        self.camera.start_recording(output, format='mjpeg')
        try:
            self.address = ('', self.serverPort)
            self.server = StreamingServer(self.address, self.StreamingHandler)
            self.server.serve_forever()
            self.currentlyStreaming = True

    def stopStreaming(self):
        self.camera.stop_recording()
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
