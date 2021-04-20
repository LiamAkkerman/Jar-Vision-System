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
| `--model=filename` | Specify the tflite model file | `/home/pi/model.tflite` |

### Desktop
`desktop/main.ipynb` is intended to run on a more powerful desktop. It trains the model. The model file needs to be moved to the Pi.

`desktop/generator.py` is used to create labels for the photos. Run the script to launch an interactive matplotlib windows. It will automatically load `.npy` RBG arrays in from file (if any are present, the paths may need adjusting). 
1. an image will appear
2. click 3 points on the rim of a jar. select the upper most lip of the jar mouth.
3. a circle and marker will appear
4. repeat until all jars have be marked with circles
5. once all jars are marked, press "Next Photo"
6. the circles remain in place for the next photo
7. if the carried over circles are incorrect, press "Clear"
8. continue until over
9. press "Done" to save the labelled dataset to a file and exit

 - every 10 images, it will autosave into an archive with "_autosave" appended
 - "Undo" will remove any + markers on screen
 - "Undo" will remove the last marked circle centre entirely if no + is present
 - "Undo" can only remove the one most recent circle centre and only from the current photo
 - if you need more undone, use "Clear" and restart the current photo
 - pressing "Next Photo" can not be undone and the data since the last autosave is ruined
 - if a grievous error is made (like finishing an image with a mistake), exit the script and rely on the last autosave
 - "Clear" removes all marks and centres on a photo
 - "Done" will also record the marked centres, do not press "Done" with unmarked jars
 - pressing "Done" can be done at any time to save
 - once a photo has been labeled, it will not reappear while using this program later
 - it is recommended to label an entire batch (26 photos) before exiting
   - this is why the centres carry over



## TODO
### Collect Data
 - ~~develop pi software base~~
 - ~~implement camera in software~~
 - ~~build camera jig~~
 - determine camera parameters
 - take tonnes of photos
 - ~~if the size is getting too big, find method of compression~~
### Process Data
 - ~~develop way to process photos~~
   - ~~crop, align, etc..~~
   - ~~goal would be uniformity~~
 - ~~develop a GUI to manually label correct coordinates~~
   - ~~pyplt can do this (but not in a jupyter notebook)~~
 - ~~develop method of storing the database of labeled images~~
   - ~~I think pickle will work for this in append binary mode~~
 - manually process all the photos
### Build Model
 - read database and feed to Keras for training
 - develop a Keras model
 - ~~save the model as an exportable format~~
   - ~~Keras can directly save a model~~
   - ~~TensorFlow Lite can save models for better performance~~
### Run Model
 - ~~install tensorflow on the pi in some regard~~
 - ~~load model on the pi in python~~
 - ~~run the model inference~~
 - output inference results
   - outputting to console is fine but a graphic will be better
