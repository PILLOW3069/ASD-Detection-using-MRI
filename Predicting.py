import tensorflow as tf
import numpy as np
def predict(data):
    
    asd_detector=tf.keras.models.load_model('./ALLOUT_ASD_predictor_v1.keras')
    data=np.expand_dims(data,axis=-1)
    data=np.expand_dims(data,axis=0)
    temp=asd_detector.predict(data)
    print('predicted')
    return temp[0][0]
    