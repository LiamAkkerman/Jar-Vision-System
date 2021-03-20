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
 - implement camera
   - camera hardware en route
 - build camera jig
 - develop preprocessing routine
 - develop results visualization
   - could be canceled
 - develop method of storing dataset
   - assuming they exceed the GitHub limits
   - I can host an FTP or webDEV server
 - collect dataset
 - figure out way to feed RGB images into Keras
   - instead of converting it to Numpy
 - develop the Keras model layers
