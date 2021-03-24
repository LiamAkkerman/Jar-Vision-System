# Jar-Vision-System
A Keras based vision system for targeting jars in a washing tray.

## Usage
### Raspberry Pi
`pi/main.py` is intended to run on the Raspberry Pi with a PiCamera v2 installed. It will run the model and return find the jar coordinates.

It accepts the following options:
| Argument | Description | Default |
| -------- | ----------- | :-----: |
| `--collect` | only collects images to add to dataset. Does not run the model | |
| `--dry`  | Dry run. Do not save images | |
| `--upload_path=/path` | upload images to `/path` | `/home/pi/images` |

### Desktop
`desktop/main.ipynb` is intended to run on a more powerful desktop. It trains the model. The model file needs to be moved to the Pi.



## TODO
### Collect Data
 - ~~develop pi software base~~
 - ~~implement camera in software~~
 - build camera jig
 - determine camera parameters
 - take all the photos
 - if the size is getting too big, find method of 
### Process Data
 - develop way to process photos
   - crop, align, etc..
   - goal would be uniformity
 - develop a GUI to manually label correct coordinates
   - pyplt can do this (but not in a jupyter notebook)
 - develop method of storing the database of labeled images
   - I think pickle will work for this in append binary mode
 - manually process all the photos
### Build Model
 - read database and feed to Keras for training
 - develop a Keras model
 - save the model as an exportable format
   - Keras can directly save a model
   - TensorFlow Lite can save models for better performance
### Run Model
 - install tensorflow on the pi in some regard
 - load model on the pi in python
 - run the model inference
 - output inference results
   - outputting to console is fine but a graphic will be better
