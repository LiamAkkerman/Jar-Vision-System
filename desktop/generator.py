# # import general libraries
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.widgets import Button
from glob import glob
import bz2
import pickle

def pts_to_centre(pts):
    '''
    returns coordinates of centre of a circle and radius from 3 points on the edge
    reference: https://math.stackexchange.com/a/1460096
    '''

    # define system of equations
    np_arr = np.asarray([
        [pts[0][0]**2 + pts[0][1]**2, pts[0][0], pts[0][1], 1],
        [pts[1][0]**2 + pts[1][1]**2, pts[1][0], pts[1][1], 1],
        [pts[2][0]**2 + pts[2][1]**2, pts[2][0], pts[2][1], 1]
    ])

    # take each minor and the determinates
    m11 = np.linalg.det(np.delete(np_arr, 0, axis=1))
    m12 = np.linalg.det(np.delete(np_arr, 1, axis=1))
    m13 = np.linalg.det(np.delete(np_arr, 2, axis=1))
    m14 = np.linalg.det(np.delete(np_arr, 3, axis=1))

    # calculate
    x0 = 0.5 * (m12 / m11)
    y0 = -0.5 * (m13 / m11)
    r = np.sqrt(x0 ** 2 + y0 ** 2 + (m14 / m11))

    return (x0, y0, r)

def draw_centres(ax, pts):
    pass

def undo_b(event):
    global undo_flag
    print('undo')
    undo_flag = True


def clear_b(event):
    print('clear')
    global centres
    centres = list()
    #[shape.remove() for shape in ax.patches]
    ax.patches = []

def next_b(event):
    global next_image_flag
    print('next')
    next_image_flag = True

def done_b(event):
    global done_flag
    print('done')
    done_flag = True


next_image_flag = False
done_flag = False
undo_flag = False

plt.clf()
fig, ax = plt.subplots()
plt.subplots_adjust(right=0.85)

ax_next = plt.axes([0.82, 0.50, 0.15, 0.08])
ax_undo = plt.axes([0.82, 0.35, 0.15, 0.08])
ax_clear = plt.axes([0.82, 0.20, 0.15, 0.08])
ax_done = plt.axes([0.82, 0.05, 0.15, 0.08])
bnext = Button(ax_next, 'Next photo')
bnext.on_clicked(next_b)
bundo = Button(ax_undo, 'Undo')
bundo.on_clicked(undo_b)
bclear = Button(ax_clear, 'Clear')
bclear.on_clicked(clear_b)
bdone = Button(ax_done, 'Done') # exit?
bdone.on_clicked(done_b)

plt.ion()

file_list = glob('./desktop/set1/*.npy')
archive_list = glob('./dataset/*.pkl.bz2')

centres = list()
markers = list()
dataset = list()

while not done_flag:
    next_image_flag = False
    undo_possible = False

    if not file_list:
        print('no more images to be done')
        break

    image_name = file_list.pop()
    print('\nnext image:', image_name)
    image = np.load(image_name, allow_pickle=True)
    image_cropped = image.copy()[99:599, 236:736, :] # crop image
    ax.imshow(image_cropped)

    while not (next_image_flag or done_flag):
        undo_flag = False
        pts = list()
        while len(pts) < 3 and not (next_image_flag or done_flag or undo_flag):
            point = list()

            point = plt.ginput(1, timeout=0.5)  # buttons will work right away but more resource heavy
            # point = plt.ginput(1, timeout=-1) # an extra click is needed to flush but better performance
            
            if point: # conditional is just for timeout mode
                point = point[0]
                if point[0] < 1 or point[1] < 1:
                    # a button was probably clicked
                    pass
                else:
                    markers.append(ax.scatter(point[0], point[1], color='red', marker='+'))
                    pts.append(point)

        if undo_flag:
            if markers: # clear the current markers
                [marker.remove() for marker in markers]
                markers = list() 
            elif undo_possible: # remove the last centre selection
                print('removing last centre')
                centres.pop()
                outline_marker.remove()
                centre_marker.remove()
                print(len(centres), 'should remain')
                undo_possible = False
            else: # nothing can be undo'd
                print('can only undo up to 1 previous centre and from the current image')
            continue 

        [marker.remove() for marker in markers]
        markers = list()           

        if not (next_image_flag or done_flag):
            # error handling
            if len(pts) != 3: # not enough points in circle
                print('malformed circle, try again')
                print('not enough points')
                continue
            if any([i[0] < 1 or i[1] < 1 for i in pts]): # this means somewhere outside was probably clicked, like a button
                print('malformed circle, try again')
                print('abnormal coordinate included (likely a button)')
                continue

            (x0, y0, r) = pts_to_centre(pts)

            if abs(r - 35) > 15: # circle weird size
                print('malformed circle, try again')
                print('abnormal circle size')
                continue

            print('centre', (x0, y0), 'radius', r)
            centres.append((x0, y0))

            outline_marker = patches.Circle((x0, y0), radius=r, linewidth=1, edgecolor='r', facecolor='none')
            ax.add_patch(outline_marker)
            centre_marker = patches.Circle((x0, y0), radius=2, color='r')
            ax.add_patch(centre_marker)

            undo_possible = True # indicates there's something to undo

    print('image processed with', len(centres), 'centres')
    # save image and label into dataset
    dataset.append({'image': image_cropped, 'label': centres.copy(), 'filename': image_name, 'testing': True})

# save dataset to file
print('\nlabeled', len(dataset), 'images')
archive_filename = 'dataset/test_data.pkl.bz2'
with bz2.BZ2File(archive_filename, mode='w') as f:
    pickle.dump(dataset, f)
print(archive_filename, 'saved')
print('exiting')

