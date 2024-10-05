import tensorflow as tf
import nibabel as nib
import numpy as np
from scipy.ndimage import rotate, shift, zoom
from tensorflow.keras.utils import Sequence # type: ignore
from tensorflow.keras.preprocessing.image import ImageDataGenerator#type: ignore
from tensorflow.keras.layers import Conv3D, MaxPooling3D, Flatten, Dense, Dropout, BatchNormalization, GlobalAveragePooling3D#type: ignore
import pandas as pd
import os
from Data_Feeder import file_names

checkpoint_path = "/kaggle/working/latest.weights.h5"
checkpoint_dir = os.path.dirname(checkpoint_path)

import math
n_batches = len(file_names) / 5
n_batches = math.ceil(n_batches) 


cp_callback = tf.keras.callbacks.ModelCheckpoint(
    filepath=checkpoint_path, 
    verbose=1, 
    save_weights_only=True,
    save_freq=5*n_batches)

input_shape=(182,218,182,1)
asd_detector=tf.keras.models.Sequential()
asd_detector.add(Conv3D(filters=32,kernel_size=(3,3,3),activation='relu',input_shape=input_shape))
asd_detector.add(MaxPooling3D(pool_size=(2,2,2)))
asd_detector.add(BatchNormalization())


asd_detector.add(GlobalAveragePooling3D())

asd_detector.add(Dense(64,activation='relu'))
asd_detector.add(Dropout(0.3))

asd_detector.add(Dense(1,activation='sigmoid'))
asd_detector.compile(optimizer='adam',loss='binary_crossentropy',metrics=['accuracy'])