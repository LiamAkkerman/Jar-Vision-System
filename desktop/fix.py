# import file I/O libraries
from datetime import datetime
from glob import glob
import bz2
import pickle
import numpy as np

dataset = list()
archive_list = glob('./dataset/*.pkl.bz2')
archive_filename = 'dataset/archive_' + datetime.now().strftime('%Y%m%d%H%M%S') + '.pkl.bz2'

for archive in archive_list:
    with bz2.BZ2File(archive, mode='r') as f:
        dataset.extend(pickle.load(f))
print('files loaded')


''' strip path to dataset '''
# for item in dataset:
#     if not item['testing']:
#         print(item['filename'][0:9] + '\\' + item['filename'][-24:])
#         item['filename'] = item['filename'][0:9] + '\\' + item['filename'][-24:]
# labels = [a['label'] for a in dataset if not a['testing']]
# for label in labels:
#     label = [a for a in label if not np.isnan(a).any()]

''' remove nan rows '''
for item in dataset:
    if not item['testing']:
        if np.isnan(item['label']).any():
            item['label'] = [a for a in item['label'] if not np.isnan(a).any()]
# labels = [a['label'] for a in dataset if not a['testing']]

''' check unique '''
# uniques = np.unique([a['image'] for a in dataset if not a['testing']])
# print(uniques.shape)

# new_dataset = list()
# for item in dataset:
#     if item['image'] in uniques:
#         uniques.remove(item)
#         new_dataset.append(item)

# print(*labels, sep='\n')

# print('total', len(dataset), 'items')
# print('unique', len(uniques), 'items')
# print('consolidating', len(new_dataset), 'items')



''' save archive '''
print('consolidating', len(dataset), 'items')
with bz2.BZ2File(archive_filename, mode='w') as f:
    pickle.dump(dataset, f)
