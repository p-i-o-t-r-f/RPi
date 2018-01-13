import RPi.GPIO as GPIO
import time
import picamera
import datetime  # new
from subprocess import call

def get_file_name():  # new
    return datetime.datetime.now().strftime("%Y-%m-%d_%H.%M.%S.h264")

sensor = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor, GPIO.IN, GPIO.PUD_DOWN)

previous_state = False
current_state = False

cam = picamera.PiCamera()

while True:
    time.sleep(0.1)
    previous_state = current_state
    current_state = GPIO.input(sensor)
    if current_state != previous_state:
        new_state = "HIGH" if current_state else "LOW"
        print("GPIO pin %s is %s" % (sensor, new_state))
        if current_state:
            fileName = get_file_name()  # new
            cam.start_preview()
            cam.start_recording(fileName)  # new
            # please change username, source folder and destination application folder
            photo = "./dropbox_uploader.sh upload /home/username/source_folder/%s /destination/%s" % (fileName,fileName)
            call ([photo], shell=True)
        else:
            cam.stop_preview()
            cam.stop_recording()  # new

