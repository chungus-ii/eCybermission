import os
import cv2
import numpy as np
from tensorflow as tf
from sklearn as preprocessing

class Generator(tf.keras.utils.Sequence):
    #DATASET_PATH is the training directory or the testing directory, not the directory that contains both
    def init(self, DATASET_PATH, BATCH_SIZE = 50, image_min_side = 50):
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
        
        #iterating through each class
        for class_name in classes:
            #path for the current class
            class_path = os.path.join(DATASET_PATH, class_name)
            #iterating through each image in the class
            for image_file_name in os.listdir(class_path):
                #adding the image path
                self.image_paths.append(os.path.join(class_path, image_file_name))
                #adding the image label
                self.image_labels.append(class_name)
        #transforming all the labels into numbers
        self.image_labels = np.array(lb.transform(self.image_labels), dtype='float32')
        #check that the image_paths and image_labels are the same, which is necessary becuase each label corresponds with an image
        assert len(self.image_paths) == len(self.image_labels)

    def create_image_groups(self):
        #shuffle the images
        seed = 4321
        np.random.seed(seed)
        np.random.shuffle(self.image_paths)
        np.random.seed(seed)
        np.random.shuffle(self.image_labels)

        #TODO: Divide image_labels and image_paths, based on BATCH_SIZE
