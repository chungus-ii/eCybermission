import os
import cv2
import numpy as np
from tensorflow as tf
from sklearn as preprocessing

class Generator(tf.keras.utils.Sequence):
    def init(self, DATASET_PATH = '/eCybermission/dataset', BATCH_SIZE = 50, image_min_side = 50):
        
        #size of the batches that will be generated
        self.batch_size = BATCH_SIZE

        #if the image's smalles side is smaller than this, it will be enarged while keeping it's aspect ratio
        self.image_min_side = image_min_side