import keras
import numpy as np
import tensorflow as tf
import h5py
import keras.backend as K
from keras.callbacks import LearningRateScheduler
from keras.callbacks import EarlyStopping
import tensorflow as tf
import os
import matplotlib.pyplot as plt
import matplotlib
import tensorflow.keras.optimizers
from sklearn.model_selection import train_test_split
import CnnModel as msmla
from keras.callbacks import ReduceLROnPlateau

matplotlib.use('TkAgg')
x_training = np.load(r"x_training.npy")
y_training = np.load(r"y_training.npy")

x_testing = np.load(r"x_testing.npy")
y_testing = np.load(r"y_testing.npy")

x_validation = np.load(r"x_validation.npy")
y_validation = np.load(r"y_validation.npy")
resolution = 32
band_num = 10
batch_size =32
earlystop_callback = EarlyStopping(
  monitor='val_accuracy',  patience=2,verbose=1, mode='auto')
def scheduler(epoch):
    if epoch % 1 == 0 and epoch != 0:
        lr = K.get_value(model.optimizer.lr)
        K.set_value(model.optimizer.lr, lr * 0.1)
        print("lr update to {}".format(lr * 0.1))
    return K.get_value(model.optimizer.lr)
reduce_lr = LearningRateScheduler(scheduler)

def generator():
    while 1:
        row = np.random.randint(0,len(x_training),size=batch_size)
        x = np.zeros((batch_size,x_training.shape[-1]))
        y = np.zeros((batch_size,))
        x = x_training[row]
        y = y_training[row]
        yield x,y
Reduce = ReduceLROnPlateau(monitor='val_accuracy',
                           factor=0.1,
                           patience=1,
                           verbose=1,
                           mode='auto',
                           epsilon=0.0001,
                           cooldown=0,
                           min_lr=0)


model = msmla.MSMLA50((resolution,resolution,band_num))
history = model.fit_generator(generator(), epochs=50, steps_per_epoch=len(x_training)//(batch_size),  callbacks=[Reduce,earlystop_callback], validation_data=[x_validation,y_validation])
model.save_weights('Parameters.h5', save_format='h5')
plt.switch_backend('TkAgg')
fig1 = plt.figure()
plt.plot(history.history['loss'],'r',linewidth=3.0)
plt.plot(history.history['val_loss'],'b',linewidth=3.0)
plt.legend(['Training loss', 'Validation Loss'],fontsize=18)
plt.xlabel('Epochs ',fontsize=16)
plt.ylabel('Loss',fontsize=16)
plt.title('Loss Curves :CNN',fontsize=16)
fig1.savefig('loss_cnn.png')
plt.show()


fig2=plt.figure()
plt.plot(history.history['accuracy'],'r',linewidth=3.0)
plt.plot(history.history['val_accuracy'],'b',linewidth=3.0)
plt.legend(['Training Accuracy', 'Validation Accuracy'],fontsize=18)
plt.xlabel('Epochs ',fontsize=16)
plt.ylabel('Accuracy',fontsize=16)
plt.title('Accuracy Curves : CNN',fontsize=16)
fig2.savefig('accuracy_cnn.png')
plt.show()

print('------------------Start testing------------------')
loss, acc = model.evaluate(x_testing, y_testing)
print('test loss:', loss)
print('test accuracy:', acc)
