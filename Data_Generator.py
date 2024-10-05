import tensorflow as tf
import nibabel as nib
import numpy as np
from scipy.ndimage import rotate, shift, zoom
from tensorflow.keras.utils import Sequence # type: ignore
from tensorflow.keras.preprocessing.image import ImageDataGenerator#type: ignore

def load_nifti_image(file_name):
    img = nib.load(f'./New_Processed/New_Processed/{file_name}')
    img_data = img.get_fdata()
    img_data = np.expand_dims(img_data, axis=-1)
    return img_data

class NiftiDataGenerator(Sequence):
    def __init__(self, file_paths, labels, batch_size=5, dim=(182, 218, 182), n_channels=1, n_classes=2, augment=True,*args,**kwargs):
        self.file_paths = file_paths
        self.labels = labels
        self.batch_size = batch_size
        self.dim = dim
        self.n_channels = n_channels
        self.n_classes = n_classes
        self.augment = augment
        self.on_epoch_end()

    def __len__(self):
        return int(np.floor(len(self.file_paths) / self.batch_size))
    def on_epoch_end(self,*args,**kwargs):
        pass


    def __getitem__(self, index):
        batch_paths = self.file_paths[index * self.batch_size:(index + 1) * self.batch_size]
        batch_labels = self.labels[index * self.batch_size:(index + 1) * self.batch_size]
        X, y = self.__data_generation(batch_paths, batch_labels)
        return X, y
    def __data_generation(self, batch_paths, batch_labels):
        X = np.empty((self.batch_size, *self.dim, self.n_channels))
        y = np.empty((self.batch_size), dtype=int)

        for i, (file_path, label) in enumerate(zip(batch_paths, batch_labels)):
            img_data = load_nifti_image(file_path)
            X[i]=img_data
            y[i] = label
            
        return X, y
