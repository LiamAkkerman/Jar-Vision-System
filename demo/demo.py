import numpy as np
import matplotlib.pyplot as plt
import tensorflow.lite as tflite
from glob import glob


interpreter = tflite.Interpreter(model_path='./demo/model.tflite')
print('interpreter loaded', type(interpreter))

interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()


images = glob('./demo/*.npy')
for image_name in images:
    image = np.asarray(np.load(image_name, allow_pickle=True)/255.0, dtype=np.float32)
    image_cropped = image.copy()[79:579, 236:736, :] # crop image
    image_sized = np.resize(image_cropped, (1, *image_cropped.shape))

    interpreter.set_tensor(input_details[0]['index'], image_sized)
    interpreter.invoke()
    pred = interpreter.get_tensor(output_details[0]['index'])
    overlay_pred = np.squeeze(pred, axis=0)
    pred = overlay_pred.copy()
    overlay_pred[overlay_pred < 0.1] = None

    fig, ax = plt.subplots()
    ax.imshow(image_cropped)
    plt.xlim([0, 500])
    plt.ylim([0, 500])
    plt.title('Input Image')

    fig, ax = plt.subplots()
    ax.imshow(image_cropped)
    ax.imshow(overlay_pred, cmap='Reds', alpha=0.6)
    plt.xlim([0, 500])
    plt.ylim([0, 500])
    plt.title('Input Image with Predicted Overlay')

    fig, ax = plt.subplots()
    ax.imshow(pred, cmap='Reds')
    plt.xlim([0, 500])
    plt.ylim([0, 500])
    plt.title('Model Prediction')

    plt.show()
    


