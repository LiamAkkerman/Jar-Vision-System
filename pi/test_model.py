import numpy as np
print('numpy:', np.__version__)

# import tensorflow as tf
# print('tensroflow:', tf.__version__)

# from tensorflow import keras
# print('keras:', keras.__version__)

import tensorflow.lite as tflite
#print('tflite:', tflite.__version__)


sample_input = np.array(np.load('image_20210410181812.npy', allow_pickle=True)[94:594, 236:736, :]/255.0, dtype=np.float32)
sample_input = np.reshape(sample_input, [1, 500, 500, 3])
print('image loaded as', sample_input.shape, type(sample_input))

interpreter = tflite.Interpreter(model_path='model-202104182124.tflite')
print('interpreter loaded', type(interpreter))

interpreter.allocate_tensors()

# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

print(input_details)
print(output_details)

# Test the model on random input data.
interpreter.set_tensor(input_details[0]['index'], sample_input)

interpreter.invoke()

# The function `get_tensor()` returns a copy of the tensor data.
# Use `tensor()` in order to get a pointer to the tensor.
output_data = interpreter.get_tensor(output_details[0]['index'])
print(output_data)
