import numpy as np
import matplotlib.pyplot as plt
import tensorflow.lite as tflite
from glob import glob


interpreter = tflite.Interpreter(model_path='./model_202104240144.tflite')
print('interpreter loaded', type(interpreter))

interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()


images = glob('./demo/*.npy')
for i, image_name in enumerate(images):
    image = np.asarray(np.load(image_name, allow_pickle=True)/255.0, dtype=np.float32)
    image_cropped = image.copy()[79:579, 236:736, :] # crop image
    image_sized = np.resize(image_cropped, (1, *image_cropped.shape))

    interpreter.set_tensor(input_details[0]['index'], image_sized)
    interpreter.invoke()
    pred = interpreter.get_tensor(output_details[0]['index'])
    overlay_pred = np.squeeze(pred, axis=0)
    pred = overlay_pred.copy()
    overlay_pred[overlay_pred < 0.1] = None

    fig, ax = plt.subplots(nrows=3, sharex=True, figsize=(4, 12))

    ax[0].imshow(image_cropped)
    ax[0].set_xlim([0, 500])
    ax[0].set_ylim([0, 500])
    ax[0].set_title('Input Image')

    ax[1].imshow(image_cropped)
    ax[1].imshow(overlay_pred, cmap='Reds', alpha=0.6)
    ax[1].set_xlim([0, 500])
    ax[1].set_ylim([0, 500])
    ax[1].set_title('Input Image with Predicted Overlay')

    ax[2].imshow(pred, cmap='Reds')
    ax[2].set_xlim([0, 500])
    ax[2].set_ylim([0, 500])
    ax[2].set_title('Model Prediction')

    plt.savefig('./demo/image_' + str(i) + '.png', format='png')
    


