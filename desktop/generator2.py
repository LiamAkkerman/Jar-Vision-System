import numpy as np
import matplotlib.pyplot as plt
from skimage.draw import disk
import pickle
import bz2


''' testing and examples for the dataset '''

def exit_dist(elem):
    ''' find distance to (0,0) which is approximately the exit '''
    return np.sqrt(elem[0] ** 2 + elem[1] ** 2)


data_type = np.uint8    # data type in the array. could be float for a 0 to 1 range, unless a keras layer will do that.
max_value = np.iinfo(np.dtype(data_type)).max # an all-the-way on pixel  # lol why such complicated
tray_side = 500         # the number of pixels on each edge of the tray
jar_dia = np.floor(tray_side/5.5) # the diameter of a jar in pixels. the 5.5 is an estimate
print(jar_dia)

# generate a grid of 25 equal spaced coordinates
equal_grid = list()
spacing = (tray_side/2 - jar_dia*0.55)/2 # the 0.55 is an estimate so it's not right on the edge
for i in range(-2, 3):
        for j in range(-2, 3): # probably a better way to do this but whatever
                coord = (tray_side/2 + i*spacing, tray_side/2 + j*spacing)
                equal_grid.append(coord)
equal_grid.sort(key=exit_dist) # sort the list by how close to the exit the jars are

# fill in a dataset with each fullness of the tray
coords = list()
dataset = list()
dataset.append({'image': np.zeros((tray_side, tray_side, 3), dtype=data_type), 'label': list(), 'filename': 'ideal_data_0', 'testing': True}) # include an empty tray
while equal_grid:
        coords.append(equal_grid.pop()) # include one more jar each time, starting from furthest from 
        image = np.zeros((tray_side, tray_side, 3), dtype=data_type)

        for coord in coords:
                rr, cc = disk(coord, jar_dia/2) # draw a circle
                image[rr, cc, :] = max_value # write it onto the image
                

        dataset.append({'image': image, 'label': coords.copy(), 'filename': 'ideal_data_' + str(len(coords)), 'testing': True})

# write to file and compress
# using bz2 because the data is highly compressible 
with bz2.BZ2File('dataset/ideal_data.pkl.bz2', mode='w') as f:
        pickle.dump(dataset, f)

# test read from file
with bz2.BZ2File('dataset/ideal_data.pkl.bz2', mode='r') as f:
        test_read = pickle.load(f)
        print(test_read[6])

        plt.imshow(test_read[6]['image'])
        plt.show()

