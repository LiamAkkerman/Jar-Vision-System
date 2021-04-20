#!/usr/bin/env python

# imports
from time import sleep
from datetime import datetime
import numpy as np
import sys

from picamera import PiCamera
import picamera.array
# from gpiozero import Button

import tensorflow.lite as tflite

# metadata
__copyright__ = 'Copyright 2021'
__authors__ = ['Liam Akkerman', 'Aidan Hunter']
__version__ = '0.2'
__status__ = 'Prototype'

# function definitions
def save_image(stream, path):
    filename = path + 'image_' + datetime.now().strftime('%Y%m%d%H%M%S') + '.npy'

    with open(filename, 'wb') as f:
        np.save(f, stream.array, allow_pickle=True)

    print(filename, 'written to file')

def preprocess_image():
    return None

def run_model(stream, model): #there is probably a conventional name for this
    image = stream.array[79:579, 236:736, :]/255.0 # the slicing is to crop the image. I don't know if it will work like this consitently 
    image = np.array(np.reshape(image, [1, 500, 500, 3]), dtype=np.float32) # this could be improved. there is redundant steps and it's not adaptive

    interpreter.set_tensor(start_tensor_index, image) # assign the first tensor (i.e. the input)
    interpreter.invoke()                                     # run the model to get the output
    output_data = interpreter.get_tensor(start_tensor_index) # read the last tensor (i.e. the output)

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
    interpreter = None
    collect_mode = False
    save_mode = True
    up_path = './images/'
    model_path = './model.tflite'

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

        if opt.startswith('--model'):
            model_path = opt.split("=", 1)[1]
            print('model specified:', model_path)
            continue

        print('ERROR: unknown option', opt)
        raise(KeyError)

    # load Keras model (if required)
    if not collect_mode:
        interpreter = tflite.Interpreter(model_path=model_path)
        interpreter.allocate_tensors()
        start_tensor_index = interpreter.get_input_details()[0]['index']
        end_tensor_index = interpreter.get_output_details()[0]['index']
        print('interpreter loaded')

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
            run_model(stream=stream, model=interpreter) 

        if save_mode:
            save_image(stream, path=up_path)

        

    camera.close()


