import numpy as np
from tensorflow.keras.models import Model
from tensorflow.keras.layers import *
import tensorflow as tf
from utils import se_convolutional_block, se_identity_block , Xception_block
from utils import cbam_block as cbam
import tensorflow.keras
import keras
import numpy as np
import CnnModel as msmla
import tensorflow as tf
import h5py
import keras.backend as K
import tensorflow as tf
import os
import matplotlib.pyplot as plt
import matplotlib
import tensorflow.keras.optimizers
from sklearn.model_selection import train_test_split



batch_size =32
resolution = 32
band_num = 10

def generator():
    g_index = 0
    range = len(np_prediction)
    while 1:
        if g_index+batch_size <  range:
            row = np.arange(g_index, g_index + batch_size)
        else:
            row = np.arange(g_index,range)

        x = np.zeros((batch_size,np_prediction.shape[-1]))
        x = np_prediction[row]
        g_index = g_index + batch_size
        yield x




np_prediction = np.load(r'pre_image.npy')

model = msmla.MSMLA50((resolution,resolution,band_num))
model.load_weights('Weights.h5')

preds = model.predict_generator(generator(),steps=len(np_prediction)//batch_size+1,verbose=1)
one_res = np.argmax(preds, axis = 1)
print(one_res.shape)
print(one_res)
np.save(r'result.npy',one_res)
