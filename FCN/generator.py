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
    
    def load_image_paths_and_labels(self, DATASET_PATH):
        """
        This is used to load a list of image paths and a list of their labels.
        This information will be saved to the object after initialization.
        """
        
        #list of paths of class directories within image directory
        classes = os.listdir(DATASET_PATH)
        #creation of LabelBinarizer object, 
        lb = preprocessing.LabelBinarizer()
        #fitting LabelBinarizer to current classes
        lb.fit(classes)

        #creating lists for image paths and label
        self.image_paths = []
        self.image_labels = []
        
        #TODO - contiue from this point (have to eat dinner)