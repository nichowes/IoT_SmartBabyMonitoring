from time import sleep
from picamera import PiCamera

camera = PiCamera()
camera.resolution = (1024,768)
camera.start_preview()

# camera warm up
sleep(5)
camera.capture('testing.jpg')
