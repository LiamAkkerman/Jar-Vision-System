#!/usr/bin/env python

# imports
from time import sleep
from datetime import datetime
import numpy as np
import sys

from picamera import PiCamera
import picamera.array
# from gpiozero import Button

# import tensorflow as tf
# from tensorflow import keras
import tflite_runtime as tflite

# metadata
__copyright__ = 'Copyright 2021'
__authors__ = ['Liam Akkerman', 'Aidan Hunter']
__version__ = '0.1'
__status__ = 'Prototype'

# function definitions
def save_image(stream, path):
    #filename = path + datetime.now().strftime('%Y%m%d%H%M%S') + '.npy'
    filename = path + 'image_' + datetime.now().strftime('%Y%m%d%H%M%S') + '.npy' # remove this line once testing is done

    with open(filename, 'wb') as f:
        np.save(f, stream.array, allow_pickle=True)

    print(filename, 'written to file')

def preprocess_image():
    return None

def run_model(stream, model): #there is probably a conventional name for this

    coordinates = (0, 0) #TODO, obviously
    return coordinates

def display_result():
    #TODO I don't know how this will happen besides printing the coordinates to the console
    # a web interface could be made which overlays a circle on the image but that is over-zealous
    return None



# main program
if __name__ == '__main__':
    print('Jar Detection System. Version', __version__)

    # get command line options and parameters
    opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
    args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]

    # initialize camera
    camera = PiCamera()
    camera.resolution = (820, 616)
    sleep(2) # camera start up time
    stream = picamera.array.PiRGBArray(camera)
    print('camera initialised')

    # initialize the hardware button
    # the button is used to take a photo and run the model
    # button across GPIO4 to GND
    # button = Button(4) 

    # default options
    model = None
    collect_mode = False
    save_mode = True
    up_path = '/home/pi/images/'

    # parse command line options
    while opts:
        opt = opts.pop()
        print('option:', opt)
        if opt == '--collect':
            print('data collection mode, no model will run')
            collect_mode = True
            continue

        if opt == '--dry':
            print('dry run mode, not images will be saved')
            save_mode = False
            continue

        if opt.startswith('--upload_path'):
            up_path = opt.split("=", 1)[1]
            print('upload path specified:', up_path)
            continue

        print('ERROR: unknown option', opt)
        raise(KeyError)

    # load Keras model (if required)
    if not collect_mode:
        model = keras.models.load_model('/home/pi/model.model') #TODO error handling, TODO pass model in args
        print('keras model loaded')

    print('\nready!')
    # main loop
    while True:
        print('\a', end='') # make a noise to signal it's ready to go
        stream.truncate(0) #flushes the stream clean
        #button.wait_for_press()
        user_input = input("Press a key to take photo")
        if user_input.lower() == 'exit':
            break
        
        #stream = capture_image(camera=camera)
        camera.capture(stream, 'rgb')

        if collect_mode:
            sleep(1)
        else:
            preprocess_image()
            run_model(stream=stream, model=model) 

        if save_mode:
            save_image(stream, path=up_path)

        

    camera.close()


