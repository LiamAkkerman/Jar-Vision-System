#!/usr/bin/env python

# imports
from time import sleep
import sys

from picamera import PiCamera
from gpiozero import Button

import tensorflow as tf
from tensorflow import keras

# metadata
__copyright__ = 'Copyright 2021'
__authors__ = ['Liam Akkerman', 'Aidan Hunter']
__version__ = '0.1'
__status__ = 'Prototype'

# function definitions
def capture_image(camera, save=True, path='/home/pi/images'):
    """ capture an image to feed to model and save into dataset

    Keyword arguments:
    camera -- the PiCamera object
    save -- bool on if to save the image into the dataset (default True)
    path -- path to save image to (default /home/pi/images)
    """

    filename = 'foo.rgb' #TODO change to increment or something
    camera.capture(filename, resize=(320, 320), 'rgb')
    print(filename, 'captured')

    if save:
        continue #TODO save it to the dataset folder in encoded format
        # or change to save afterwards to allow the model to run first

    return filename # or should it return the data?

def preprocess_image():
    return None

def run_model(model): #there is probably a conventional name for this

    coordinates = (0, 0) #TODO, obviously
    return coordinates

def display_result()
    #TODO I don't know how this will happen besides printing the coordinates to the console
    # a web interface could be made which overlays a circle on the image but that is over-zealous
    return None



# main program
if __name__ is '__main__':
    print('Jar Detection System. Version', __version__)

    opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
    args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]

    camera = PiCamera()
    camera.resolution = (720, 720) #TODO set the correct res and other settings
    sleep(2) # camera start up time
    print('camera initialised')

    button = Button(4) #button across GPIO4 to GND

    model = None
    if '--collect' is in opts:
        print('data collection mode, no model will run')
    else:
        model = keras.models.load_model('/home/pi/model.model') #TODO error handling, TODO pass model in args
        print('keras model loaded')

    save_mode = True
    if '--dry' is in opts:
        print('dry run mode, not images will be saved')
        save_mode = False

    up_path = '/home/pi/images'
    if any(opt.startswith('--upload_path') for opt in opts):
        up_path = opt.split("=", 1)[1] for opt in opts if opt.startswith('--upload_path') #uh, it loops twice, it could just be one TODO I suppose


    # main loop
    while True:
        button.wait_for_press()
        capture_image(camera=camera, save=save_mode, path=up_path)

        if model is None:
            # collect mode
            sleep(2)
        else:
            preprocess_image()
            run_model(model=model) 
    
    camera.close()
    return None # this will never be reached. I'm not sure how this should be for python

